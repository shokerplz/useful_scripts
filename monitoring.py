#!/bin/python3
import requests, subprocess, telebot, datetime, time, paramiko, threading, os.path, json
bot = telebot.TeleBot("1361961268:AAFfRYV0jRjSr58Y9JiqA2wJABjLo7dG9lI")
def centos7_checker(client):
    stdin, stdout, stderr = client.exec_command('cat /etc/*-release | grep centos | wc -l \n')
    data = (stdout.read() + stderr.read()).decode("utf-8").replace("\n", "")
    if (int(data) > 0): return True
    return False
if os.path.isfile("host_data") and os.path.getsize("host_data") > 0 and os.path.isfile("disk_data") and os.path.getsize("disk_data") > 0:
    hosts = json.load(open("host_data"))
    disks = json.load(open("disk_data"))
else:
    hosts = {
        "host11": [1,1,1,2,0,0,"11"], # 1 - ping, 2 - curl, 3 - raid, 4 - amount of disks, 5 - amount of not working links, 6 - centos/ubuntu last - host address
        "host12": [1,1,1,2,0,0,"12"],
        "host13": [1,1,1,2,0,0,"13"],
        "host01": [1,1,1,2,0,0,"01"],
        "host02": [1,1,1,2,0,0,"02"],
        "host03": [1,1,1,2,0,0,"03"],
    }
    disks = {host: [] for host in hosts.keys()}
    open("host_data", "w")
    open("disk_data", "w")
chat_id = "175628933"
status = 0
msg = ""
clients = []
for host in [*hosts]:
    address = "192.168.142.1" + hosts[host][-1:][0]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=address, username="ivan", port=22, key_filename="ssh_mail")
    hosts[host][5] = centos7_checker(client)
    clients.append(client)
def ping_curl():
    while True:
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
        now = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        for ping in [*hosts]:
            address = "192.168.142.1" + hosts[ping][-1:][0]
            ping_res = subprocess.call(['ping', '-c', '3', address], stdout=subprocess.DEVNULL)
            try:
                curl_res = requests.get("http://"+address, proxies={'http': None, 'https': None})
                status = 200
            except:
                status = 1
            if (ping_res == 0) and (hosts[ping][0] == 0):
                bot.send_message(chat_id, "["+now+"] [OK] ["+"task"+hosts[ping][-1:][0]+"] Host: "+address+" Up")
                hosts[ping][0] = 1
            elif (ping_res != 0) and (hosts[ping][0] == 1):
                bot.send_message(chat_id, "["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"] Host: "+address+" No ping!")
                print("["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"] Host: "+address+" No ping!")
                hosts[ping][0] = 0
            if (status == 200) and (hosts[ping][1] == 0):
                bot.send_message(chat_id, "["+now+"] [OK] ["+"task"+hosts[ping][-1:][0]+"] Host: "+address+" Wp up")
                hosts[ping][1] = 1
            elif (status != 200) and (hosts[ping][1] == 1):
                bot.send_message(chat_id, "["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"] Host: "+address+" Wp down!")
                print("["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"] Host: "+address+" Wp down!")
                hosts[ping][1] = 0
        time.sleep(1)
def mdstat():
    while True:
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
        now = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        for client in clients:
            ping = "host"+client.get_transport().sock.getpeername()[0][-2:]
            stdin, stdout, stderr = client.exec_command('cat /proc/mdstat | grep _ | wc -l \n')
            data = (stdout.read() + stderr.read()).decode("utf-8").replace("\n", "")
            if (data == "0") and (hosts[ping][2] == 0):
                bot.send_message(chat_id, "["+now+"] [OK] ["+"task"+hosts[ping][-1:][0]+"]"+" Raid is clean")
                hosts[ping][2] = 1
            elif (data != "0") and (hosts[ping][2] == 1):
                bot.send_message(chat_id, "["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"]"+" Raid is degraded!")
                print("["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"]"+" Raid is degraded!")
                hosts[ping][2] = 0
            if (hosts[ping][5]): stdin, stdout, stderr = client.exec_command('/usr/sbin/ip a | grep NO-CARRIER | wc -l \n')
            else: stdin, stdout, stderr = client.exec_command('/sbin/ip a | grep NO-CARRIER | wc -l \n')
            data = (stdout.read() + stderr.read()).decode("utf-8").replace("\n", "")
            if (data == "0") and (hosts[ping][4] > 0):
                bot.send_message(chat_id, "["+now+"] [OK] ["+"task"+hosts[ping][-1:][0]+"]"+" Links are ok")
                hosts[ping][4] = 0
            elif (data != "0") and (hosts[ping][4] == 0):
                bot.send_message(chat_id, "["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"]"+" One or more links disconnected")
                print("["+now+"] [ALARM] ["+"task"+hosts[ping][-1:][0]+"]"+" One or more links disconnected")
                hosts[ping][4] = 1
            stdin, stdout, stderr = client.exec_command('lsblk -d | grep disk \n')
            data = (stdout.read() + stderr.read()).decode("utf-8").splitlines()
            msg = ""
            if (len(data) > hosts[ping][3]):
                for disk_info in data:
                    if (disk_info not in disks[ping]):
                        msg += "DISK "+disk_info.split()[0]+" "+disk_info.split()[3]+" Inserted "
                        disks[ping].append(disk_info)
                print(msg)
                bot.send_message(chat_id, "["+now+"] [MESSAGE] ["+"task"+hosts[ping][-1:][0]+"]"+" "+msg)
                hosts[ping][3] = len(data)
            if (len(data) < hosts[ping][3]):
                for disk_info in disks[ping]:
                    if (disk_info not in data):
                        msg += "DISK "+disk_info.split()[0]+" "+disk_info.split()[3]+" Removed "
                        disks[ping].remove(disk_info)
                print(msg)
                bot.send_message(chat_id, "["+now+"] [MESSAGE] ["+"task"+hosts[ping][-1:][0]+"]"+" "+msg)
                hosts[ping][3] = len(data)
        json.dump(hosts, open("host_data",'w'))
        json.dump(disks, open("disk_data",'w'))
        time.sleep(300)
service_monitoring = threading.Thread(target=ping_curl, daemon=True)
mdadm_monitoring = threading.Thread(target=mdstat, daemon=True)
service_monitoring.start()
mdadm_monitoring.start()
while True:
    time.sleep(1)