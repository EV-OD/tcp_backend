import tkinter as tk
from tkinter import scrolledtext
import psutil
from datetime import datetime
import winreg


    



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

class ProcessTreeViewApp:
    def __init__(self, master,pid):
        self.master = master
        master.title("Process Tree Viewer")

        # Left column
        left_frame = tk.Frame(master, width=100)
        left_frame.pack(side=tk.LEFT, fill='y')

        # Main column (process tree view)
        main_frame = tk.Frame(master)
        main_frame.pack(side=tk.LEFT, expand=True, fill='both')

        self.text_area = scrolledtext.ScrolledText(left_frame, width=50, height=20)
        self.text_area.pack(expand=True, fill='both')

        self.text_area2 = scrolledtext.ScrolledText(main_frame, width=50, height=20)
        self.text_area2.pack(expand=True, fill='both')

        

        # Right column
        right_frame = tk.Frame(master, width=100)
        right_frame.pack(side=tk.LEFT, fill='y')

        self.text_area3 = scrolledtext.ScrolledText(right_frame, width=50, height=20)
        self.text_area3.pack(expand=True, fill='both')

        update_button = tk.Button(left_frame, text="Kill Process", command=self.kill_process_by_pid(pid))
        update_button.pack(pady=10)
        update_button2 = tk.Button(left_frame, text="Fake Flag")
        update_button2.pack(pady=10)
        # Replace this with the desired process ID
        self.target_process_id = pid  # Change to your specific process ID

        self.processNames =  [ ]
        self.process_counts = {
            'cmd.exe': set(),
            'powershell.exe': set(),
            'conhost.exe': set(),
            'wmiprvse.exe': set(),
            'svchost.exe': set(),
            'explorer.exe': set(),
            'lsass.exe': set(),
            'csrss.exe': set(),
            'winlogon.exe': set(),
            'services.exe': set()
        }

        self.update_process_tree()
        self.redg_change()
        self.tcp_connections_made()
    def kill_process_by_pid(self,pid):
        def haha():
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
        return haha
            
    def increase_process_count(self, process_name,pid):
        if process_name in self.process_counts:
            self.process_counts[process_name].add(pid)

    def update_process_tree(self):
        try:
            process = psutil.Process(self.target_process_id)
            self.text_area.delete('1.0', tk.END)
            parent_processes = get_all_parent_processes(self.target_process_id)

            process_info = self.get_process_info()
            self.text_area.insert(tk.END, process_info,'count')

            self.text_area.tag_config('parent', background="#112ebf", foreground="white")
            self.text_area.tag_config('child', background="#1199bf", foreground="white")
            self.text_area.tag_config('count', background="#bf116e", foreground="white")


            if parent_processes:

                for i, process in enumerate(parent_processes[::-1], start=1):
                    process_name = process.name()
                    process_id = process.pid
                    process_info = {"pid": process_id, "processName": process_name, "path": process.exe()}
                    self.text_area.insert(tk.END, f"Parent Process: {i}. {process_name} (PID: {process_id})\n", 'parent')
                    self.increase_process_count(process_name, process_id)
                    if process_name not in (entry.get("processName") for entry in self.processNames):
                        self.processNames.append(process_info)

            else:
                print(f"No parent processes found for PID {self.target_process_id}")

            # Get children processes (subprocesses)
            children = process.children(recursive=True)

            for child in children:
                child_name = child.name()
                child_id = child.pid
                child_exe = child.exe()

                child_info = {
                    "pid": child_id,
                    "processName": child_name,
                    "path": child_exe,
                    
                }
                self.text_area.insert(tk.END, f"Child Process: {child_name} (PID: {child_id})\n", 'child')
                self.increase_process_count(child_name, child_id)
                if child_name not in (entry.get("processName") for entry in self.processNames):
                    self.processNames.append(child_info)

            

            # Schedule the next update after 0.1 seconds
          
            self.master.after(100, self.update_process_tree)

        except psutil.NoSuchProcess:
            self.text_area.insert(tk.END, f"No process found with PID: {self.target_process_id}")
        except Exception as e:
            self.text_area.insert(tk.END, f"An error occurred: {e}")

    def get_process_info(self):
        process_info = f"\nProcess Counts:\n"
        for process_name, ids in self.process_counts.items():
            if len(ids) > 0:
                process_info += f"{process_name}: {len(ids)}\n"
        return process_info
    
    def redg_change(self):
        suspicious_keys = [
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnceEx",
        r"System\CurrentControlSet\Services",]

        for key_path in suspicious_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
                
                try:
                    index = 0
                    while True:
                        name, value, _ = winreg.EnumValue(key, index)
                        # print(f"  Found: {name} = {value}")
                        index += 1
                        for entry in self.processNames:
                            value=str(value.split("--")[0]).strip()
                            path=str(entry.get("path")).strip()
                            if value == path :
                                self.text_area2.insert(tk.END, f"Redg Found for {value} in {key_path}")

                except FileNotFoundError:
                    pass  # No more values

            except FileNotFoundError:
                # print(f"{key_path} not found.")
                ...

            except Exception as e:
                # print(f"Error accessing {key_path}: {e}")
                ...

            print("\n")

    def tcp_connections_made(self):
        for entry in self.processNames:
            process_pid = entry.get("pid")
            if process_pid is not None:
                try:
                    process = psutil.Process(process_pid)
                    connections = process.connections(kind="inet")
                    
                    if connections:
                        for conn in connections:
                            try:
                                 if conn.raddr.ip:
                                     self.text_area3.insert(tk.END, f"{entry.get('processName')}(PID: {process_pid}) : {conn.raddr.ip} \n")
                            except Exception:
                                pass


                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                    print(f"Error accessing process with PID {process_pid}: {e}")


    



if __name__ == "__main__":
    root = tk.Tk()
    pid=9320
    app = ProcessTreeViewApp(root,pid)
    root.mainloop()
