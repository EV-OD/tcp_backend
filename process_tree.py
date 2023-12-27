import tkinter as tk
from tkinter import scrolledtext
import psutil
from datetime import datetime

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

        self.text_area = scrolledtext.ScrolledText(master, width=50, height=20)
        self.text_area.pack(expand=True, fill='both')

        # Replace this with the desired process ID
        self.target_process_id = pid  # Change to your specific process ID

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
                print(f"Parent processes for PID {self.target_process_id}:")

                for i, process in enumerate(parent_processes[::-1], start=1):
                    self.text_area.insert(tk.END, f"Parent Process: {i}. {process.name()} (PID: {process.pid})\n", 'parent')
                    self.increase_process_count(process.name(),process.pid)

            else:
                print(f"No parent processes found for PID {self.target_process_id}")

            # Get children processes (subprocesses)
            children = process.children(recursive=True)

            for child in children:
                self.text_area.insert(tk.END, f"Child Process: {child.name()} (PID: {child.pid})\n", 'child')
                # Increase the count for the child process
                self.increase_process_count(child.name(),child.pid)

            # Update the process counts in the label
            

            # Schedule the next update after 5 seconds
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


if __name__ == "__main__":
    root = tk.Tk()
    pid=4024
    app = ProcessTreeViewApp(root,pid)
    root.mainloop()
