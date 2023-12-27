import psutil
import time
from pprint import pprint
from database import Ip,Session
session=Session()
import requests
from plyer import notification
import json

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,  
        timeout=10, 
    )

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
    url = "http://127.0.0.1:100/check_ip"  # Replace with your server URL
    data = {"ip": ip}

    try:
        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(data)
        response = requests.post(url, data=json_data,headers=headers)

        if response.status_code == 200:
            response_text = str(response.text)
            if response_text.lower() == 'true':
                return True
            elif response_text.lower() == 'false':
                print("here")
                ip = Ip(ip_address=ip, checked=True)
                session.add(ip)
                session.commit()
                return False
        else:
            print(f"Failed to send IP {ip} to server. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"Error sending IP to server: {e}")


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
                                break
                        else:
                            response=check_ip(conn.raddr.ip) 
                        if response==True:
                            # show_notification(f"Flagged IP Detected in {process_name}", "Hehe")
                            view_subprocesses_of_pid(conn.pid)
                        
                except Exception:
                    pass

    session.close()

if __name__ == "__main__":
    main()