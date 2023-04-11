import os

def create_garlic_os_folders(folder_path):
    folders = [
        "AMIGA", "AMIGACD", "APPS", "ARCADE", "ATARI", "ATARIST", "bios", "COLECO",
        "COMMODORE", "CPC", "CPS", "CPS1", "CPS2", "CPS3", "DOS", "EIGHTHUNDRED",
        "FAIRCHILD", "FBA2012", "FBAHACK", "FBNEO", "FC", "FDS", "FIFTYTWOHUNDRED",
        "GB", "GBA", "GBC", "GG", "GW", "INTELLIVISION", "JAGUAR", "LYNX", "MAME",
        "MAME2000", "MD", "MEGADUCK", "MS", "MSX", "NEOCD", "NEOGEO", "NGP", "NGPC",
        "ODYSSEY", "PANASONIC", "PCE", "PCECD", "PCEIGHTYEIGHT", "PCENGINE", "PCFX",
        "PCNINETYEIGHT", "PICO", "POKE", "PORTS", "PS", "QUAKE", "SATELLAVIEW", "save",
        "Saves", "SCUMMVM", "SEGACD", "SEGASGONE", "SEVENTYEIGHTHUNDRED", "SFC", "SGB",
        "SGFX", "SMS", "SUFAMI", "SUPERVISION", "THIRTYTWOX", "TIC", "UZEBOX", "VB",
        "VECTREX", "VERTICAL", "VIDEOPAC", "VIDEOS", "VMU", "WonderSwan", "WS", "X68000",
        "XONE", "ZXEIGHTYONE", "ZXS"
    ]

    for folder in folders:
        os.makedirs(os.path.join(folder_path, folder), exist_ok=True)

    return True, "Folders for Garlic OS have been created."
