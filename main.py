import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scripts import rom_file_organizer


def organize_files(operation):
    folder_path = path_label.cget("text")
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


def browse_directory():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_label.config(text=folder_path)
        organize_button1.config(state=tk.NORMAL)
        organize_button2.config(state=tk.NORMAL)


def on_click(app_name):
    app_title.config(text=app_name)
    update_right_frame(app_name)


def update_right_frame(app_name):
    global chd_frame
    if app_name == "Organize CHD Files":
        chd_frame.grid(column=1, row=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    else:
        chd_frame.grid_remove()


window = tk.Tk()
window.title("RG35XX Roms Manager")
# window.geometry("500x100")
window.minsize(500, 100)
window.maxsize(500, 100)
window.iconphoto(True, tk.PhotoImage(file="./media/icon.gif"))


left_frame = ttk.Frame(window, relief="groove", borderwidth=1)
left_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

left_frame_title = ttk.Label(left_frame, text="Applications")
left_frame_title.grid(column=0, row=0)

app_names = ["Organize CHD Files", "Application 2", "Application 3"]

apps_listbox = tk.Listbox(left_frame, height=4, width=20)
for i, app_name in enumerate(app_names):
    apps_listbox.insert(i, app_name)
apps_listbox.bind(
    "<<ListboxSelect>>",
    lambda event: on_click(apps_listbox.get(apps_listbox.curselection())),
)
apps_listbox.grid(column=0, row=1)

right_frame = ttk.Frame(window, relief="groove", borderwidth=1)
right_frame.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

app_title = ttk.Label(right_frame, text="")
app_title.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))

chd_frame = ttk.Frame(right_frame)
chd_frame.columnconfigure(1, weight=1)

browse_button = ttk.Button(chd_frame, text="Browse", command=browse_directory)
browse_button.grid(column=0, row=1, sticky=(tk.W, tk.E))

path_label = ttk.Label(chd_frame, text="")
path_label.grid(column=1, row=1, sticky=(tk.W, tk.E))

organize_button1 = ttk.Button(
    chd_frame,
    text="Generate M3U Playlists",
    state=tk.DISABLED,
    command=lambda: organize_files("generate_m3u"),
)
organize_button1.grid(column=0, row=2, sticky=(tk.W, tk.E))

organize_button2 = ttk.Button(
    chd_frame,
    text="Revert to Single Folder",
    state=tk.DISABLED,
    command=lambda: organize_files("revert"),
)
organize_button2.grid(column=1, row=2, sticky=(tk.W, tk.E))

window.columnconfigure(0, weight=0, minsize=100)  # Set minsize=200 for the left frame
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
chd_frame.columnconfigure(1, weight=1)
chd_frame.rowconfigure(1, weight=1)

chd_frame.grid_remove()  # Hide frame by default

window.mainloop()
