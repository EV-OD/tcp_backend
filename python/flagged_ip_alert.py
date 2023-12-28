import psutil
import time
from pprint import pprint
from database import Ip,Session
session=Session()
import requests
import json
import tkinter as tk
from process_tree import ProcessTreeViewApp
import threading
from win10toast_click import ToastNotifier
import signal
import hashlib

class ResettableStorage:
    def __init__(self):
        self.data = set()
        self.reset_interval = 120  # 2 minutes in seconds
        self.reset_timer = threading.Timer(self.reset_interval, self.reset_storage)
        self.reset_timer.start()

    def reset_storage(self):
        self.data = set()
        print("Storage reset.")
        self.reset_timer = threading.Timer(self.reset_interval, self.reset_storage)
        self.reset_timer.start()

    def add_data(self, value):
        self.data.add(value)

    def check_data(self, value):
        if value in self.data:
            return False
        return True
    

def hash_string(input_string):
    # Create a new SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes representation of the input string
    sha256_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_string = sha256_hash.hexdigest()

    return hashed_string

def process_tree(pid):
    def gg():
        root = tk.Tk()
        app = ProcessTreeViewApp(root,pid)
        root.mainloop()
    return gg

# Signal handler to stop threads on Ctrl+C
def signal_handler(storage):
    def lol(sig,frame):
        print("Ctrl+C pressed. Stopping threads.")
        storage.reset_timer.cancel()
        # Add more cleanup if needed
        exit(0)
    return lol


def get_process_name_by_pid(pid):
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return "Non-existent process"
    except psutil.AccessDenied:
        return "Access denied"
    except psutil.ZombieProcess:
        return "Zombie process"
    except Exception as e:
        return f"Unknown error: {e}"

def check_ip(ip):
    url = "http://127.0.0.1:8000/checkip/"  # Replace with your server URL
    data = {"ip": ip}

    try:
        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(data)
        response = requests.post(url, data=json_data,headers=headers)

        if response.status_code == 200:
            response_text = str(response.text)
            if response_text.lower() == 'true':
                print("Panic")
                return True
            elif response_text.lower() == 'false':
                ip = Ip(ip_address=ip, checked=True)
                session.add(ip)
                session.commit()
                return False
        else:
            print(f"Failed to send IP {ip} to server. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"Error sending IP to server: {e}")



def main():
    storage = ResettableStorage()
    signal.signal(signal.SIGINT, signal_handler(storage))

    while True:
        ips = session.query(Ip).all()
        connections = psutil.net_connections(kind="all")
        # pprint(connections)
        for conn in connections :
            if conn.status == 'ESTABLISHED' or conn.status == 'LISTEN':
                try:
                    if conn.raddr.ip != "127.0.0.1":
                        process_name=get_process_name_by_pid(conn.pid)
                        for ip in ips:
                            if ip.ip_address == conn.raddr.ip:
                                response=False
                                break
                        else:
                            response=check_ip(hash_string(conn.raddr.ip)) 
                        if response==True:
                            
                            # Add data to the storage
                            if storage.check_data(conn.pid):
                                storage.add_data(conn.pid)
                                toaster = ToastNotifier() 
                                toaster.show_toast(title=f"Moye Moye with {process_name}",duration=2,threaded=True,callback_on_click=process_tree(conn.pid) )
                            # view_subprocesses_of_pid(conn.pid)
                        
                except Exception:
                    pass

    session.close()

if __name__ == "__main__":
    main()