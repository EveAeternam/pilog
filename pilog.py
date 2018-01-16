#import tty
#import sys
#import termios

import csv

from guizero import App, Text, TextBox, Picture, info, PushButton, Box, error

app = App(title="Hello World!", width = 420, height=340) #, layout="grid")
msg_intro = Text(app, text="Scan ID Card to begin checkout process", size=15) #, grid=[0,0], align="top")
msg_intro2 = Text(app, text="or scan Equipment to return", size=15) #, grid=[0,1], align="top")
pic = Picture(app, image="img/barcode.png") #, grid=[0,2], align="top")
id_scan = TextBox(app, width=40, grid=[0,3]) #, align="top")
is_logged = "false"
user_logged = ""
user_id = ""
n=0
session_timeout=240

def main():
	
	id_scan.focus()
	app.after(1000, loopyloop)
	#app.tk.attributes("-fullscreen", True)
	app.display()
	
	return 0
	
def loopyloop():
	
	raw_id = id_scan.value
	global n
	global user_logged
	global user_id
	
	print(is_logged + " ; " + user_logged + " ; " + user_id)
	
	if (is_logged == "true"):
		n += 1
		
	if (n==session_timeout):
		loguser(user_logged)
		print("SESSION TIMEOUT")
		n=0
	
	if (what_is(raw_id) == "usr"):
		user_id = get_fit_id(raw_id)
		user_logged = who_is(user_id)
		print("User " + user_logged + " just logged in with ID: " + str(user_id[0:3]) + " " + str(user_id[3:6]) + " " + str(user_id[6:9]))
		loguser(user_logged)
	elif (what_is(raw_id) == "cmd"):
		execute(raw_id)
	
	app.after(1000, loopyloop)
	
def loguser(usr):
	global is_logged
	is_usr_logged = is_logged
	if (is_usr_logged == "false"):
		print(usr+" just logged in!")
		msg_intro.value = "Logged in as:"
		msg_intro2.value = usr
		pic.value = "usr/user.png"
		id_scan.value = ""
		is_logged = "true"
	else:
		print(user_logged+" just logged out!")
		msg_intro.value = "Scan ID Card to begin checkout process"
		msg_intro2.value = "or scan Equipment to return"
		pic.value = "img/barcode.png"
		id_scan.value = ""
		is_logged = "false"
		info("Logged out!", usr + " has successfully logged out!")
	
	return 0
	
def logged(txt):
	
	print("ID: " + str(txt) + " logged")
	#Curl here
	
	return 0
	
def what_is(val):
	
	id_type=""
	if (len(val) == 16):
		id_type="usr"
	else:
		if ("$" in val):
			id_type="cmd"
		else:
			id_type="eqp"
	return id_type

def who_is(val):
	with open('db/userlist.csv', newline='') as csvfile:
		usrd = csv.reader(csvfile)
		for row in usrd:
			x = ','.join(row)
			if str(val) in x:
				return x[10:]
				
def has_pic(val):
	#check if they have a pic
	return 0

	
def get_fit_id(rawid):
	
	fitid = rawid[6:15]
	
	return fitid
	
def execute(cmd):
	
	return 0

if __name__ == '__main__':
	main()

