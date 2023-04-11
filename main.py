import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scripts import rom_file_organizer


def show_tooltip(widget, text):
    def enter(event):
        tooltip.config(text=text)
        tooltip.place(x=event.x_root + 20, y=event.y_root + 20)

    def leave(event):
        tooltip.place_forget()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


def browse_directory():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_label.config(text=folder_path)
        organize_button1.config(state=tk.NORMAL)
        organize_button2.config(state=tk.NORMAL)


def organize_files(operation):
    folder_path = path_label["text"]
    organize_button1.config(state=tk.DISABLED)
    organize_button2.config(state=tk.DISABLED)

    if not folder_path:
        messagebox.showerror("Error", "No directory selected.")
        return

    if operation == "generate_m3u":
        success, message = rom_file_organizer.generate_m3u_playlist_for_multi_disc_games(folder_path)
    elif operation == "revert":
        success, message = rom_file_organizer.organize_ps1_roms_in_a_single_folder(folder_path)

    if success:
        messagebox.showinfo("Completed", message)
    else:
        messagebox.showerror("Error", message)

    organize_button1.config(state=tk.NORMAL)
    organize_button2.config(state=tk.NORMAL)


window = tk.Tk()
window.title("RG35XX Roms Manager")
window.geometry("600x150")

frame = ttk.Frame(window, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

apps_frame = ttk.LabelFrame(frame, text="Applications")
apps_frame.grid(column=0, row=0, rowspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

organize_chd_button = ttk.Button(apps_frame, text="Organize CHD Files")
organize_chd_button.grid(column=0, row=0, padx=10, pady=10, sticky=(tk.W, tk.E))

chd_frame = ttk.LabelFrame(frame, text="Organize CHD Files")
chd_frame.grid(column=1, row=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

browse_button = ttk.Button(chd_frame, text="Browse", command=browse_directory)
browse_button.grid(column=0, row=0, sticky=(tk.W, tk.E))

path_label = ttk.Label(chd_frame, text="")
path_label.grid(column=1, row=0, sticky=(tk.W, tk.E))

organize_button1 = ttk.Button(
    chd_frame, text="Generate M3U Playlists", state=tk.DISABLED, command=lambda: organize_files("generate_m3u")
)
organize_button1.grid(column=0, row=2, sticky=(tk.W, tk.E))

organize_button2 = ttk.Button(
    chd_frame, text="Revert to Single Folder", state=tk.DISABLED, command=lambda: organize_files("revert")
)
organize_button2.grid(column=1, row=2, sticky=(tk.W, tk.E))

tooltip = ttk.Label(window, relief="solid", borderwidth=1, background="white")

show_tooltip(organize_button1, "Organize multi-disc games into subdirectories and create M3U playlists.")
show_tooltip(organize_button2, "Move all ROM files back to the main folder, remove M3U files and subdirectories.")

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(1, weight=1)

apps_frame.columnconfigure(0, weight=1)
apps_frame.rowconfigure(0, weight=1)

chd_frame.columnconfigure(1, weight=1)
chd_frame.rowconfigure(2, weight=1)

window.mainloop()
