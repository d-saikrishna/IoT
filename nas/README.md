# Building a Network Attached Storage (NAS) with RPi

Building your own cloud storage

## Things you need:
1. RPi
2. External harddisk
3. Powered USB Hub (optional) - External harddisks draw more power and your RPi charger may not be designed for that.

## Steps:
1. Format your external Harddisk

        # List all your external disks connected
        sudo fdisk -l
        (or)
        lsblk

        # Find the drive (/dev/sda) and partitions (/dev/sda1, /dev/sda2 etc)

        # Unmount the drive
        unmount /dev/sda1
        unmount /dev/sda2
        etc

        # Open Parted wizard
        sudo parted /dev/sda
        ## Create new harddisk label
        mklabel gpt #It will prompt you to erase the drive - Y
        ## Create new partition of ext4 entire disk
        mkpart [Name_of_Drive] ext4 0% 100%
        ## Quit parted wizard
        quit

        # Format the newly created partition with ext4 file system
        sudo mkfs.ext4 /dev/sda1

        # You can also rename the partition
        sudo e2label /dev/sda1 [Name_of_Drive]
        
        # Reboot Pi
        sudo shutdown -r now

        # Give yourselves write permissions on drive
        sudo chown -R pi /media/<username>/<[Name_of_Drive]>

2. Share the drive on your private network using Samba 

        # Install samba on RPi
        sudo apt update
        sudo apt upgrade
        sudo apt install samba samba-common
        
        # Edit the smb.conf file
        sudo nano /etc/samba/smb.conf

        ## Make these changes
               interfaces = lo eth0
        
        ## Add these lines at the end of smb.conf
                [Medianame]
                path = /media/username/directory
                writeable = yes
                create mask = 0777 # all permissions
                directory mask = 0777
                public=no
                browseable = yes

3. Create password and add users

        # Add password to the existing user
        sudo smbpasswd -a <existing_username>

        # Add more users
        sudo adduser <new_user>
        sudo smbpasswd -a <new_user>

4. test samba and restart service

        testparm
        sudo systemctl restart smbd

You'll be able to use NAS on local now using Samba (SMB). You'd find the NAS on File Explorer on Windows, iOS etc. You can also connect using Pi's private IP. `smb://pi.local`

For remote internet access, we can use SFTP:

5. Allow inbound connections to your RPi . Login to your router UI and edit Firewall rules accordingly. If you are using Jio Fiber, Airtel etc., chances are that you don't have a static IP address. You can start with changing IPv6 Firewall rules. Start with "Allow all" - tighthen the security later.
6. Port forwarding. Open port 22 (SSH+SFTP) of your RPi to the internet so that you can use RPi from any device.  I used IPv6 address because Jio Fiber uses CGNAT with IPv4 (meaning I don't have a public IPv4 to open ports). Know RPi's IPv6 by running `ifconfig` on its terminal.
7. Use SFTP to access the HDD from anywhere in the world. Your HDD will be in `/media/username/hdd`

## Costs
Electricity costs per month of hosting this would be about 27Rs (5V*0.85A*24*30/1000 kWh * 9Rs) 

# References:
1. [PCMag](https://www.pcmag.com/how-to/how-to-turn-a-raspberry-pi-into-a-nas-for-whole-home-file-sharing)