# Building a Network Attached Storage (NAS) with RPi

Building your own cloud storage

Things you need:
1. RPi
2. External harddisk
3. Powered USB Hub (optional)

Steps:
1. Format your external Harddisk
2. Share the drive using Samba. [Here's a good tutorial covering both steps](https://www.pcmag.com/how-to/how-to-turn-a-raspberry-pi-into-a-nas-for-whole-home-file-sharing). Also make the following change in the smb.conf file (you will read about in the tutorial)

        interfaces = lo eth0

        [Medianame]
        path = /media/username/directory
        writeable = yes
        create mask = 0777
        directory mask = 0777
        public=no
        browseable = yes


3. test samba

        testparm
        sudo systemctl restart smbd
You'll be able to use NAS on local now using SMB. For remote internet access:

4. Allow inbound connections to your RPi . Login to your router UI and edit Firewall rules accordingly. If you are using Jio Fiber, Airtel etc., chances are that you don't have a static IP address. You can start with changing IPv6 Firewall rules. Start with "Allow all" - tighthen the security later.
5. Port forwarding. Open port 22 (SSH) of your RPi to the internet so that you can use RPi from any device.  I used IPv6 address because Jio Fiber uses CGNAT with IPv4 (meaning I don't have a public IPv4 to open ports). Know RPi's IPv6 by running `ifconfig` on its terminal.
6. Use SFTP to access the HDD from anywhere in the world. Your HDD will be in `/media/username/hdd`
