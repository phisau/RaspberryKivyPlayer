# Description
Simple Raspberry Pi Kivy Media Player. It uses Kivy as the Gui Builder, which is written in Python. You can define three radio stations and a path to your music folder directory.

You can use it as a replacement for a music player with easier touch control than the pre-installed music players on Raspbian.

# Install
Kivy doesn't run on Python3.8, yet. So create a virtual envorenment with Python 3.7 or Python 3.6, then download the repository.
```bash
python3.7 -m virtualenv venv
source venv/bin/activate

git clone https://github.com/phisau/RaspberryKivyPlayer.git
```
# Start
```bash
python main.py
```

# Customization
## Fullscreen
For trying it out on the desktop, set the fullscreen option in the prirpconfig.py to False. To use it on a touchscreen on your Pi, better set it to True.
## Radio
To change the radio stations look into the rpirconfig.py file. At the moment buttons for three (german) radio stations are entered.
## Music
You can also change the path to the music folder in the rpirconfig.py file. I use a Nas, which I connect to via NFS and mount it into the /mnt/nas/music folder.

## Network Tab
This is still individualized to my network. To change the change your IP Addresses for the NAS and Network Analysis look into the main.py file. It's still messy in there, the router is usually picked as 192.168.178.1, the Nas as 192.168.2.28. The VPN Tab calls scripts on my router to change the outgoing VPN. The file is something like this:

```ksh
#!/bin/ksh
# /home/admin/scripts/switch_vpn.sh
# Program to restart tun0 in order to restart vpn

datum=$(date)
country=$1
/usr/bin/pkill "openvpn"

echo "stopped openvpn"
echo "trying to start VPN through $1" 
case $1 in
        ch-at) 
                /usr/local/sbin/openvpn --daemon --config "/home/admin/ovpn/ch-at.ovpn"
        ;;
        is-de) 
                /usr/local/sbin/openvpn --daemon --config "/home/admin/ovpn/is-de.ovpn"
        ;;
        is-us) 
                /usr/local/sbin/openvpn --daemon --config "/home/admin/ovpn/is-us.ovpn"
        ;;
        ch-fr) 
                /usr/local/sbin/openvpn --daemon --config "/home/admin/ovpn/ch-fr.ovpn"
        ;;

esac

echo "restarted interfaces"

 
```

# Screenshots
![Main Menu](https://user-images.githubusercontent.com/28599991/84600211-00be4700-ae78-11ea-942d-e183d2be7ff3.png)
![Nework Menu](https://user-images.githubusercontent.com/28599991/84600222-16337100-ae78-11ea-8641-4b48e8e1a967.png)
