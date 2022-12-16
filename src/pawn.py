import datetime
import platform
import sys

filename = sys.argv[1]
dev = False
current_date = datetime.date.today().strftime("%B %d, %Y") + " " + datetime.datetime.now().strftime("%H:%M:%S")

if not dev:
    print(f"PAWN 0.0.1 (main, ALPHA) on {platform.system()} {platform.release()}, shell session started at {current_date}")
    print(f"Type 'help()' for help")
    while True:
        text = input(">>>")
