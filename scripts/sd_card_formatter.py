import os
import shutil

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
        for console_name, folder_name in folders_dict.items():
            console_folder_path = os.path.join(root_folder, folder_name)
            if os.path.exists(console_folder_path):
                print(f"Removing folder: {console_folder_path}")
                shutil.rmtree(console_folder_path)
            else:
                print(f"Folder not found: {console_folder_path}")

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

    for console_name, source_folder_name in source_folders.items():
        source_folder = os.path.join(input_dir, source_folder_name)
        target_folder_name = target_folders.get(console_name)

        if not os.path.exists(source_folder):
            continue

        if target_folder_name:
            parent_input_dir = os.path.dirname(os.path.dirname(input_dir))
            target_folder = os.path.join(parent_input_dir, target_folder_name)
            for file_name in os.listdir(source_folder):
                file_path = os.path.join(source_folder, file_name)
                if os.path.isfile(file_path):
                    try:
                        shutil.move(file_path, os.path.join(target_folder, file_name))
                    except FileNotFoundError:
                        print(f"File not found: {file_path}")
        else:
            # If the target OS doesn't have a specific console folder, copy the entire folder to the new directory
            parent_input_dir = os.path.dirname(os.path.dirname(input_dir))
            target_folder = os.path.join(parent_input_dir, source_folder_name)
            if not os.path.exists(target_folder):
                shutil.copytree(source_folder, target_folder)

    # Step 5: Remove the folders from the previous OS
    success, message = undo_rom_folder_creation(input_dir, current_os)
    if not success:
        raise RuntimeError(message)




if __name__ == "__main__":
    input_dir = "H:\Games\Convert SD Card Content\\"
    target_os = "Garlic"

    try:
        convert_rom_folders(input_dir, target_os)
        print(f"Successfully converted {input_dir} to {target_os}")
    except Exception as e:
        print(f"Error converting folders: {str(e)}")
