import os
import shutil
import sys
import subprocess
import psutil
import tempfile
import ctypes

# Dictionary of console names and folder names for Garlic OS
garlic_os_folders = {
    "Amiga": "AMIGA",
    "AmigaCD32": "AMIGACD",
    "Arcade": "ARCADE",
    "Atari2600": "ATARI",
    "Atari5200": "ATARIST",
    "Atari7800": "EIGHTHUNDRED",
    "AtariJaguar": "JAGUAR",
    "AtariLynx": "LYNX",
    "Commodore64": "COMMODORE",
    "FBA": "FBA2012",
    "FinalBurnAlpha": "FBNEO",
    "GameBoy": "GB",
    "GameBoyAdvance": "GBA",
    "GameBoyColor": "GBC",
    "GameGear": "GG",
    "Intellivision": "INTELLIVISION",
    "MSX": "MSX",
    "MAME": "MAME",
    "MAME2000": "MAME2000",
    "Megadrive": "MD",
    "NeoGeo": "NEOGEO",
    "NeoGeoPocket": "NGP",
    "NeoGeoPocketColor": "NGPC",
    "NintendoDS": "NDS",
    "Nintendo64": "N64",
    "NintendoEntertainmentSystem": "FC",
    "PCEngine": "PCENGINE",
    "PlayStation": "PS",
    "ScummVM": "SCUMMVM",
    "Sega32X": "SEGASGONE",
    "SegaCD": "SEGACD",
    "SegaGenesis": "SMD",
    "SegaMasterSystem": "SMS",
    "SNES": "SFC",
    "SuperGrafx": "PCEIGHTYEIGHT",
    "SuperNintendoEntertainmentSystem": "SFC",
    "TurboGrafx16": "PCECD",
    "VirtualBoy": "VB",
    "WonderSwan": "WonderSwan",
    "WonderSwanColor": "WS"
}

# Dictionary of console names and folder names for Batocera
batocera_folders = {
    "Amiga": "amiga",
    "Atari2600": "atari2600",
    "Atari5200": "atari5200",
    "Atari7800": "atari7800",
    "AtariJaguar": "atarljaguar",
    "AtariLynx": "atarilynx",
    "Commodore64": "c64",
    "Dreamcast": "dreamcast",
    "FinalBurnAlpha": "fba",
    "GameBoy": "gb",
    "GameBoyAdvance": "gba",
    "GameBoyColor": "gbc",
    "Genesis": "genesis",
    "MAME": "mame",
    "MasterSystem": "mastersystem",
    "MSX": "msx",
    "Nintendo64": "n64",
    "NeoGeo": "neogeo",
    "NintendoEntertainmentSystem": "nes",
    "NeoGeoPocket": "ngp",
    "NeoGeoPocketColor": "ngpc",
    "PCEngine": "pcengine",
    "PlayStation": "psx",
    "ScummVM": "scummvm",
    "Sega32X": "sega32x",
    "SegaCD": "segacd",
    "SNES": "snes",
    "VirtualBoy": "virtualboy",
    "Wii": "wii",
    "WonderSwan": "wonderswan",
    "WonderSwanColor": "wonderswancolor"
}

# Dictionary of OS names and their corresponding folder dictionaries
os_folders = {
    "Garlic": garlic_os_folders,
    "Batocera": batocera_folders,
}

# Global variable for Batocera subdirectories
batocera_subdirs = ["batocera", "userdata", "roms"]


def get_file_inventory(folder):
    """
    Returns the inventory of files and their sizes in a folder.

    Args:
        folder (str): The path to the folder.

    Returns:
        dict: A dictionary with file names as keys and file sizes as values.
    """
    inventory = {}
    for item_name in os.listdir(folder):
        item_path = os.path.join(folder, item_name)
        if os.path.isfile(item_path):
            inventory[item_name] = os.path.getsize(item_path)

    return inventory


def verify_moved_files(inventory, target_folder):
    """
    Verifies if the moved files are in the target folder based on the inventory.

    Args:
        inventory (dict): A dictionary with file names as keys and file sizes as values.
        target_folder (str): The path to the target folder.

    Returns:
        bool: True if all files have been moved, False otherwise.
    """
    for file_name, file_size in inventory.items():
        target_file_path = os.path.join(target_folder, file_name)
        if not os.path.exists(target_file_path) or os.path.getsize(target_file_path) != file_size:
            return False

    return True


