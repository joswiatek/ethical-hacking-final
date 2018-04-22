#!/bin/bash

echo -e "\e[91mKilling everything\n"
pkill -f tshark
pkill -f dnsmasq
pkill -f hostapd
pkill -f tmux
cd ..
rm -r captive_portal/
echo -e "\e[91mExiting!"
exit $?

