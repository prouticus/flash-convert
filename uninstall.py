import sys
import os
import ctypes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1
    )

def delete_key_tree(root, path):
    try:
        with winreg.OpenKeyEx(root, path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, 0)
                    delete_key_tree(root, f"{path}\\{subkey_name}")
                except OSError:
                    break
        winreg.DeleteKey(root, path)
    except FileNotFoundError:
        pass

def main():
    if not is_admin():
        print("Requesting administrator privileges...")
        run_as_admin()
        sys.exit(0)

    base = r"SystemFileAssociations\.heic\shell\FlashConvert"

    cmd_store = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell"

    try:
        delete_key_tree(winreg.HKEY_CLASSES_ROOT, base)
        delete_key_tree(winreg.HKEY_LOCAL_MACHINE, cmd_store + r"\FlashConvert.ToPNG")
        delete_key_tree(winreg.HKEY_LOCAL_MACHINE, cmd_store + r"\FlashConvert.ToJPG")
        print("Context menu uninstalled successfully!")
    except Exception as e:
        print(f"ERROR: {e}")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
