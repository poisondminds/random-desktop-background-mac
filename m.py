import subprocess
import shutil
import string
import random
import os
import requests
import time
import sys

def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

def clean_dir():
    if os.path.isdir("b"):
        for file in os.listdir("b"):
            os.unlink(os.path.join("b", file))
        os.rmdir("b")

def download_random():
    file_name = ""
    r = requests.get("http://picsum.photos/1280/720/?random", stream=True)
    if r.status_code == 200:
        if not os.path.isdir("b"):
            os.mkdir("b")
        with open("b/{}.jpg".format(random_string(5)), 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            file_name = f.name

    return file_name

def set_desktop_background(filename):
    SCRIPT = """/usr/bin/osascript<<END
    tell application "Finder"
    set desktop picture to POSIX file "%s"
    end tell
    END"""

    subprocess.Popen(SCRIPT%filename, shell=True)

PERIOD_SECONDS_DEFAULT = 30

try:
    period_seconds = int(sys.argv[1])
except:
    period_seconds = PERIOD_SECONDS_DEFAULT

while True:
    file_name = download_random()
    abs_path = os.path.abspath(file_name)
    set_desktop_background(abs_path)
    time.sleep(1)
    clean_dir()
    time.sleep(period_seconds)
