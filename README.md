# pilog

Equipment check-out station for FITV (Florida Tech Video Productions), where I was Director of Technical Services. A Raspberry Pi with a 480 × 320 touchscreen and a barcode scanner ran it at the equipment room door.

## How it works
1. A member scans their Florida Tech ID card (raw card or 9-digit ID) to start a session; their name and photo come up.
2. They scan each item's barcode to sign it in or out. Each movement is posted to an IFTTT webhook with who and what.
3. Scanning the ID again ends the session; an idle session signs itself out after four minutes.

Members and gear live in two CSV files (`db/userlist.csv`, `db/inventory.csv`), with photos in `usr/` and `eqp/`. Barcodes containing `$` are admin commands (`$ext` closes the app).

## Run
Python 3 with [guizero](https://lawsie.github.io/guizero/). Set the webhook URL in the `PILOG_WEBHOOK` environment variable, then `./start.sh`. The app expects to live in `/home/pi/pilog/` and runs fullscreen.

Status: alpha, January 2018; in use at FITV. Not maintained.