def undo_rom_folder_creation(root_folder, os_name):
    """
    Removes the folder tree for all consoles in the specified root folder based on the given OS.

    Args:
        root_folder (str): The path to the root folder where the console folders should be removed.
        os_name (str): The name of the OS (either "Garlic" or "Batocera").

    Returns:
        bool: True if the folders were removed successfully, False otherwise.
        str: A message indicating the result of the folder removal.
    """
    folders_dict = os_folders.get(os_name, {})

    if not folders_dict:
        return False, f"Invalid OS name: {os_name}"

    try:
        if os_name == "Garlic":
            for console_name, folder_name in folders_dict.items():
                console_folder_path = os.path.join(root_folder, folder_name)
                if os.path.exists(console_folder_path):
                    print(f"Removing folder: {console_folder_path}")
                    shutil.rmtree(console_folder_path)
                else:
                    print(f"Folder not found: {console_folder_path}")
        elif os_name == "Batocera":
            batocera_folder = os.path.join(root_folder, "batocera")
            if os.path.exists(batocera_folder):
                print(f"Removing folder: {batocera_folder}")
                shutil.rmtree(batocera_folder)
            else:
                print(f"Folder not found: {batocera_folder}")

        return True, f"Folders for all consoles in {root_folder} have been removed."
    except Exception as e:
        return False, f"Error removing folders: {str(e)}"


def create_rom_folders(root_folder, os_name):
    """
    Creates the folder tree for all consoles in the specified root folder based on the given OS.

    Args:
        root_folder (str): The path to the root folder where the console folders should be created.
        os_name (str): The name of the OS (either "Garlic" or "Batocera").

    Returns:
        bool: True if the folders were created successfully, False otherwise.
        str: A message indicating the result of the folder creation.
    """
    folders_dict = os_folders.get(os_name, {})

    if not folders_dict:
        return False, f"Invalid OS name: {os_name}"

    try:
        if os_name == "Batocera":
            root_folder = os.path.join(root_folder, *batocera_subdirs)

        for console_name, folder_name in folders_dict.items():
            console_folder_path = os.path.join(root_folder, folder_name)
            os.makedirs(console_folder_path, exist_ok=True)

        return True, f"Folders for all consoles in {root_folder} have been created."
    except Exception as e:
        return False, f"Error creating folders: {str(e)}"


