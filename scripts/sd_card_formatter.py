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
    "NintendoEntertainmentSystem": "NES",
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


def undo_rom_folder_creation(root_folder, os_name):
    """
    Deletes all console folders in the specified root folder.

    Args:
        root_folder (str): The path to the root folder where the console folders should be deleted.
        os_name (str): The name of the OS (either "Garlic" or "Batocera").

    Returns:
        bool: True if the folders were deleted successfully, False otherwise.
        str: A message indicating the result of the deletion.
    """
    folders_dict = os_folders.get(os_name, {})
    try:
        for console_name, folder_name in folders_dict.items():
            folder_path = os.path.join(root_folder, folder_name)
            shutil.rmtree(folder_path)

        return True, f"Folders for all consoles in {root_folder} have been deleted."
    except Exception as e:
        return False, f"Error deleting folders: {str(e)}"


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
            root_folder = os.path.join(root_folder, "userdata", "roms")

        for console_name, folder_name in folders_dict.items():
            console_folder_path = os.path.join(root_folder, folder_name)
            os.makedirs(console_folder_path, exist_ok=True)

        return True, f"Folders for all consoles in {root_folder} have been created."
    except Exception as e:
        return False, f"Error creating folders: {str(e)}"