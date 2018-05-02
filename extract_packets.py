from scapy.all import *
import codecs
import sys
import sqlite3

def usage():
    print('python extract_packets.py pcap_file cookies_db')

if len(sys.argv) < 3:
    print('Insufficient arguments')
    usage()
    exit(1)

pcap_file = sys.argv[1]
pcap = None

try:
    pcap = rdpcap(pcap_file)
except FileNotFoundError:
    print('Could not find file:', pcap_file)
except PermissionError:
    print('Did not have read permissions for file:', pcap_file)

if not pcap:
    exit(1)

sessions = pcap.sessions()

class HTTP_Packet:
    GET      = 'GET'
    POST     = 'POST'
    RESPONSE = 'RESPONSE'
    INVALID  = 'INVALID'

    def __init__(self, src, dst, payload):
        self.src = src
        self.dst = dst

        idx = payload.find('\r\n\r\n')
        if idx == -1:
            self.type = HTTP_Packet.INVALID
            return
        packet = payload[:idx]
        if packet.startswith('GET'):
            self.type = HTTP_Packet.GET
            get = packet.splitlines()[0]
            self.path = get[len('GET '):(len(get) - len(' HTTP/1.1'))]
        elif packet.startswith('HTTP'):
            self.type = HTTP_Packet.RESPONSE
        else:
            self.type = HTTP_Packet.INVALID
        self.headers = {}
        for header in packet.splitlines()[1:]:
            header = header.split(': ')
            self.headers[header[0]] = header[1]
        self.cookies = []
        if 'set-cookie' in self.headers:
            params = self.headers['set-cookie'].split(';')
            params[0] = params[0].split('=')
            self.cookies.append({'name': params[0][0].strip(), 'value': params[0][1].strip()})
            for param in params[1:]:
                param = param.strip()
                if '=' in param:
                    param = param.split('=')
                    self.cookies[0].update({param[0].strip(): param[1].strip()})
                else:
                    self.cookie[0].update({param: 1})
            # Swap for uniform src/dst
            self.src, self.dst = self.dst, self.src
        if 'Cookie' in self.headers:
            for cookie in self.headers['Cookie'].split(';'):
                cookie = cookie.split('=')
                self.cookies.append({'name': cookie[0].strip(), 'value': cookie[1].strip()})

    def is_valid(self):
        return self.type != HTTP_Packet.INVALID

    def cookie_sql(self):
        sqls = []
        for cookie in self.cookies:
            sqls.append((self.src, self.headers['Host'] + self.path,
                cookie['name'], cookie['value'], self.headers['User-Agent']))
        return sqls

cookies = sqlite3.connect(sys.argv[2])
c = cookies.cursor()
c.execute('''
        CREATE TABLE IF NOT EXISTS cookies (
            src text NOT NULL,
            url text NOT NULL,
            name text NOT NULL,
            value text NOT NULL,
            user_agent text,
            PRIMARY KEY (src, url, name)
        );''')
cookies.commit()

cookie_packets = []
for packet in pcap:
    try:
        if packet[TCP].dport == 80 or packet[TCP].sport == 80:
            if type(packet[TCP].payload) == scapy.packet.Raw:
                payload = codecs.decode(bytes(packet[TCP].payload), encoding='utf-8', errors='replace')
                http_packet = HTTP_Packet(packet[IP].src, packet[IP].dst, payload)
                if http_packet.is_valid():
                    if 'Cookie' in http_packet.headers:
                        c.executemany('INSERT OR REPLACE INTO cookies VALUES (?,?,?,?,?)', http_packet.cookie_sql())
                        cookies.commit()
    except IndexError as e:
        continue

cookies.close()
