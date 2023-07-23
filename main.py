import logging
import webbrowser
from time import sleep
import datetime
import tkinter as tk
from tkinter import ttk
import threading
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = tk.Tk()
root.title("NeverJB Auto Reconnect")
root.configure(bg="black")
root.state("zoomed")

webbrowser.open_new("https://neverjailbreak.com")

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.WARNING,
                    datefmt='%Y-%m-%d %H:%M:%S')

log_path = "C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/console.log"
server_ip = "185.193.165.74"
server_pwd = ""
timeout_msg = "Server connection timed out."
dc_msg = "Disconnect:"
sleep_sec = 1

start_time = datetime.datetime.now()
message_count = 0

calistir = 0

def kapat():
    global calistir
    calistir = 0
    kapat_button.config(state=tk.DISABLED)
    ac_button.config(state=tk.NORMAL)

def ac():
    global calistir
    calistir = 1
    ac_button.config(state=tk.DISABLED)
    kapat_button.config(state=tk.NORMAL)
    t1 = threading.Thread(target=program)
    t1.start()
    t2 = threading.Thread(target=program2)
    t2.start()

def scan():
    logging.info("Scanning " + log_path)
    f = open(log_path,"r", encoding='utf-8', errors='ignore')
    if f.mode == 'r':
        lines = f.readlines()
        for x in lines:
            if x.startswith(dc_msg) or x == x.startswith(timeout_msg):
                f.close()
                logging.info("Found DC message!")
                connect_to_ip()
                open(log_path, 'w').close()
                return True

        f.close()
        return False

def check_last_line():
    global message_count
    with open(log_path, "r", encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            if last_line == "[PROOYUN.NET] - Top10sure ekleme yapildi!":
                message_count += 1

def connect_to_ip():
    logging.info("Connecting to {ip} with password {pwd}...".format(ip=server_ip, pwd=server_pwd))
    webbrowser.open_new("steam://connect/{ip}/{pwd}".format(ip=server_ip, pwd=server_pwd))

def program():
    global start_time
    global message_count
    while calistir == 1:
        elapsed_time = datetime.datetime.now() - start_time
        if elapsed_time.total_seconds() >= 180:
            if message_count == 0:
                connect_to_ip()
            start_time = datetime.datetime.now()
            message_count = 0
        check_last_line()
        sleep(sleep_sec)

def program2():
    while calistir == 1:
        scan()
        sleep(sleep_sec)


logo = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo, bg="black")
logo_label.pack(fill="both", expand=True)

photo = tk.PhotoImage(file="logo.png")
root.wm_iconphoto(False, photo)
root.iconphoto(True, photo)


button_frame = tk.Frame(root, bg="black")
button_frame.pack(pady=10)

kapat_button = tk.Button(button_frame, text="Kapat", command=kapat, state=tk.DISABLED, bg="white", fg="black",
                         font=("Arial", 12))
kapat_button.pack(side=tk.LEFT, padx=10, fill="x", expand=True)

ac_button = tk.Button(button_frame, text="Aç", command=ac, bg="white", fg="black", font=("Arial", 12))
ac_button.pack(side=tk.RIGHT, padx=10, fill="x", expand=True)

# Titlenın sol tarafındaki metni değiştirme
style = ttk.Style()
style.configure("TFrame", foreground="white", background="black")
style.configure("TLabel", foreground="white", background="black", font=("Arial", 16, "bold"))
ttk.Label(root, text="NeverJB Auto Reconnect", style="TLabel").pack(side=tk.TOP, pady=10)

root.mainloop()
