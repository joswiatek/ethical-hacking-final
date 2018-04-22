#!/bin/bash

if [[ "$(id -u)" != "0" ]]; then
	echo -e "\nThis script must be run as root" 1>&2
	exit 0
fi

# Need to setup wireless device

airmon-ng check kill
/etc/init.d/avahi-daemon stop

iwconfig 
airmon-ng start wlan0
iwconfig 

echo "Test wireless device"
timeout --foreground 3 airodump-ng wlan0mon

#Perform Probe Count
echo "Perform Probe Count"

SSID=$(python probe_count.py wlan0mon 30)
echo -e "SSID: $SSID\n"

read -p "Press enter to continue"

# Install prereqs for Captive Portal
apt update
apt -y install hostapd dnsmasq apache2

git clone https://github.com/AloysAugustin/captive_portal.git
cd captive_portal

for f in $(ls); do sed -i 's/wlan0/wlan0mon/g' $f; done

sed -i 's/FR/US/g' hostapd.conf
sed -i "s/CaptiveWifi/$SSID DO NOT CONNECT/g" hostapd.conf
sed -i 's/channel=10/channel=6/g' hostapd.conf
cp -r ../portal/templates/* templates
cp -r ../portal/static/* static
cp ../portal/server.py ./

# Add what we want to do to the start script
echo -e "tmux select-pane -t 0\n" >> start.sh
echo -e "tmux split-window -v\n" >> start.sh
echo -e 'tmux send-keys "tshark -i wlan0mon -w ../wlan0mon_capture" C-m\n' >> start.sh
echo -e "tmux split-window -v\n" >> start.sh

read -p "Press enter to continue"

bash start.sh 
tmux attach
