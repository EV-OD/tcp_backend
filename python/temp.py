from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class RegistryChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Registry Change Detected: {event.src_path}")

def monitor_registry_changes():
    path_to_monitor = r"C:\Path\To\Registry\Key"
    event_handler = RegistryChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_monitor, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Example: Monitor changes to the registry key "HKEY_LOCAL_MACHINE\SOFTWARE"
monitor_registry_changes()
