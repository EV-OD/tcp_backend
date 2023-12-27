from flask import Flask, jsonify, json
from flask_cors import CORS
import psutil
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def get_all_parent_processes(process_id):
    processes = []
    try:
        process = psutil.Process(process_id)
        while process:
            processes.append(process)
            process = process.parent()
    except psutil.NoSuchProcess:
        print(f"No process found with PID: {process_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return processes


# Initialize process_data and a lock to synchronize access
process_data = []
data_lock = threading.Lock()

def get_valid_remote_ips(pid):
    try:
        process = psutil.Process(pid)
        connections = process.connections()

        valid_remote_ips = set()

        for connection in connections:
            try:
                if connection.status == 'ESTABLISHED' or connection.status == 'LISTEN':
                    if connection.raddr:
                        remote_ip = connection.raddr.ip
                        if remote_ip and remote_ip != "127.0.0.1":
                            valid_remote_ips.add(remote_ip)
            except Exception as e:
                print(f"{e} error aayo bro")
                pass
        return list(valid_remote_ips)

    except psutil.NoSuchProcess as e:
        print(f"Error: Process with PID {pid} not found.")
        return []

def custom_encoder(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, time.struct_time):
        return time.mktime(obj)  # Convert time.struct_time to UNIX timestamp
    return str(obj)

def get_process_info(process: psutil.Process, is_root=True):
    try:
        valid_remote_ips = get_valid_remote_ips(process.pid)

        # Check if the process has valid remote IPs
        if not valid_remote_ips:
            return None

        process_info = {
            "pid": process.pid,
            "process_name": process.name(),
            "path": process.exe(),
            "start": time.mktime(time.localtime(process.create_time())),
            "connection": valid_remote_ips,
            "isRunning": str(process.is_running()),
            "duration":0,
            "parent_process":[]
        }
    except psutil.AccessDenied as e:
        process_info = {
            "pid": process.pid,
            "process_name": process.name(),
            "path": "denied",
            "start": time.mktime(time.localtime(process.create_time())),
            "connection": get_valid_remote_ips(process.pid),
            "isRunning": str(process.is_running()),
            "duration":0,
            "parent_process":[]

        }

    if is_root:
        sub_processes = get_sub_processes(process)
        # Filter only sub-processes that have valid remote IPs
        sub_processes = [sub_process for sub_process in sub_processes if get_process_info(sub_process, is_root=False) is not None]
        process_info["sub_process"] = sub_processes

    return process_info

def get_sub_processes(parent_process):
    sub_processes = []
    for child in parent_process.children():
        sub_process_info = get_process_info(child, is_root=False)
        if sub_process_info is not None:
            sub_processes.append(sub_process_info)
    return sub_processes

def update_process_data():
    global process_data
    while True:
        updated_data = []
        for process in psutil.process_iter(['pid', 'name']):
            process_info = get_process_info(process)
            if process_info is not None:
                updated_data.append(process_info)

        # Acquire the lock before updating process_data
        with data_lock:
            process_data = updated_data

        time.sleep(0.1)  # Update every 0.1 seconds

@app.route('/api/processes', methods=['GET'])
def get_processes():
    # Acquire the lock before accessing process_data
    with data_lock:
        for p in process_data:
            pid = p["pid"]
            process = psutil.Process(pid)

            # Avoid repeating parent processes
            parent_pids = set()
            parent_pids.add(pid)
            parent_process = get_all_parent_processes(pid)
            for parent in parent_process:
                if parent.pid not in parent_pids:
                    parent_pids.add(parent.pid)
                    p["parent_process"].append({
                        "pid": parent.pid,
                        "process_name": parent.name(),
                        "path": "denied",
                        "start": time.mktime(time.localtime(parent.create_time())),
                        "connection": get_valid_remote_ips(parent.pid),
                        "isRunning": str(parent.is_running()),
                        "duration": 0  # You may need to calculate the duration based on your requirements
                    })
            children_pids=set()
            children_pids.add(pid)
            children = process.children(recursive=True)
            for child in children:
                if child.pid not in children_pids:
                    children_pids.add(child.pid)
                    p["sub_process"].append({
                        "pid": child.pid,
                        "process_name": child.name(),
                        "path": "denied",
                        "start": time.mktime(time.localtime(child.create_time())),
                        "connection": get_valid_remote_ips(child.pid),
                        "isRunning": str(child.is_running()),
                        "duration": 0  # You may need to calculate the duration based on your requirements
                    })

        return jsonify(json.loads(json.dumps(process_data, default=custom_encoder)))

if __name__ == '__main__':
    update_thread = threading.Thread(target=update_process_data)
    update_thread.daemon = True  # Daemonize the thread to stop when the main process stops
    update_thread.start()

    app.run(debug=True)
