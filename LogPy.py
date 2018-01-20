import csv
import sys
import urllib.request
import urllib.parse

from guizero import App, Text, TextBox, Picture, info, PushButton, Box, error

# UI MODULES
app = App(title="Equipment Logger - FITV", width = 420, height=340)
msg_intro = Text(app, text="Scan ID Card to begin checkout process", size=15)
msg_intro2 = Text(app, text="or scan Equipment to return", size=15)
pic = Picture(app, image="img/barcode.png")
id_scan = TextBox(app, width=40)

# GLOBAL VARIABLES
session_is_logged = "false"
session_user_logged = ""
session_user_id = ""

# GLOBAL CONSTANTS
n=0
session_timeout=240
url = 'https://maker.ifttt.com/trigger/fitv_equip_log/with/key/bw9CXnOD2nsTte7e7ZL2NW'

####

def main():
	
	id_scan.focus()
	app.after(1000, loopyloop)
	#app.tk.attributes("-fullscreen", True)
	app.display()
	
	return 0
	
### ACTUALLY THE MAIN LOOP

def loopyloop():
	
    raw_id = id_scan.value
    
    global session_user_logged
    global session_user_id

    session_timeout_tick()

    id_type = what_is(raw_id)

    if (id_type == "usr-raw"):
        session_timeout_reset()
        usrid = get_fit_id(raw_id)
        if (session_active()):
            session_log_out(usrid)
        else:
            session_log_in(usrid)
    elif (id_type == "usr"):
        session_timeout_reset()
        usrid = raw_id
        if (session_active()):
            session_log_out(usrid)
        else:
            session_log_in(usrid)
    elif (id_type == "cmd"):
        session_timeout_reset()
        execute(raw_id)
    elif (id_type == "eqp"):
        if (session_active()):
            session_timeout_reset()
            if (eqp_exists(raw_id)):
                check_out(raw_id)
            else:
                error("No such ID", "The scanned ID does not exist.")
            id_scan.value = ""
        else:
            error("Not logged in!", "Please log in prior to scanning equipment!")
            id_scan.value = ""

    app.after(1000, loopyloop)

### SESSIONS

def session_log_in(id):
    global session_user_logged
    global session_is_logged

    if (session_is_logged == "false"):
        print("Logging in user: " + who_is(id))
        msg_intro.value = "Logged in as:"
        msg_intro2.value = who_is(id)
        pic.value = "usr/" + id + ".png"
        id_scan.value = ""
        session_is_logged = "true"
        session_user_logged = id
    else:
        print("Warning: Tried logging in while session was active.")

    return 0

def session_log_out(id):
    global session_user_logged
    global session_is_logged

    if (session_is_logged == "true"):
        print("Logging out user: " + who_is(id))
        msg_intro.value = "Scan ID Card to begin checkout process"
        msg_intro2.value = "or scan Equipment to return"
        pic.value = "img/barcode.png"
        id_scan.value = ""
        session_is_logged = "false"
        session_user_logged = ""
        info("Logged out!", who_is(id) + " has successfully logged out!")
    else:
        print("Warning: Tried logging out while no session was active.")

    return 0

def session_active():
    if (session_is_logged == "true"):
        return 1
    else:
        return 0

def session_timeout_tick():
    global n

    if (session_active()):
        n += 1

    if (n==session_timeout):
        loguser(session_user_logged)
        print("SESSION TIMEOUT")
        n=0
    return 0

def session_timeout_reset():
    global n
    n=0
    return 0

### EQUIPMENT LOGGING

def check_out(eqpid):
	
    print(eqp_available(eqpid))
    webhook = url + "?value1=" + who_is(session_user_logged) + "&value2=" + eqp_what_is(eqpid) + " (" + eqpid + ")" + "&value3=" + "I/O"
    #https://maker.ifttt.com/trigger/fitv_equip_log/with/key/bw9CXnOD2nsTte7e7ZL2NW?value1=testuser&value2=testeqp&value3=io
    webhook_parsed = webhook.replace(' ', '%20')
    print("Hailing " + webhook_parsed)
    f = urllib.request.urlopen(webhook_parsed)
    print(f.read().decode('utf-8'))
    msg_intro.value = "Checked out:"
    msg_intro2.value = eqp_what_is(eqpid)
    pic.value = "eqp/" + eqpid + ".png"

    return 0

### IDENTIFY SCANNED CODE

def what_is(val1):
	
    id_type=""

    if (len(val1) == 16):
        id_type="usr-raw"
    elif (len(val1) == 9 and val1[:2] == "90"):
        id_type="usr"
    elif (len(val1) == 5 and not val1[:2] == "90"):
        id_type="eqp"
    else:
        if ("$" in val1):
            id_type="cmd"

    return id_type

### FETCH USER DATA ###
def who_is(val):
	with open('db/userlist.csv', newline='') as csvfile:
		usrd = csv.reader(csvfile)
		for row in usrd:
			x = ','.join(row)
			if str(val) in x:
				return x[10:]

def get_id(username):
	with open('db/userlist.csv', newline='') as csvfile:
		usrd = csv.reader(csvfile)
		for row in usrd:
			x = ','.join(row)
			if str(username) in x:
				return x[:9]

### EQUIPMENT IDENTIFIERS ###				
def eqp_what_is(id):
	with open('db/inventory.csv', newline='') as csvfile:
		eqprd = csv.reader(csvfile)
		for row in eqprd:
			x = ','.join(row)
			if str(id) in x:
				y = len(x)-20
				return x[28:y]
				
def eqp_exists(id):
    with open('db/inventory.csv', newline='') as csvfile:
        eqprd = csv.reader(csvfile)
        for row in eqprd:
            x = ','.join(row)
            if str(id) in x:
                return 1
        return 0

def eqp_available(id):
    with open('db/inventory.csv', newline='') as csvfile:
        eqprd = csv.reader(csvfile)
        for row in eqprd:
            x = ','.join(row)
            if str(id) in x:
                if (x[8:17] == "#########"):
                    return 1
        return 0

### CONVERT AND PARSE
def get_fit_id(rawid):
	
	if (len(rawid) == 16):
		fitid = rawid[6:15]
	elif (len(rawid) == 9):
		fitid = rawid
	
	return fitid

### RUN COMMANDS
def execute(cmd):
    if (cmd == "$ext"):
        sys.exit(0)

    return 0


### PYTHON3 BS
if __name__ == '__main__':
	main()

