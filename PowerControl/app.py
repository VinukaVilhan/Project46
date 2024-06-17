import customtkinter as ctk
from ttkbootstrap.constants import *
from PIL import Image
from power_functions import shutdown, restart, sleep, toggle_entry_and_shutdown, toggle_entry_and_restart, toggle_entry_and_sleep, toggle_entry_and_wifi_off_control, toggle_entry_and_wifi_on_control, toggle_on_wifi_switch, go_back, get_admin_privileges, abort_shutdown, abort_restart, abort_sleep, abort_wifi_off, abort_wifi_on, wifi_off_thread, wifi_on_thread, resource_path

get_admin_privileges()
#created a window frame object
root = ctk.CTk(fg_color="#121212")
root.title("Control")

# Set the size of the window
root.geometry("500x500")

# Create a bold font tuple
bold_font = ('Arial', 15, 'bold')

# Create a custom font using the hacker font file
hacker_font = ("Courier", 15, 'bold')
hacker_font_button = ("Courier",14, 'bold')
hacker_countdown_font = ("Courier", 22, 'bold')

# Create shutdown widgets
shutdown_countdown = ctk.CTkLabel(root, text="", font=hacker_countdown_font, text_color="#00FF00")
shutdown_countdown.grid_remove()
shutdown_text_label = ctk.CTkLabel(root, text="Enter Shutdown Time (HH:MM)", font=hacker_font)
shutdown_entry = ctk.CTkEntry(root)
shutdown_button = ctk.CTkButton(root, text="Shutdown", font=hacker_font_button, hover_color="#006400",fg_color="#000000", border_color="#00FF00", border_width=2, command=lambda:shutdown(shutdown_entry, root, shutdown_countdown,shutdown_abort_button, restart_entry,sleep_entry))
shutdown_abort_button = ctk.CTkButton(root, text="Abort", font=hacker_font_button, hover_color="#640000",fg_color="#000000", border_color="#FF0000", border_width=2, width=80, height=20, corner_radius=5, command=lambda: abort_shutdown(shutdown_countdown,shutdown_abort_button, restart_entry,sleep_entry))

# Create restart widgets
restart_countdown = ctk.CTkLabel(root, text="", font=hacker_countdown_font, text_color="#00FF00")
restart_countdown.grid_remove()
restart_text_label = ctk.CTkLabel(root, text="Enter Restart Time (HH:MM)", font=hacker_font)
restart_entry = ctk.CTkEntry(root)
restart_button = ctk.CTkButton(root, text="Restart", font=hacker_font_button,  hover_color="#006400",fg_color="#000000", border_color="#00FF00", border_width=2, command=lambda:restart(restart_entry, root, restart_countdown, restart_abort_button, shutdown_entry,sleep_entry))
restart_abort_button = ctk.CTkButton(root, text="Abort", font=hacker_font_button, hover_color="#640000",fg_color="#000000", border_color="#FF0000", border_width=2, width=80, height=20, corner_radius=5, command=lambda: abort_restart(restart_countdown,restart_abort_button, shutdown_entry,sleep_entry))

# Create sleep widgets
sleep_countdown = ctk.CTkLabel(root, text="", font=hacker_countdown_font, text_color="#00FF00")
sleep_countdown.grid_remove()
sleep_text_label = ctk.CTkLabel(root, text="Enter Sleep Time (HH:MM)", font=hacker_font)
sleep_entry = ctk.CTkEntry(root)
sleep_button = ctk.CTkButton(root, text="Sleep", font=hacker_font_button,  hover_color="#006400",fg_color="#000000", border_color="#00FF00", border_width=2, command=lambda:sleep(sleep_entry, root, sleep_countdown, sleep_abort_button, shutdown_entry, restart_entry))
sleep_abort_button = ctk.CTkButton(root, text="Abort", font=hacker_font_button, hover_color="#640000",fg_color="#000000", border_color="#FF0000", border_width=2, width=80, height=20, corner_radius=5, command=lambda: abort_sleep(sleep_countdown,sleep_abort_button, shutdown_entry, restart_entry))

# Create wifi widgets (off)
wifi_off_countdown = ctk.CTkLabel(root, text="", font=hacker_countdown_font, text_color="#00FF00")
wifi_off_countdown.grid_remove()
wifi_off_text_label = ctk.CTkLabel(root, text="Enter WIFI Adapter OFF Time (HH:MM)", font=hacker_font)
wifi_off_entry = ctk.CTkEntry(root)
wifi_off_button = ctk.CTkButton(root, text="Turn Off WIFI", font=hacker_font_button, hover_color="#006400", fg_color="#000000", border_color="#00FF00", border_width=2, command=lambda: wifi_off_thread(wifi_off_entry, root, wifi_off_countdown, wifi_off_abort_button, shutdown_entry, restart_entry, sleep_entry))
wifi_off_abort_button = ctk.CTkButton(root, text="Abort", font=hacker_font_button, hover_color="#640000",fg_color="#000000", border_color="#FF0000", border_width=2, width=80, height=20, corner_radius=5, command=lambda: abort_wifi_off(wifi_off_countdown,wifi_off_abort_button))

