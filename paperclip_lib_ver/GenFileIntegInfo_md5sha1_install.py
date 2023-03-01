import winreg
import sys
import ctypes
import os
import tkinter as tk
from tkinter import messagebox

def add_context_menu_entry(file_extension, menu_text, command):
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_extension)
        winreg.SetValue(key, '', winreg.REG_SZ, menu_text)
        key = winreg.CreateKey(key, 'shell')
        key = winreg.CreateKey(key, menu_text)
        key = winreg.CreateKey(key, 'command')
        winreg.SetValue(key, '', winreg.REG_SZ, command)
    except WindowsError:
        print(f"Failed to add context menu entry for {file_extension}")

def delete_context_menu_entry(file_extension, menu_text):
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_extension + "\\shell\\" + menu_text, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteKey(key, 'command')
        winreg.CloseKey(key)
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_extension + "\\shell", 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteKey(key, menu_text)
        winreg.CloseKey(key)
    except WindowsError as e:
        if e.errno == 2:
            # Entry not found, do nothing
            print(f"Context menu entry for {file_extension} not found, nothing to delete")
        else:
            # Some other error, print the error message
            print(f"Failed to delete context menu entry for {file_extension}: {e}")

def check_context_menu_entry(file_extension, menu_text):
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_extension + "\\shell")
        i = 0
        while True:
            subkey = winreg.EnumKey(key, i)
            if subkey == menu_text:
                winreg.CloseKey(key)
                return True
            i += 1
    except WindowsError:
        pass
    return False

#---------------------------------------------------------------------
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

if ctypes.windll.shell32.IsUserAnAdmin():
    pass
else:
    messagebox.showinfo("Title", "Not running as administrator. exit()")
    exit()

import subprocess

try:
    # Try to import pyperclip
    import pyperclip
except ImportError:
    # If pyperclip is not installed, run pip to install it
    subprocess.check_call(["pip", "install", "pyperclip"])
    import pyperclip
#---------------------------------------------------------------------

codeOfGenFileIntegInfo_py = '''
# -*- coding: utf-8 -*-
import hashlib
import os
import sys
import pyperclip

def get_file_info_md5sha1(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    md5hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    sha1hash = hashlib.sha1(open(file_path, 'rb').read()).hexdigest()
    return (file_name, file_size, md5hash, sha1hash)

def get_file_info_sha256(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    hash_value = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    return (file_name, file_size, hash_value.hexdigest())

file_path = sys.argv[1]
hash_type = sys.argv[2]

if hash_type == '1':
    file_info = get_file_info_md5sha1(file_path)
    info_str = f"파일명: {file_info[0]}\\n파일크기: {file_info[1]} bytes\\nMD5: {file_info[2]}\\nSHA1: {file_info[3]}"
elif hash_type == '2':
    file_info = get_file_info_sha256(file_path)
    info_str = f"파일명: {file_info[0]}\\n파일크기: {file_info[1]} bytes\\nSHA256: {file_info[2]}"
else:
    pass

pyperclip.copy(info_str)
'''

# Create folder if it doesn't exist
folder_path = r"C:\Program Files\M4ndU\GenFileIntegrityInfo"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Created folder {folder_path}")

# Create file in folder
file_path = os.path.join(folder_path, "GenFileIntegInfo.py")
if not os.path.exists(file_path):
    with open(file_path, "w", encoding='utf8') as f:
        f.write(codeOfGenFileIntegInfo_py)
    print(f"Created file {file_path}")
else:
    print(f"File {file_path} already exists")

#---------------------------------------------------------------------

file_extension = "*"
menu_text_sha1 = "Copy FileInfo with MD5+SHA1 to clipboard"
menu_text_sha2 = "Copy FileInfo with SHA256 to clipboard"
command_sha1 = " \"C:\Program Files\M4ndU\GenFileIntegrityInfo\GenFileIntegInfo.py\" \"%1\" 1"
command_sha2 = " \"C:\Program Files\M4ndU\GenFileIntegrityInfo\GenFileIntegInfo.py\" \"%1\" 2"

if check_context_menu_entry(file_extension, menu_text_sha2):
    print(f"Context menu entry for {file_extension} with text '{menu_text_sha2}' already exists")
    delete_context_menu_entry(file_extension, menu_text_sha2)
else:
    print(f"Context menu entry for {file_extension} with text '{menu_text_sha2}' does not exist")

if check_context_menu_entry(file_extension, menu_text_sha1):
    print(f"Context menu entry for {file_extension} with text '{menu_text_sha1}' already exists")
    messagebox.showinfo("Install", "Already Installed")
    exit()
else:
    print(f"Context menu entry for {file_extension} with text '{menu_text_sha1}' does not exist")
    command = sys.executable + command_sha1
    add_context_menu_entry(file_extension, menu_text_sha1, command)

messagebox.showinfo("Install complete", "Install complete")
