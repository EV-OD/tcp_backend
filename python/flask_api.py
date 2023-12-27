from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import threading
import time
import base64
import os
import ctypes
import string
import random
import os
import pystray
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

default_logo="../assets/default_logo.png"

# Initialize process_data and a lock to synchronize access
process_data = []
data_lock = threading.Lock()


def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())
            # print(encoded_image.decode('utf-8'))
            return encoded_image.decode('utf-8')
    except FileNotFoundError:
        return f"File not found: {image_path}"
    except Exception as e:
        return f"Error converting image to base64: {e}"
    
def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def extract_icon_from_exe(icon_in_path, icon_name=generate_random_string, icon_out_path="C://Enigma//assets", out_width = 56, out_height = 56):

    """Given an icon path (exe file) extract it and output at the desired width/height as a png image.

    Args:
        icon_in_path (string): path to the exe to extract the icon from
        icon_name (string): name of the icon so we can save it out with the correct name
        icon_out_path (string): final destination (FOLDER) - Gets combined with icon_name for full icon_path
        out_width (int, optional): desired icon width
        out_height (int, optional): desired icon height

    Returns:
        string: path to the final icon
    """
    import win32ui
    import win32gui
    import win32con
    import win32api
    from PIL import Image

    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

    large, small = win32gui.ExtractIconEx(icon_in_path,0)
    win32gui.DestroyIcon(small[0])

    hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_x )
    hdc = hdc.CreateCompatibleDC()

    hdc.SelectObject( hbmp )    
    hdc.DrawIcon( (0,0), large[0] )

    bmpstr = hbmp.GetBitmapBits(True)
    icon = Image.frombuffer(
        'RGBA',
        (32,32),
        bmpstr, 'raw', 'BGRA', 0, 1
    )

    full_outpath = os.path.join(icon_out_path, "{}.png".format(icon_name))
    icon.resize((out_width, out_height))
    icon.save(full_outpath)
    #return the final path to the image
    return full_outpath

def extract_icon_to_base64(exe_path):
    try:
        # Ensure the file path is not None
        if not exe_path or not os.path.exists(exe_path):
            return f"Error: Invalid file path: {exe_path}"

        # Use pystray to load the icon
        icon = pystray.Icon("test_icon", Image.open(exe_path))

        # Convert the icon to base64
        icon_bytes_io = io.BytesIO()
        icon.icon.save(icon_bytes_io, format="PNG")
        icon_base64 = base64.b64encode(icon_bytes_io.getvalue()).decode("utf-8")
        return icon_base64

    except Exception as e:
        print(f"Error extracting icon: {e}")
        return image_to_base64(default_logo)
    
# def extract_icon_from_exe(exe_path):
    
    try:
        if not exe_path or not os.path.exists(exe_path):
            print(f"Error: Invalid file path: {exe_path}")
        # Get the icon handle
        icon_handle = ctypes.windll.shell32.ExtractAssociatedIconW(None, exe_path)

        # Get information about the icon
        icon_info = ctypes.create_string_buffer(260)  # Buffer size for the icon information
        ctypes.windll.shell32.SHGetPathFromIDListW(icon_handle, icon_info)

        # Save the icon as an image file
        icon_path = icon_info.value.decode("utf-16")
        icon_path = icon_path.rstrip("\x00")  # Remove null characters at the end
        icon_path = os.path.splitext(icon_path)[0] + ".ico"  # Change the extension to .ico

        with open(icon_path, "wb") as icon_file:
            ctypes.windll.shell32.DestroyIcon(icon_handle)  # Cleanup the icon handle
            icon_file.write(ctypes.string_at(icon_handle, -1))

        return icon_path

    except Exception as e:
        print(f"Error extracting icon: {e}")
        return default_logo
    
    
def get_process_info(process, is_root=True):
    try:
        process_info = {
            "pid": process.pid,
            "process_name": process.name(),
            "path": process.exe(),
            "logo_path": extract_icon_to_base64(extract_icon_from_exe(process.exe())),  # Update with the correct path
            "isRunning": str(process.is_running())
        }
    except psutil.AccessDenied as e:
        process_info = {
            "pid": process.pid,
            "process_name": process.name(),
            "path":"denied",
            "logo_path": "default",  # Update with the correct path
            "isRunning": str(process.is_running())
        }


    if is_root:
        process_info["sub_process"] = get_sub_processes(process)

    return process_info

def get_sub_processes(parent_process):
    sub_processes = []
    for child in parent_process.children():
        sub_process_info = get_process_info(child, is_root=False)
        sub_processes.append(sub_process_info)
    return sub_processes

def update_process_data():
    global process_data
    while True:
        updated_data = []
        for process in psutil.process_iter(['pid', 'name']):
            process_info = get_process_info(process)
            updated_data.append(process_info)

        # Acquire the lock before updating process_data
        with data_lock:
            process_data = updated_data

        time.sleep(5)  # Update every 5 seconds

@app.route('/api/processes', methods=['GET'])
def get_processes():
    # Acquire the lock before accessing process_data
    with data_lock:
        return jsonify(process_data)

if __name__ == '__main__':
    update_thread = threading.Thread(target=update_process_data)
    update_thread.daemon = True  # Daemonize the thread to stop when the main process stops
    update_thread.start()

    app.run(debug=True)