#create wifi on button
wifi_on_countdown = ctk.CTkLabel(root, text="", font=hacker_countdown_font, text_color="#00FF00")
wifi_on_countdown.grid_remove()
wifi_on_text_label = ctk.CTkLabel(root, text="Enter WIFI Adapter ON Time (HH:MM)", font=hacker_font)
wifi_on_entry = ctk.CTkEntry(root, state="normal")
wifi_on_switch = ctk.CTkSwitch(root, text="Turn On Now", font=hacker_font_button, command=lambda: toggle_on_wifi_switch(wifi_on_entry, wifi_on_switch))
wifi_on_button = ctk.CTkButton(root, text="Turn On WIFI", font=hacker_font_button, hover_color="#006400",fg_color="#000000", border_color="#00FF00", border_width=2, command=lambda:wifi_on_thread(wifi_on_entry, root, wifi_on_switch, wifi_on_countdown, wifi_on_abort_button, shutdown_entry, restart_entry, sleep_entry))
wifi_on_abort_button = ctk.CTkButton(root, text="Abort", font=hacker_font_button, hover_color="#640000",fg_color="#000000", border_color="#FF0000", border_width=2, width=80, height=20, corner_radius=5, command=lambda: abort_wifi_on(wifi_on_countdown,wifi_on_abort_button))

# Create back button
back_button = ctk.CTkButton(root, text="Back", width=80, font=hacker_font_button, height=20, corner_radius=5, hover_color="#006400",fg_color="#000000", border_color="#00FF00", border_width=2, command=lambda: go_back(
    shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label,
    shutdown_text_label, restart_text_label, sleep_text_label, wifi_off_text_label, wifi_on_text_label,
    shutdown_entry, restart_entry, sleep_entry, wifi_off_entry, wifi_on_entry,
    shutdown_button, restart_button, sleep_button, wifi_off_button, back_button, wifi_on_button, wifi_on_switch, shutdown_countdown, restart_countdown, sleep_countdown, wifi_off_countdown, wifi_on_countdown, shutdown_abort_button, restart_abort_button, sleep_abort_button, wifi_off_abort_button, wifi_on_abort_button))

# Load icons for shutdown
shutdown_resource_image = resource_path("assets/Icons/shutdown.png")
shutdown_image = ctk.CTkImage(light_image=Image.open(shutdown_resource_image), size=(50, 50))

# Create label for shutdown icon
shutdown_label = ctk.CTkLabel(root, image=shutdown_image, text="", bg_color="#121212")
shutdown_label.grid(row=1, column=0, pady=10)
shutdown_label.bind("<Button-1>", lambda event: toggle_entry_and_shutdown(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, shutdown_text_label, shutdown_entry, shutdown_button, back_button, shutdown_abort_button))

# Load icons for restart
restart_resorce_image = resource_path("assets/Icons/restart.png")
restart_image = ctk.CTkImage(light_image=Image.open(restart_resorce_image), size=(50, 50))

# Create label for restart icon
restart_label = ctk.CTkLabel(root, image=restart_image, text="", bg_color="#121212")
restart_label.grid(row=2, column=0, pady=10)
restart_label.bind("<Button-1>", lambda event: toggle_entry_and_restart(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, restart_text_label, restart_entry, restart_button, back_button, restart_abort_button))

# Load icons for sleep
sleep_resource_image = resource_path("assets/Icons/sleep.png")
sleep_image = ctk.CTkImage(light_image=Image.open(sleep_resource_image), size=(50, 50))

# Create label for sleep icon
sleep_label = ctk.CTkLabel(root, image=sleep_image, text="", bg_color="#121212")
sleep_label.grid(row=3, column=0, pady=10)
sleep_label.bind("<Button-1>", lambda event:toggle_entry_and_sleep(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, sleep_text_label, sleep_entry, sleep_button, back_button, sleep_abort_button))

# Load icons for wifi control
wifi_off_resorce_image = resource_path("assets/Icons/wifi_off.png")
wifi_off_image = ctk.CTkImage(light_image=Image.open(wifi_off_resorce_image), size=(50, 50))

# Create label for wifi icon
wifi_off_label = ctk.CTkLabel(root, image=wifi_off_image, text="", bg_color="#121212")
wifi_off_label.grid(row=4, column=0, pady=10)
wifi_off_label.bind("<Button-1>", lambda event: toggle_entry_and_wifi_off_control(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label,wifi_off_text_label, wifi_off_entry, wifi_off_button, back_button, wifi_off_abort_button))

# Load icons for wifi control
wifi_on_resorce_image = resource_path("assets/Icons/wifi_on.png")
wifi_on_image = ctk.CTkImage(light_image=Image.open(wifi_on_resorce_image), size=(50, 50))

# Create label for wifi icon
wifi_on_label = ctk.CTkLabel(root, image=wifi_on_image, text="", bg_color="#121212")
wifi_on_label.grid(row=5, column=0, pady=10)
wifi_on_label.bind("<Button-1>", lambda event: toggle_entry_and_wifi_on_control(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, wifi_on_text_label, wifi_on_entry, wifi_on_button, back_button, wifi_on_switch, wifi_on_abort_button))


# Center all widgets vertically and horizontally
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(0, weight=4)


root.mainloop()