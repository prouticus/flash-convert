import os
import sys
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

def find_exe():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "dist", "flash_convert.exe"),
        os.path.join(script_dir, "flash_convert.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None

def create_key(parent, subkey):
    return winreg.CreateKeyEx(parent, subkey, 0, winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY)

def main():
    if not is_admin():
        print("Requesting administrator privileges...")
        run_as_admin()
        sys.exit(0)

    exe_path = find_exe()
    if exe_path is None:
        print("ERROR: flash_convert.exe not found.")
        print("Run build.bat first to create the executable.")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"Using executable: {exe_path}")

    base = r"SystemFileAssociations\.heic\shell\FlashConvert"

    cmd_store = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell"

    try:
        # Create the parent "Flash Convert" menu entry
        with create_key(winreg.HKEY_CLASSES_ROOT, base) as key:
            winreg.SetValueEx(key, "MUIVerb", 0, winreg.REG_SZ, "Flash HEIC Convert")
            winreg.SetValueEx(key, "SubCommands", 0, winreg.REG_SZ,
                              "FlashConvert.ToPNG;FlashConvert.ToJPG")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f"{exe_path},0")

        # Register "to PNG" in the CommandStore
        with create_key(winreg.HKEY_LOCAL_MACHINE, cmd_store + r"\FlashConvert.ToPNG") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "to PNG")
        with create_key(winreg.HKEY_LOCAL_MACHINE, cmd_store + r"\FlashConvert.ToPNG\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{exe_path}" "%1" png')

        # Register "to JPG" in the CommandStore
        with create_key(winreg.HKEY_LOCAL_MACHINE, cmd_store + r"\FlashConvert.ToJPG") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "to JPG")
        with create_key(winreg.HKEY_LOCAL_MACHINE, cmd_store + r"\FlashConvert.ToJPG\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{exe_path}" "%1" jpg')

        print("Context menu installed successfully!")
        print("Right-click a .heic file -> Show more options -> Flash HEIC Convert")

    except PermissionError:
        print("ERROR: Permission denied. Please run as Administrator.")
    except Exception as e:
        print(f"ERROR: {e}")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
