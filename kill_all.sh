#!/bin/bash

echo -e "\e[91mKilling everything\n"
./clean_firewall.sh
pkill -f tshark
pkill -f dnsmasq
pkill -f hostapd
pkill -f tmux
cd ..
rm -r captive_portal/
cp /etc/hosts.BAK /etc/hosts
echo -e "\e[91mExiting!"
exit $?

