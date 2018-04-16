import sys
import os
import subprocess
from collections import Counter

def run_dump(prefix, duration):
    # remove existing output file
    cmd = ['tshark', '-i', interface, '-a', 'duration:' + str(duration), \
            '-T', 'fields', '-e', 'wlan.ssid', 'subtype', 'probereq']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    total_ssids = Counter()
    for line in proc.stdout:
        line = line.strip()
        if len(line) > 0 and line != 'DIRECT-':
            total_ssids[line] += 1

    most = total_ssids.most_common(1)
    print(most[0])
        
if __name__ == '__main__':
    interface = sys.argv[1]
    duration = int(sys.argv[2])

    run_dump(interface, duration)