def convert_rom_folders(input_dir, target_os):
    """
    Scans the input directory to determine its current OS, creates the target OS folder structure,
    moves ROM files to the new directories, and removes the folders from the previous OS.

    Args:
        input_dir (str): The path to the input directory containing the ROM files.
        target_os (str): The target OS for the new folder structure (e.g., "Garlic", "Batocera").
    """
    # Step 1: Accept an input directory and OS - done through function arguments

    # Step 2: Scan directory to determine what OS it is
    current_os = None
    threshold = 3  # Number of matching folders required for OS detection
    original_input_dir = input_dir
    for os_name, folders_dict in os_folders.items():
        console_folders = list(folders_dict.values())
        if os_name == "Batocera":
            console_folders.append("bios")
            batocera_roms_folder = os.path.join(input_dir, "batocera", "roms")
            if os.path.exists(batocera_roms_folder):
                input_dir = batocera_roms_folder

        matching_folders = [os.path.exists(os.path.join(input_dir, folder_name)) for folder_name in console_folders]
        if sum(matching_folders) >= threshold:
            current_os = os_name
            break

    if not current_os:
        raise ValueError(f"Could not detect folder structure for {input_dir}")

    if current_os == target_os:
        return

    # Backup saves folder for Batocera
    if current_os == "Batocera":
        saves_backup = os.path.join(input_dir, "saves_backup")
        saves_folder = os.path.join(input_dir, "saves")
        if os.path.exists(saves_folder):
            if not os.path.exists(saves_backup):
                os.makedirs(saves_backup)
            for file_name in os.listdir(saves_folder):
                shutil.move(os.path.join(saves_folder, file_name), os.path.join(saves_backup, file_name))

    # Step 3: Create the directories for the input OS
    print(f"Creating folders for {target_os} in {original_input_dir}")
    success, message = create_rom_folders(original_input_dir, target_os)
    if not success:
        raise RuntimeError(message)

    # Step 4: Move files from the current OS to their new directories
    source_folders = os_folders[current_os]
    target_folders = os_folders[target_os]
    all_files_moved = True  # Initialize the variable to track if all files were moved

    for console_name, source_folder_name in source_folders.items():
        source_folder = os.path.join(input_dir, source_folder_name)
        target_folder_name = target_folders.get(console_name)

        if not os.path.exists(source_folder):
            continue

        if target_folder_name:
            parent_input_dir = os.path.dirname(os.path.dirname(input_dir))
            target_folder = os.path.join(parent_input_dir, target_folder_name)
            source_inventory = get_file_inventory(source_folder)

            for item_name in os.listdir(source_folder):
                item_path = os.path.join(source_folder, item_name)
                try:
                    if os.path.isfile(item_path):
                        shutil.move(item_path, os.path.join(target_folder, item_name))
                    elif os.path.isdir(item_path):
                        target_subdir = os.path.join(target_folder, item_name)
                        shutil.move(item_path, target_subdir)
                except FileNotFoundError:
                    print(f"File or directory not found: {item_path}")

            # Verify the files have been moved
            if not verify_moved_files(source_inventory, target_folder):
                print("Error: Some files were not moved successfully.")
                all_files_moved = False  # Update the variable if some files were not moved
                break
        else:
            # If the target OS doesn't have a specific console folder, move the entire folder to the new directory
            parent_input_dir = os.path.dirname(os.path.dirname(input_dir))
            target_folder = os.path.join(parent_input_dir, source_folder_name)
            source_inventory = get_file_inventory(source_folder)

            if not os.path.exists(target_folder):
                shutil.move(source_folder, target_folder)

            # Verify the files have been moved
            if not verify_moved_files(source_inventory, target_folder):
                print("Error: Some files were not moved successfully.")
                all_files_moved = False  # Update the variable if some files were not moved
                break

    # Step 5: Remove the folders from the previous OS
    success, message = undo_rom_folder_creation(original_input_dir, current_os)
    if not success:
        raise RuntimeError(message)
    else:
        print(f"Successfully converted {original_input_dir} to {target_os}")


def get_external_drives():
    drives = []

    for part in psutil.disk_partitions(all=False):
        if sys.platform.startswith("win32"):
            if 'removable' in part.opts:
                drives.append(part.device)
        elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            if part.mountpoint.startswith("/media") or part.mountpoint.startswith("/Volumes"):
                drives.append(part.device)

    return drives


def check_admin_rights():
    """
    Checks if the script has administrative rights.
    :return: True if admin rights, otherwise False
    """
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def format_drive(drive: str, file_system: str):
    if sys.platform.startswith("win"):
        # Use PowerShell for exFAT formatting and diskpart for FAT32 formatting on Windows
        if file_system == "FAT32":
            # Create a temporary diskpart script file
            with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as script_file:
                script_file.write(f"select volume {drive}\n"
                                  "format fs=fat32 quick\n"
                                  "exit\n")
                script_file_path = script_file.name

            # Use diskpart to format the drive
            command = f"diskpart /s {script_file_path}"
        else:
            command = f"powershell.exe Clear-Disk -Number (Get-Disk -Path '\\\\.\\{drive}:').Number -RemoveData -Confirm:$false ; Format-Volume -DriveLetter {drive[0]} -FileSystem exFAT"

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )
    else:
        # Use mkfs for Linux and macOS
        file_system_flag = "fat32" if file_system == "FAT32" else "exfat"
        command = f"sudo mkfs.{file_system_flag} {drive}"

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )

    stdout, stderr = process.communicate()
    print(f"Return code: {process.returncode}")
    print(f"Stdout: {stdout}")
    print(f"Stderr: {stderr}")

    if process.returncode == 0:
        return True, stdout, stderr
    else:
        return False, stdout, stderr



# if __name__ == "__main__":
#     in_dir = "D:\\"
#     t_os = "Garlic"
#
#     try:
#         convert_rom_folders(in_dir, t_os)
#         print(f"Successfully converted {in_dir} to {t_os}")
#     except Exception as e:
#         print(f"Error converting folders: {str(e)}")
