"""
this program keeps track of stop signals 
and quits all side programs based of pid,
you can think of it like a central control 
system or a handler controlled by client.py

"""

import subprocess
stop = input()
script_name = "sattracker.py"
ps_out = subprocess.Popen("ps -ef".split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().decode('UTF-8').split("\n")
for entry in ps_out:  
    if script_name in entry:
        pid = entry.split()[1]
        subprocess.run(f"kill {pid}")

