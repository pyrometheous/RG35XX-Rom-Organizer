import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scripts import rom_file_organizer, sd_card_formatter
import platform


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
        path_label_sd_card.config(text=folder_path)  # Add this line to update the path_label_sd_card text
        organize_button1.config(state=tk.NORMAL)
        organize_button2.config(state=tk.NORMAL)
        setup_sd_card_button_garlic.config(state=tk.NORMAL)
        setup_sd_card_button_batocera.config(state=tk.NORMAL)



def on_click(app_name):
    app_title.config(text=app_name)
    update_right_frame(app_name)


def update_right_frame(app_name):
    if app_name == "Organize CHD Files":
        chd_frame.grid(column=1, row=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        sd_card_frame.grid_remove()
    elif app_name == "Setup ROM SD Card":
        chd_frame.grid_remove()
        sd_card_frame.grid(column=1, row=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    else:
        chd_frame.grid_remove()
        sd_card_frame.grid_remove()


def setup_sd_card(os):
    folder_path = path_label.cget("text")
    success, message = sd_card_formatter.create_rom_folders(folder_path, os)

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


window = tk.Tk()
window.title("RG35XX Roms Manager")
# window.geometry("500x100")
window.minsize(500, 100)
window.maxsize(500, 100)
window.iconphoto(True, tk.PhotoImage(file="./media/icon.gif"))

left_frame = ttk.Frame(window, relief="groove", borderwidth=2)
left_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

left_frame_title = ttk.Label(left_frame, text="Applications")
left_frame_title.grid(column=0, row=0)

application_names = ["Organize CHD Files", "Setup ROM SD Card", "Application 3"]

apps_listbox = tk.Listbox(left_frame, height=len(application_names), width=calculate_pixel_width(application_names))
for i, application_name in enumerate(application_names):
    apps_listbox.insert(i, application_name)
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

window.columnconfigure(0, weight=0, minsize=150)  # Set minsize=200 for the left frame
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
chd_frame.columnconfigure(1, weight=1)
chd_frame.rowconfigure(1, weight=1)

sd_card_frame = ttk.Frame(right_frame)
sd_card_frame.columnconfigure(1, weight=1)

browse_button_sd_card = ttk.Button(sd_card_frame, text="Browse", command=browse_directory)
browse_button_sd_card.grid(column=0, row=1, sticky=(tk.W, tk.E))


path_label_sd_card = ttk.Label(sd_card_frame, text="")
path_label_sd_card.grid(column=1, row=1, columnspan=2, sticky=(tk.W, tk.E))  # Add columnspan=2

setup_sd_card_button_garlic = ttk.Button(
    sd_card_frame,
    text="Create Folders for Garlic OS",
    state=tk.DISABLED,
    command=lambda: setup_sd_card("Garlic")
)
setup_sd_card_button_garlic.grid(column=0, row=2, sticky=(tk.W, tk.E))
setup_sd_card_button_batocera = ttk.Button(
    sd_card_frame,
    text="Create Folders for Batocera",
    state=tk.DISABLED,
    command=lambda: setup_sd_card("Batocera")
)
setup_sd_card_button_batocera.grid(column=1, row=2, sticky=(tk.W, tk.E))  # Change column from 2 to 1

sd_card_frame.grid_remove()  # Hide frame by default

chd_frame.grid_remove()  # Hide frame

# Uncomment the line below to start the application with the first app selected by default
apps_listbox.selection_set(0)
on_click(application_names[0])

window.mainloop()