import winreg

def check_malicious_registry_keys():
    suspicious_keys = [
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"Software\Microsoft\Windows\CurrentVersion\RunOnceEx",
    r"System\CurrentControlSet\Services",
    
    # Add more suspicious keys as needed
]

    for key_path in suspicious_keys:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            print(f"Checking {key_path} for suspicious entries:")
            
            try:
                index = 0
                while True:
                    name, value, _ = winreg.EnumValue(key, index)
                    print(f"  Found: {name} = {value}")
                    index += 1
            except FileNotFoundError:
                pass  # No more values

        except FileNotFoundError:
            print(f"{key_path} not found.")

        except Exception as e:
            print(f"Error accessing {key_path}: {e}")

        print("\n")

if __name__ == "__main__":
    check_malicious_registry_keys()
