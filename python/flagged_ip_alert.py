import psutil
import time
from pprint import pprint
from database import Ip,Session
session=Session()
import requests
import json
import tkinter as tk
from process_tree import ProcessTreeViewApp

from win10toast_click import ToastNotifier


    

def process_tree(pid):
    def gg():
        root = tk.Tk()
        app = ProcessTreeViewApp(root,pid)
        root.mainloop()
    return gg

def view_subprocesses_of_pid(parent_pid):
    try:
        parent_process = psutil.Process(parent_pid)
        subprocesses = parent_process.children(recursive=True)

        print(f"Subprocesses of PID {parent_pid}:")
        for subprocess in subprocesses:
            print(f"PID: {subprocess.pid}, Name: {subprocess.name()}")

    except psutil.NoSuchProcess:
        print(f"Process with PID {parent_pid} not found.")

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

def kill_process_by_pid(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()  # Send a termination signal
        process.wait(timeout=5)  # Wait for the process to terminate (optional)
        print(f"Process with PID {pid} terminated successfully.")
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}.")
    except psutil.AccessDenied:
        print(f"Access denied to terminate process with PID {pid}.")
    except Exception as e:
        print(f"Error terminating process with PID {pid}: {e}")

def main():
    
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
                            response=check_ip(conn.raddr.ip) 
                        if response==True:
                            toaster = ToastNotifier() 
                            toaster.show_toast(title=f"Moye Moye with {process_name}",duration=2,threaded=True,callback_on_click=process_tree(conn.pid) )
                            kill_process_by_pid(conn.pid)
                            view_subprocesses_of_pid(conn.pid)
                        
                except Exception:
                    pass

    session.close()

if __name__ == "__main__":
    main()