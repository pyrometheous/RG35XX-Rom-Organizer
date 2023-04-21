import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scripts import rom_file_organizer, sd_card_formatter
import subprocess
import platform
import sys
import os

from scripts.sd_card_formatter import format_drive, get_external_drives


def main():
    # Define application Names
    application_name_01 = "Organize CHD Files"
    application_name_02 = "Setup ROM SD Card"
    application_name_03 = "Format SD Card"

    def organize_files(operation):
        folder_path = chd_path_label.cget("text")

        if operation == "generate_m3u":
            success, message = rom_file_organizer.generate_m3u_playlist_from_CHD(
                folder_path
            )
        elif operation == "revert":
            success, message = rom_file_organizer.move_CHD_to_root_folder_delete_m3u_files(
                folder_path
            )

        if success:
            messagebox.showinfo("Completed", message)
        else:
            messagebox.showerror("Error", message)

    def browse_directory(app_button, app_path_label):
        folder_path = filedialog.askdirectory()
        if folder_path:
            app_path_label.config(text=folder_path)
            app_button.config(state=tk.NORMAL)

    def prompt_relaunch_with_admin_rights():
        root = tk.Tk()

        root.withdraw()
        result = messagebox.askyesno(
            "Admin Rights Required",
            "This feature requires admin rights. Do you want to relaunch the script with admin rights?"
        )
        root.destroy()
        return result

    def relaunch_with_admin_rights():
        system = platform.system()

        cmd = None

        if system == "Windows":
            cmd = ["powershell", "Start-Process", "python", sys.argv[0], "-Verb", "RunAs"]
        elif system in ["Linux", "Darwin"]:
            cmd = ["sudo", "python3", sys.argv[0]]
        else:
            raise OSError("Unsupported operating system.")

        subprocess.run(cmd, check=True)

    def on_click(app_name):
        app_title.config(text=app_name)

        update_right_frame(app_name)

    def update_right_frame(app_name):
        if app_name == application_name_01: # Organize CHD Files
            chd_frame.grid(column=1, row=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            sd_card_frame.grid_remove()
            sd_card_frame
        elif app_name == application_name_02: # Setup ROM SD Card
            chd_frame.grid_remove()
            sd_card_frame.grid(column=1, row=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        elif app_name == application_name_03: # Format SD Card
            drive_format_frame.grid(column=1, row=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
            chd_frame.grid_remove()
            sd_card_frame.grid_remove()
        else:
            chd_frame.grid_remove()
            sd_card_frame.grid_remove()

    def update_drive_list(drive_combobox):
        drives = get_external_drives()
        drive_combobox["values"] = drives
        if drives:
            drive_combobox.set(drives[0])
        else:
            drive_combobox.set("")

    def setup_sd_card(operating_system):
        folder_path = chd_path_label.cget("text")

        success, message = sd_card_formatter.create_rom_folders(folder_path, operating_system)

        if success:
            messagebox.showinfo("Completed", message)
        else:
            messagebox.showerror("Error", message)

    def calculate_pixel_width(lst):
        padding = 0
        # Determine the default font on the current OS
        os_name = platform.system()
        if os_name == "Windows":
            font_name = "Segoe UI"
            font_size = 9  # Default font size on Windows
        elif os_name == "Darwin":
            font_name = "Helvetica"
            font_size = 13  # Default font size on macOS
        else:
            font_name = "DejaVu Sans"  # Assuming a Linux-like OS
            font_size = 10  # Default font size on Linux

        # Create a Tkinter window and a Text widget to set the default font
        root = tk.Tk()
        root.withdraw()
        text = tk.Text(root, font=(font_name, font_size))

        # Find the longest string in the list
        longest_str = max(lst, key=len)

        # Set the contents of the Text widget to the longest string
        text.insert("1.0", longest_str)

        # Resize the Text widget to fit its contents
        text.update_idletasks()
        text_width = text.winfo_width()
        text_height = text.winfo_height()
        text.config(width=text_width, height=text_height)

        # Calculate the pixel width of the Text widget
        pixel_width = text_width - 4  # Subtract 4 pixels for the widget border

        # Return the pixel width as an integer
        return int(pixel_width) + padding

    def populate_application_names(local_vars):
        application_names = []

        for var_name in local_vars:
            if var_name.startswith("application_name_"):
                application_names.append(local_vars[var_name])

        return application_names

    def create_app_frame_template():
        frame = ttk.Frame(right_frame)

    def populate_apps():
        listbox = tk.Listbox(left_frame, height=len(application_names),
                                  width=calculate_pixel_width(application_names))
        for i, application_name in enumerate(application_names):
            listbox.insert(i, application_name)
        listbox.bind(
            "<<ListboxSelect>>",
            lambda event: on_click(listbox.get(listbox.curselection())),
        )
        listbox.grid(column=0, row=1)

        r_frame = ttk.Frame(window, relief="groove", borderwidth=1)
        r_frame.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title = ttk.Label(r_frame, text="")
        title.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))
        return listbox, r_frame, title

    def handle_format_drive(drive, file_system, parent):
        success, stdout, stderr = format_drive(drive, file_system)
        if success:
            messagebox.showinfo("Success", f"Drive {drive} formatted successfully.", parent=parent)
        else:
            messagebox.showerror("Error", f"Error formatting drive {drive}:\n{stderr}", parent=parent)

    def enable_buttons_after_browsing(app_path_label, *buttons):
        def inner_enable_buttons_after_browsing():
            folder_path = browse_directory(buttons[0], app_path_label)
            for button in buttons:
                button.config(state=tk.NORMAL)

        return inner_enable_buttons_after_browsing

    def create_organize_chd_files_frame():
        frame = ttk.Frame(right_frame)
        frame.columnconfigure(1, weight=1)

        # Create Generate M3U Playlists button
        organize_button1 = ttk.Button(
            frame,
            text="Generate M3U Playlists",
            state=tk.DISABLED,
            command=lambda: organize_files("generate_m3u"),
        )
        organize_button1.grid(column=0, row=3, sticky=(tk.W, tk.E))

        # Create Revert to Single Folder button
        organize_button2 = ttk.Button(
            frame,
            text="Revert to Single Folder",
            state=tk.DISABLED,
            command=lambda: organize_files("revert"),
        )
        organize_button2.grid(column=1, row=3, sticky=(tk.W, tk.W))

        # Setup Path Label
        path_label = ttk.Label(frame, text="")
        path_label.grid(column=1, row=2, sticky=(tk.W, tk.E))

        # Setup Browse Button
        browse_button = ttk.Button(frame, text="Browse", command=lambda: browse_directory(organize_button1, path_label))
        browse_button.grid(column=0, row=1, sticky=(tk.W, tk.E))

        # Frame and window formatting

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)
        return frame, path_label

    def create_setup_roms_sd_card_frame():
        frame = ttk.Frame(right_frame)
        frame.columnconfigure(1, weight=1)

        # Create the path_label
        path_label = ttk.Label(frame, text="")
        path_label.grid(column=1, row=2, sticky=tk.W)  # Left-align the label within the grid

        # Configure the columns
        frame.columnconfigure(0, weight=1)
        #frame.columnconfigure(1, weight=0)  # Set the weight to 0 for the column containing the label
        #frame.columnconfigure(2, weight=1)

        # Create Button to create folders for Garlic OS
        create_folders_for_garlic_os_button = ttk.Button(
            frame,
            text="Create Folders for Garlic OS",
            state=tk.DISABLED,
            command=lambda: setup_sd_card("Garlic")
        )
        create_folders_for_garlic_os_button.grid(column=0, row=3, sticky=(tk.W, tk.E))

        # Create Button to create folders for Batocera
        create_folders_for_batocera_os_button = ttk.Button(
            frame,
            text="Create Folders for Batocera",
            state=tk.DISABLED,
            command=lambda: setup_sd_card("Batocera")
        )
        create_folders_for_batocera_os_button.grid(column=1, row=3, sticky=(tk.W, tk.E))

        # Create Browse Button
        browse_button = ttk.Button(
            frame,
            text="Browse",
            command=enable_buttons_after_browsing(
                path_label,
                create_folders_for_batocera_os_button,
                create_folders_for_garlic_os_button
            ),
        )
        browse_button.grid(column=0, row=1, sticky=(tk.W, tk.E))

        return frame, path_label

    def on_format_drive(drive_var, file_system_var):
        drive = drive_var.get()
        file_system = file_system_var.get()

        if not drive or not file_system:
            messagebox.showerror("Error", "Please select a drive and file system")
            return

        success, _, error = format_drive(drive, file_system)
        if success:
            messagebox.showinfo("Success", f"Drive {drive} formatted successfully")
        else:
            messagebox.showerror("Error", f"Error formatting drive {drive}: {error}")

    def create_format_sd_card_frame():
        frame = ttk.Frame(right_frame)

        # Create the drive selection dropdown
        drives = get_external_drives()
        drive_var = tk.StringVar()
        drive_combobox = ttk.Combobox(frame, textvariable=drive_var)
        drive_combobox["values"] = drives
        if drives:
            drive_combobox.set(drives[0])
        drive_combobox.grid(column=0, row=1, sticky=(tk.W, tk.E))

        # Create refresh button to update the drive list
        refresh_button = ttk.Button(
            frame,
            text="Refresh",
            command=lambda: update_drive_list(drive_combobox)
        )
        refresh_button.grid(column=1, row=1, sticky=(tk.W, tk.E))

        # Create the format button
        format_button = ttk.Button(
            frame,
            text="Format Drive",
            command=lambda: on_format_drive(drive_var, file_system_var)
        )
        format_button.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E))

        # Create the file system selection dropdown
        file_systems = ["exFAT", "FAT32"]
        file_system_var = tk.StringVar(value=file_systems[0])
        file_system_combobox = ttk.Combobox(frame, textvariable=file_system_var)
        file_system_combobox["values"] = file_systems
        file_system_combobox.grid(column=0, row=2, sticky=(tk.W, tk.E))

        # Create the format drive button
        format_button = ttk.Button(
            frame,
            text="Format Drive",
            command=lambda: handle_format_drive(
                drive_var.get(),
                file_system_var.get(),
                frame
            )
        )
        format_button.grid(column=1, row=2, sticky=(tk.W, tk.E))

        return frame

    def close_app():
        window.destroy()
        sys.exit(0)

    # User Interface code
    window = tk.Tk()
    window.title("RG35XX Roms Manager")
    window.minsize(500, 100)
    window.maxsize(500, 100)
    window.protocol("WM_DELETE_WINDOW", close_app)
    window.columnconfigure(0, weight=0, minsize=150)  # Set minsize=200 for the left frame
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    icon_path = os.path.join(base_path, "media", "icon.gif")

    window.iconphoto(True, tk.PhotoImage(file=icon_path))

    left_frame = ttk.Frame(window, relief="groove", borderwidth=2)
    left_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    left_frame_title = ttk.Label(left_frame, text="Applications")
    left_frame_title.grid(column=0, row=0)

    # Build Application Names Array
    application_names = populate_application_names(locals())

    # Populate Apps

    apps_listbox, right_frame, app_title = populate_apps()

    # Create Organize CHD Files Frame
    chd_frame, chd_path_label = create_organize_chd_files_frame()

    # Create ROM SD Card Setup Frame
    sd_card_frame, setup_sd_card_folders_path_label = create_setup_roms_sd_card_frame()

    # Create Format SD Card Frame
    drive_format_frame = create_format_sd_card_frame()

    drive_format_frame.grid_remove() # Hide frame by default

    sd_card_frame.grid_remove()  # Hide frame by default

    chd_frame.grid_remove()  # Hide frame

    apps_listbox.selection_set(0)
    on_click(application_names[0])

    window.mainloop()


if __name__ == "__main__":
    main()
