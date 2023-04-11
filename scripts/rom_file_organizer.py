import os
import re


def generate_m3u_playlist_from_CHD(folder_path):
    multi_disc_games = {}
    total_files = 0
    error_log = []

    for _, _, files in os.walk(folder_path):
        total_files += len(files)

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".chd"):
                match = re.match(r"(.+?)\s\((.+?)\)\s\((Disc\s\d+)\)", filename)
                if match:
                    game_title, region, disc = match.groups()
                    if game_title not in multi_disc_games:
                        multi_disc_games[game_title] = []
                    multi_disc_games[game_title].append(os.path.join(root, filename))

    for game_title, disc_paths in multi_disc_games.items():
        subdir_path = os.path.join(folder_path, game_title)
        if not os.path.exists(subdir_path):
            os.mkdir(subdir_path)

        for disc_path in sorted(
            disc_paths, key=lambda x: re.search(r"(Disc\s\d+)", x).group(0)
        ):
            if os.path.dirname(disc_path) != subdir_path:
                old_path = disc_path
                new_path = os.path.join(subdir_path, os.path.basename(disc_path))
                try:
                    os.rename(old_path, new_path)
                except Exception as e:
                    error_log.append(
                        f"Error moving file '{old_path}' to '{new_path}': {str(e)}"
                    )

    subdirectories = [
        os.path.join(folder_path, d)
        for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
    ]

    for subdir_path in subdirectories:
        game_title = os.path.basename(subdir_path)
        m3u_filename = f"{game_title}.m3u"
        m3u_path = os.path.join(folder_path, m3u_filename)

        chd_files = [f for f in os.listdir(subdir_path) if f.endswith(".chd")]

        if chd_files:
            try:
                with open(m3u_path, "w") as m3u_file:
                    for chd_file in sorted(
                        chd_files, key=lambda x: re.search(r"(Disc\s\d+)", x).group(0)
                    ):
                        m3u_file.write(f"{game_title}/{chd_file}\n")
            except Exception as e:
                error_log.append(f"Error creating m3u file '{m3u_path}': {str(e)}")

    if error_log:
        with open(os.path.join(folder_path, "error_log.txt"), "w") as error_file:
            for error in error_log:
                error_file.write(f"{error}\n")
        return False, "Errors occurred during execution. Please check error_log.txt."
    else:
        return True, "Organization of PS1 Roms is complete."


def move_CHD_to_root_folder_delete_m3u_files(folder_path):
    error_log = []

    subdirectories = [
        os.path.join(folder_path, d)
        for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
    ]

    for subdir_path in subdirectories:
        chd_files = [f for f in os.listdir(subdir_path) if f.endswith(".chd")]

        for chd_file in chd_files:
            old_path = os.path.join(subdir_path, chd_file)
            new_path = os.path.join(folder_path, chd_file)

            try:
                os.rename(old_path, new_path)
            except Exception as e:
                error_log.append(
                    f"Error moving file '{old_path}' to '{new_path}': {str(e)}"
                )

        try:
            os.rmdir(subdir_path)
        except Exception as e:
            error_log.append(f"Error removing directory '{subdir_path}': {str(e)}")

    m3u_files = [f for f in os.listdir(folder_path) if f.endswith(".m3u")]

    for m3u_file in m3u_files:
        m3u_path = os.path.join(folder_path, m3u_file)
        try:
            os.remove(m3u_path)
        except Exception as e:
            error_log.append(f"Error removing m3u file '{m3u_path}': {str(e)}")

    if error_log:
        with open(os.path.join(folder_path, "error_log_reverse.txt"), "w") as error_file:
            for error in error_log:
                error_file.write(f"{error}\n")
        return False, "Errors occurred during execution. Please check error_log_reverse.txt."
    else:
        return True, "Reverting PS1 Roms to a single folder is complete."
