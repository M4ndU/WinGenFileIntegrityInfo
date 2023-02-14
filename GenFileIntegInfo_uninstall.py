import winreg
import sys
import ctypes
import os
import tkinter as tk
from tkinter import messagebox

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
root = tk.Tk()
root.withdraw()

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

if ctypes.windll.shell32.IsUserAnAdmin():
    pass
else:
    messagebox.showinfo("Title", "Not running as administrator. exit()")
    exit()
#---------------------------------------------------------------------

import shutil

# Define the path to the folder to delete
folder_path = r"C:\Program Files\M4ndU"

# Check if the folder exists and delete it if it does
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
    print(f"Deleted folder {folder_path}")
else:
    print(f"Folder {folder_path} does not exist")

#---------------------------------------------------------------------

file_extension = "*"
menu_text_sha1 = "Copy FileInfo with MD5+SHA1 to clipboard"
menu_text_sha2 = "Copy FileInfo with SHA256 to clipboard"

if check_context_menu_entry(file_extension, menu_text_sha1):
    print(f"Context menu entry for {file_extension} with text '{menu_text_sha1}' already exists")
    delete_context_menu_entry(file_extension, menu_text_sha1)

if check_context_menu_entry(file_extension, menu_text_sha2):
    print(f"Context menu entry for {file_extension} with text '{menu_text_sha2}' already exists")
    delete_context_menu_entry(file_extension, menu_text_sha2)

messagebox.showinfo("Uninstall complete", "Uninstall complete")
