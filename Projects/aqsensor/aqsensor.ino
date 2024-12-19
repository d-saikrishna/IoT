#include <ArduinoWiFiServer.h>
#include <BearSSLHelpers.h>
#include <CertStoreBearSSL.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiAP.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiGratuitous.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiSTA.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiType.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiClientSecureBearSSL.h>
#include <WiFiServer.h>
#include <WiFiServerSecure.h>
#include <WiFiServerSecureBearSSL.h>
#include <WiFiUdp.h>


/*
    Grove_Air_Quality_Sensor.ino
    Demo for Grove - Air Quality Sensor.

    Copyright (c) 2019 seeed technology inc.
    Author    : Lets Blu
    Created Time : Jan 2019
    Modified Time:

    The MIT License (MIT)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
*/
#include "Air_Quality_Sensor.h"

AirQualitySensor sensor(A0);
WiFiClientSecure client;
String GAS_ID = "GoogleAppScript_ID";
const char* ssid = "wifiname";
const char* password = "password";

const char* host = "script.google.com";
const int httpsPort = 443;

#define ON_Board_LED 2  //--> Defining an On Board LED, used for indicators when the process of connecting to a wifi router

void setup(void) {
    Serial.begin(9600);
    while (!Serial);
    Serial.println("Waiting sensor to init...");
    delay(20000);

    if (sensor.init()) {
        Serial.println("Sensor ready.");
    } else {
        Serial.println("Sensor ERROR!");
    }

    WiFi.begin(ssid, password); //--> Connect to your WiFi router
    Serial.println("");
    pinMode(ON_Board_LED,OUTPUT); //--> On Board LED port Direction output
    digitalWrite(ON_Board_LED, HIGH); //--> Turn off Led On Board

    //----------------------------------------Wait for connection
    Serial.print("Connecting");
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      //----------------------------------------Make the On Board Flashing LED on the process of connecting to the wifi router.
      digitalWrite(ON_Board_LED, LOW);
      delay(250);
      digitalWrite(ON_Board_LED, HIGH);
      delay(250);
      //----------------------------------------
    }
    //----------------------------------------
    digitalWrite(ON_Board_LED, HIGH); //--> Turn off the On Board LED when it is connected to the wifi router.
    //----------------------------------------If successfully connected to the wifi router, the IP Address that will be visited is displayed in the serial monitor
    Serial.println("");
    Serial.print("Successfully connected to : ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println();
    //----------------------------------------

    client.setInsecure();
}

void loop(void) {
    int quality = sensor.slope();
    int aq = 9999; //0 = fresh; 1 = low pollution; 2 = high; 3 = very high

    Serial.print("Sensor value: ");
    Serial.println(sensor.getValue());

    if (quality == AirQualitySensor::FORCE_SIGNAL) {
        Serial.println("High pollution! Force signal active.");
        aq = 3;
    } else if (quality == AirQualitySensor::HIGH_POLLUTION) {
        Serial.println("High pollution!");
        aq = 2;
    } else if (quality == AirQualitySensor::LOW_POLLUTION) {
        Serial.println("Low pollution!");
        aq = 1;
    } else if (quality == AirQualitySensor::FRESH_AIR) {
        Serial.println("Fresh air.");
        aq = 0;
    }

    sendData(sensor.getValue(), aq); //--> Calls the sendData Subroutine
    delay(3600000); // Every hour
}

// Subroutine for sending data to Google Sheets
void sendData(int sensorval, int aq) {
  Serial.println("==========");
  Serial.print("connecting to ");
  Serial.println(host);
  
  //----------------------------------------Connect to Google host
  if (!client.connect(host, httpsPort)) {
    Serial.println("connection failed");
    return;
  }
  //----------------------------------------

  //----------------------------------------Processing data and sending data
  String string_sensorval =  String(sensorval);
  String string_aq =  String(aq);
  String url = "/macros/s/" + GAS_ID + "/exec?SensorVal=" + string_sensorval + "&AQ=" + string_aq;
  Serial.print("requesting URL: ");
  Serial.println(url);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
         "Host: " + host + "\r\n" +
         "User-Agent: BuildFailureDetectorESP8266\r\n" +
         "Connection: close\r\n\r\n");

  Serial.println("request sent");
  //----------------------------------------

  //----------------------------------------Checking whether the data was sent successfully or not
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
  // String line = client.readStringUntil('\n');
  // if (line.startsWith("{\"state\":\"success\"")) {
  //   Serial.println("esp8266/Arduino CI successfull!");
  // } else {
  //   Serial.println("esp8266/Arduino CI has failed");
  // }
  // Serial.print("reply was : ");
  // Serial.println(line);
  // Serial.println("closing connection");
  // Serial.println("==========");
  // Serial.println();
  //----------------------------------------
} 
