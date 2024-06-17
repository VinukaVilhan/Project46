from tkinter import  messagebox
from datetime import datetime, timedelta
import os
import ctypes
import win32con
import sys
import ctypes
import os
import threading

#global variables
is_home_page = None
is_shutdown_page = None
is_restart_page = None
is_sleep_page = None
is_wifi_off_page = None
is_wifi_on_page = None
is_shutdown_timer_on = None
is_restart_timer_on = None
is_sleep_timer_on = None
is_wifi_off_timer_on = None
is_wifi_on_timer_on = None
is_shutdown_aborted = None
is_restart_aborted = None
is_sleep_aborted = None
is_wifi_off_aborted = None
is_wifi_on_aborted = None


def get_admin_privileges():
    """
    Get administrative privileges for the script.
    """
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # Re-run the script with administrative privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, win32con.SW_HIDE)
            sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")


def abort_shutdown(shutdown_countdown, shutdown_abort_button, restart_entry, sleep_entry):
    global is_shutdown_aborted
    is_shutdown_aborted = True

    global is_shutdown_timer_on
    is_shutdown_timer_on = False
    
    shutdown_countdown.configure(text="Shutdown Aborted")
    messagebox.showinfo("Shutdown Status", "Shutdown Aborted")
    shutdown_abort_button.configure(state="disabled")
    restart_entry.configure(state="normal")
    sleep_entry.configure(state="normal")
    

def update_shutdown_countdown(delay, shutdown_countdown, root, restart_entry, sleep_entry):
    global is_shutdown_aborted
    if is_shutdown_aborted:
        return
    
    global is_shutdown_timer_on
    is_shutdown_timer_on = True

    #check for the restart and sleep entry
    restart_sleep_entry(restart_entry, sleep_entry)
    
    #make the grid appear
    if is_shutdown_page:
        shutdown_countdown.grid(row=1, column=0, pady=10)
    else:
        shutdown_countdown.grid_remove()

    remaining_time = delay // 1000

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Update the countdown label
    shutdown_countdown.configure(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")

    #decrement the delay by 1 second
    delay -= 1000

    if delay > 0:
        # Call the function after 1 second
        root.after(1000, update_shutdown_countdown, delay, shutdown_countdown, root, restart_entry, sleep_entry)
    else:
        is_shutdown_timer_on = False
        restart_entry.configure(state="normal")
        sleep_entry.configure(state="normal")


# Parse the time entered by the user
def shutdown(shutdown_entry, root, shutdown_countdown, shutdown_abort_button, restart_entry, sleep_entry):
    global is_shutdown_aborted
    is_shutdown_aborted = False

    global is_shutdown_timer_on
    if is_shutdown_timer_on:
        messagebox.showerror("Error", "Please wait for the current shutdown process to complete or abort it before starting a new one.")
        return

    shutdown_time = shutdown_entry.get()
    try:
        # Parse the time entered by the user, gets default date
        shutdown_time = datetime.strptime(shutdown_time, "%H:%M")
        current_time = datetime.now()
        # Set the shutdown time to the current date while keeping the time
        shutdown_time = current_time.replace(hour=shutdown_time.hour, minute=shutdown_time.minute, second=0, microsecond=0)

        # If the shutdown time is less than the current time, set it for the next day
        if shutdown_time < current_time:
            shutdown_time += timedelta(days=1)

        delay = (shutdown_time - current_time).total_seconds() * 1000  # Convert to milliseconds

        # Confirmation
        if messagebox.askyesno("Shutdown Confirmation", f"Your computer will shutdown at {shutdown_time.strftime('%H:%M')}"):
            # If the user confirms, the computer will shutdown. After the delay the function will be called and the process will proceed
            root.after(int(delay), shutdown_computer)
            update_shutdown_countdown(delay, shutdown_countdown, root, restart_entry, sleep_entry)
            shutdown_abort_button.configure(state="normal")

    except ValueError:
        messagebox.showerror("Error", "Please enter the time in the format HH:MM")

def shutdown_computer():
    global is_shutdown_aborted
    if os.name == 'nt' and is_shutdown_aborted == False:
        os.system("Shutdown /s /t 1")


def abort_restart(restart_countdown, restart_abort_button, shutdown_entry, sleep_entry):
    global is_restart_aborted
    is_restart_aborted = True

    global is_restart_timer_on
    is_restart_timer_on = False
    
    restart_countdown.configure(text="Restart Aborted")
    messagebox.showinfo("Restart Status", "Restart Aborted")
    restart_abort_button.configure(state="disabled")
    shutdown_entry.configure(state="normal")
    sleep_entry.configure(state="normal")

def update_restart_countdown(delay, restart_countdown, root, shutdown_entry, sleep_entry):

    global is_restart_aborted
    if is_restart_aborted:
        return
    
    global is_restart_timer_on
    is_restart_timer_on = True

    #check for the shutdown and sleep entry
    shutdown_sleep_entry(shutdown_entry, sleep_entry)

    #check if the restart page is active
    if is_restart_page:
        restart_countdown.grid(row=1, column=0, pady=10)
    else:
        restart_countdown.grid_remove()

    remaining_time = delay // 1000

    hours, remainder = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    restart_countdown.configure(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")

    delay -= 1000

    if delay > 0:
        root.after(1000, update_restart_countdown, delay, restart_countdown, root, shutdown_entry, sleep_entry)
    else:
        is_restart_timer_on = False
        shutdown_entry.configure(state="normal")
        sleep_entry.configure(state="normal")


def restart(restart_entry, root, restart_countdown, restart_abort_button, shutdown_entry, sleep_entry):
    global is_restart_aborted
    is_restart_aborted = False

    global is_restart_timer_on
    if is_restart_timer_on:
        messagebox.showerror("Error", "Please wait for the current restart process to complete or abort it before starting a new one.")
        return

    restart_time = restart_entry.get()
    try:
        restart_time = datetime.strptime(restart_time, "%H:%M")
        current_time = datetime.now()
        restart_time = current_time.replace(hour=restart_time.hour, minute=restart_time.minute, second=0, microsecond=0)

        if restart_time < current_time:
            restart_time += timedelta(days=1)
        
        # get the deylay in milliseconds
        delay = (restart_time - current_time).total_seconds() * 1000

        if messagebox.askyesno("Restart Confirmation", f"Your computer will restart at {restart_time.strftime('%H:%M')}"):
            root.after(int(delay), restart_computer)
            update_restart_countdown(delay, restart_countdown, root, shutdown_entry, sleep_entry)
            restart_abort_button.configure(state="normal")

    except ValueError:
        messagebox.showerror("Error", "Please enter the time in the format HH:MM")

def restart_computer():
    if os.name == 'nt' and is_restart_aborted == False:
        os.system("shutdown /r /t 1")


def abort_sleep(sleep_countdown, sleep_abort_button, shutdown_entry, restart_entry):
    global is_sleep_aborted
    is_sleep_aborted = True

    global is_sleep_timer_on
    is_sleep_timer_on = False
    
    sleep_countdown.configure(text="Sleep Aborted")
    messagebox.showinfo("Sleep Status", "Sleep Aborted")
    sleep_abort_button.configure(state="disabled")
    shutdown_entry.configure(state="normal")
    restart_entry.configure(state="normal")


def update_sleep_countdown(delay, sleep_countdown, root, sleep_abort_button, shutdown_entry, restart_entry):   
    global is_sleep_aborted 
    if is_sleep_aborted:
        return
    
    global is_sleep_timer_on
    is_sleep_timer_on = True

    #check for the shutdown and restart entry
    restart_shutdown_entry(restart_entry, shutdown_entry)

    if is_sleep_page:
        sleep_countdown.grid(row=1, column=0, pady=10)
    else:
        sleep_countdown.grid_remove()

    remaining_time = delay // 1000

    hours, remainder = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    sleep_countdown.configure(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")

    delay -= 1000

    if delay > 0:
        root.after(1000, update_sleep_countdown, delay, sleep_countdown, root, sleep_abort_button, shutdown_entry, restart_entry)
    else:
        is_sleep_timer_on = False
        sleep_abort_button.configure(state="disabled")
        shutdown_entry.configure(state="normal")
        restart_entry.configure(state="normal")
        
def sleep(sleep_entry, root, sleep_countdown, sleep_abort_button, shutdown_entry, restart_entry):
    global is_sleep_aborted
    is_sleep_aborted = False

    global is_sleep_timer_on
    if is_sleep_timer_on:
        messagebox.showerror("Error", "Please wait for the current sleep process to complete or abort it before starting a new one.")
        return

    sleep_time = sleep_entry.get()
    try:
        sleep_time = datetime.strptime(sleep_time, "%H:%M")
        current_time = datetime.now()
        print(current_time)
        sleep_time = current_time.replace(hour=sleep_time.hour, minute=sleep_time.minute, second=0, microsecond=0)

        if sleep_time < current_time:
            sleep_time += timedelta(days=1)

        delay = (sleep_time - current_time).total_seconds() * 1000

        if messagebox.askyesno("Sleep Confirmation", f"Your computer will sleep at {sleep_time.strftime('%H:%M')}"):
            root.after(int(delay), sleep_computer)
            update_sleep_countdown(delay, sleep_countdown, root, sleep_abort_button, shutdown_entry, restart_entry)
            sleep_abort_button.configure(state="normal")


    except ValueError:
        messagebox.showerror("Error", "Please enter the time in the format HH:MM")

def sleep_computer():
    if os.name == 'nt' and is_sleep_aborted == False:
        os.system("Rundll32.exe powrprof.dll,SetSuspendState Sleep")


def validate_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        return None

def abort_wifi_off(wifi_off_countdown, wifi_off_abort_button):
    global is_wifi_off_aborted, is_wifi_off_timer_on
    is_wifi_off_aborted = True
    is_wifi_off_timer_on = False
    wifi_off_countdown.configure(text="Wi-Fi Adapter OFF Aborted")
    messagebox.showinfo("Wi-Fi Adapter OFF Status", "Wi-Fi Adapter OFF Aborted")
    wifi_off_abort_button.configure(state="disabled")

def update_wifi_off_countdown(delay, wifi_off_countdown, root, wifi_off_abort_button):
    global is_wifi_off_aborted, is_wifi_off_timer_on
    if is_wifi_off_aborted:
        return

    is_wifi_off_timer_on = True
    if is_wifi_off_page:
        wifi_off_countdown.grid(row=1, column=0, pady=10)
    else:
        wifi_off_countdown.grid_remove()

    remaining_time = delay // 1000
    hours, remainder = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    wifi_off_countdown.configure(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")

    if delay > 0:
        root.after(1000, update_wifi_off_countdown, delay - 1000, wifi_off_countdown, root, wifi_off_abort_button)
    else:
        is_wifi_off_timer_on = False
        wifi_off_countdown.configure(text="Wi-Fi Adapter OFF")
        wifi_off_abort_button.configure(state="disabled")
        disable_wifi()

def wifi_off(wifi_off_entry, root, wifi_off_countdown, wifi_off_abort_button, shutdown_entry, restart_entry, sleep_entry):
    global is_wifi_off_aborted
    is_wifi_off_aborted = False

    global is_wifi_off_timer_on
    if is_wifi_off_timer_on:
        messagebox.showerror("Error", "Please wait for the current WIFI OFF process to complete or abort it before starting a new one.")
        return

    wifi_off_time = validate_time(wifi_off_entry.get())
    if wifi_off_time is None:
        messagebox.showerror("Error", "Please enter the time in the format HH:MM")
        return
    
    valid = wifi_off_check(shutdown_entry, restart_entry, sleep_entry, wifi_off_entry)
    if valid == False:
        return

    current_time = datetime.now()
    wifi_off_status = current_time.replace(hour=wifi_off_time.hour, minute=wifi_off_time.minute, second=0, microsecond=0)
    if wifi_off_status < current_time:
        wifi_off_status += timedelta(days=1)

    delay = (wifi_off_status - current_time).total_seconds() * 1000

    if messagebox.askyesno("WIFI Confirmation", f"Your WIFI Adapter will be turned off at {wifi_off_status.strftime('%H:%M')}"):
        wifi_off_abort_button.configure(state="normal")
        update_wifi_off_countdown(delay, wifi_off_countdown, root, wifi_off_abort_button)

def disable_wifi():
    if os.name == 'nt':
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "netsh", "interface set interface name=\"Wi-Fi\" admin=disable", None, win32con.SW_HIDE)
        except Exception as e:
            print(f"Error: {e}")
    else:
        os.system("nmcli radio wifi off")

    messagebox.showinfo("Wi-Fi Status", "Your Wi-Fi Adapter has been turned OFF. You could turn it back ON by clicking the Wi-Fi ON icon on the Home page.")

def wifi_off_thread(wifi_off_entry, root, wifi_off_countdown, wifi_off_abort_button, shutdown_entry, restart_entry, sleep_entry):
    wifi_off(wifi_off_entry, root, wifi_off_countdown, wifi_off_abort_button, shutdown_entry, restart_entry, sleep_entry)


def abort_wifi_on(wifi_on_countdown, wifi_on_abort_button):
    global is_wifi_on_aborted, is_wifi_on_timer_on
    is_wifi_on_aborted = True
    is_wifi_on_timer_on = False
    wifi_on_countdown.configure(text="Wi-Fi Adapter ON Aborted")
    messagebox.showinfo("Wi-Fi Adapter ON Status", "Wi-Fi Adapter ON Aborted")
    wifi_on_abort_button.configure(state="disabled")

def update_wifi_on_countdown(delay, wifi_on_countdown, root, wifi_on_abort_button):
    global is_wifi_on_aborted, is_wifi_on_timer_on
    if is_wifi_on_aborted:
        return

    is_wifi_on_timer_on = True

    if is_wifi_on_page:
        wifi_on_countdown.grid(row=1, column=0, pady=10)
    else:
        wifi_on_countdown.grid_remove()

    remaining_time = delay // 1000
    hours, remainder = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    wifi_on_countdown.configure(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")

    if delay > 0:
        root.after(1000, update_wifi_on_countdown, delay - 1000, wifi_on_countdown, root, wifi_on_abort_button)
    else:
        is_wifi_on_timer_on = False
        wifi_on_countdown.configure(text="Wi-Fi Adapter ON")
        wifi_on_abort_button.configure(state="disabled")
        enable_wifi()

def wifi_on(wifi_on_entry, root, wifi_on_switch, wifi_on_countdown, wifi_on_abort_button, shutdown_entry, restart_entry, sleep_entry):
    global is_wifi_on_aborted
    is_wifi_on_aborted = False

    global is_wifi_on_timer_on
    if is_wifi_on_timer_on:
        messagebox.showerror("Error", "Please wait for the current WIFI ON process to complete or abort it before starting a new one.")
        return

    if wifi_on_switch.get():
        enable_wifi()
        return 
    
    wifi_on_time = validate_time(wifi_on_entry.get())
    if wifi_on_time is None:
        messagebox.showerror("Error", "Please enter the time in the format HH:MM")
        return

    valid = wifi_off_check(shutdown_entry, restart_entry, sleep_entry, wifi_on_entry)
    if valid == False:
        return

    current_time = datetime.now()
    wifi_on_status = current_time.replace(hour=wifi_on_time.hour, minute=wifi_on_time.minute, second=0, microsecond=0)

    if wifi_on_status < current_time:
        wifi_on_status += timedelta(days=1)

    delay = (wifi_on_status - current_time).total_seconds() * 1000

    if messagebox.askyesno("WIFI Confirmation", f"Your WIFI Adapter will be turned on at {wifi_on_status.strftime('%H:%M')}"):
        wifi_on_abort_button.configure(state="normal")
        update_wifi_on_countdown(delay, wifi_on_countdown, root, wifi_on_abort_button)

def enable_wifi():
    if os.name == 'nt' and is_wifi_on_aborted == False:
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "netsh", "interface set interface name=\"Wi-Fi\" admin=enable", None, win32con.SW_HIDE)
        except Exception as e:
            print(f"Error: {e}")
    else:
        os.system("nmcli radio wifi on")

    messagebox.showinfo("Wi-Fi Status", "Your Wi-Fi Adapter has been turned on.")

def toggle_on_wifi_switch(wifi_on_entry, wifi_on_switch):
    if wifi_on_switch.get():
        wifi_on_entry.configure(state="disabled")
    else:
        wifi_on_entry.configure(state="normal")

def wifi_on_thread(wifi_on_entry, root, wifi_on_switch, wifi_on_countdown, wifi_on_abort_button, shutdown_entry, restart_entry, sleep_entry):
    wifi_on(wifi_on_entry, root, wifi_on_switch, wifi_on_countdown, wifi_on_abort_button, shutdown_entry, restart_entry, sleep_entry)

def hide_all(*widgets):
    for widget in widgets:
        widget.grid_remove()

def toggle_entry_and_shutdown(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, shutdown_text_label, shutdown_entry, shutdown_button, back_button, shutdown_abort_button):
    
    #hides the labelsl(icons)
    hide_all(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label)

    global is_shutdown_page
    is_shutdown_page = True

    global is_home_page
    is_home_page = False

    global is_restart_page
    is_restart_page = False

    global is_sleep_page
    is_sleep_page = False

    global is_wifi_off_page
    is_wifi_off_page = False

    global is_wifi_on_page
    is_wifi_on_page = False

    shutdown_text_label.grid(row=2, column=0, pady=10)
    shutdown_entry.grid(row=3, column=0, pady=10)
    shutdown_button.grid(row=4, column=0, pady=10)
    shutdown_abort_button.grid(row=5, column=0, pady=10)
    if is_shutdown_timer_on:
        shutdown_abort_button.configure(state="normal")
    else:
        shutdown_abort_button.configure(state="disabled")
    back_button.grid(row=6, column=0, pady=10)

def toggle_entry_and_restart(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, restart_text_label, restart_entry, restart_button, back_button, restart_abort_button):
    #hides the restart labels(icons)
    hide_all(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label)

    global is_restart_page
    is_restart_page = True

    global is_home_page
    is_home_page = False

    global is_shutdown_page
    is_shutdown_page = False

    global is_sleep_page
    is_sleep_page = False

    global is_wifi_off_page
    is_wifi_off_page = False

    global is_wifi_on_page
    is_wifi_on_page = False

    restart_text_label.grid(row=2, column=0, pady=10)
    restart_entry.grid(row=3, column=0, pady=10)
    restart_button.grid(row=4, column=0, pady=10)
    restart_abort_button.grid(row=5, column=0, pady=10)
    if is_restart_timer_on:
        restart_abort_button.configure(state="normal")
    else:
        restart_abort_button.configure(state="disabled")
    back_button.grid(row=6, column=0, pady=10)

def toggle_entry_and_sleep(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label,sleep_text_label, sleep_entry, sleep_button, back_button, sleep_abort_button):
    hide_all(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label)
    
    global is_sleep_page
    is_sleep_page = True

    global is_home_page
    is_home_page = False

    global is_shutdown_page
    is_shutdown_page = False

    global is_restart_page
    is_restart_page = False

    global is_wifi_off_page
    is_wifi_off_page = False

    global is_wifi_on_page
    is_wifi_on_page = False

    sleep_text_label.grid(row=2, column=0, pady=10)
    sleep_entry.grid(row=3, column=0, pady=10)
    sleep_button.grid(row=4, column=0, pady=10)
    sleep_abort_button.grid(row=5, column=0, pady=10)
    if is_sleep_timer_on:
        sleep_abort_button.configure(state="normal")   
    else:
        sleep_abort_button.configure(state="disabled")
    back_button.grid(row=6, column=0, pady=10)


def toggle_entry_and_wifi_off_control(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, wifi_off_text_label, wifi_off_entry, wifi_off_button, back_button, wifi_off_abort_button):
    hide_all(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label)
    
    global is_wifi_off_page
    is_wifi_off_page = True

    global is_home_page
    is_home_page = False

    global is_shutdown_page
    is_shutdown_page = False

    global is_restart_page
    is_restart_page = False

    global is_sleep_page
    is_sleep_page = False

    global is_wifi_on_page
    is_wifi_on_page = False

    wifi_off_text_label.grid(row=2, column=0, pady=10)
    wifi_off_entry.grid(row=3, column=0, pady=10)
    wifi_off_button.grid(row=4, column=0, pady=10)
    wifi_off_abort_button.grid(row=5, column=0, pady=10)
    if is_wifi_off_timer_on:
        wifi_off_abort_button.configure(state="normal")
    else:
        wifi_off_abort_button.configure(state="disabled")
    back_button.grid(row=6, column=0, pady=10)


def toggle_entry_and_wifi_on_control(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label, wifi_on_text_label, wifi_on_entry, wifi_on_button, back_button, wifi_on_switch, wifi_on_abort_button):
    hide_all(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label)

    global is_wifi_on_page
    is_wifi_on_page = True

    global is_home_page
    is_home_page = False

    global is_shutdown_page
    is_shutdown_page = False

    global is_restart_page
    is_restart_page = False

    global is_sleep_page
    is_sleep_page = False

    global is_wifi_off_page
    is_wifi_off_page = False

    wifi_on_text_label.grid(row=2, column=0, pady=10)
    wifi_on_entry.grid(row=3, column=0, pady=10)
    wifi_on_switch.grid(row=4, column=0, pady=10)
    wifi_on_button.grid(row=5, column=0, pady=10)
    wifi_on_abort_button.grid(row=6, column=0, pady=10)
    if is_wifi_on_timer_on:
        wifi_on_abort_button.configure(state="normal")
    else:
        wifi_on_abort_button.configure(state="disabled")
    back_button.grid(row=7, column=0, pady=10)

def go_back(shutdown_label, restart_label, sleep_label, wifi_off_label, wifi_on_label,
    shutdown_text_label, restart_text_label, sleep_text_label, wifi_off_text_label, wifi_on_text_label,
    shutdown_entry, restart_entry, sleep_entry, wifi_off_entry, wifi_on_entry,
    shutdown_button, restart_button, sleep_button, wifi_off_button, back_button, wifi_on_button, wifi_on_switch, shutdown_countdown, restart_countdown, sleep_countdown, wifi_off_countdown, wifi_on_countdown, shutdown_abort_button, restart_abort_button, sleep_abort_button, wifi_off_abort_button, wifi_on_abort_button):

    #updating home_page
    global is_home_page
    is_home_page = True
    
    global is_shutdown_page
    is_shutdown_page = False

    global is_restart_page
    is_restart_page = False

    global is_sleep_page
    is_sleep_page = False

    global is_wifi_off_page
    is_wifi_off_page = False

    global is_wifi_on_page
    is_wifi_on_page = False

    # Hide all widgets
    hide_all(shutdown_text_label, restart_text_label, sleep_text_label, wifi_off_text_label, wifi_on_text_label, shutdown_entry, restart_entry, sleep_entry, wifi_off_entry, wifi_on_entry,shutdown_button, restart_button, sleep_button, wifi_off_button, back_button, wifi_on_button, wifi_on_switch, shutdown_countdown, restart_countdown, sleep_countdown, wifi_off_countdown, wifi_on_countdown, shutdown_abort_button, restart_abort_button, sleep_abort_button, wifi_off_abort_button, wifi_on_abort_button)
    
    # Show the labels and icons
    shutdown_label.grid(row=1, column=0, pady=10)
    restart_label.grid(row=2, column=0, pady=10)
    sleep_label.grid(row=3, column=0, pady=10)
    wifi_off_label.grid(row=4, column=0, pady=10)
    wifi_on_label.grid(row=5, column=0, pady=10)

def restart_sleep_entry(restart_entry, sleep_entry):
    #check if the restart and sleep entry is empty
    global is_shutdown_timer_on
    if is_shutdown_timer_on:
        restart_entry.configure(state="disabled")
        sleep_entry.configure(state="disabled")
    else:
        restart_entry.configure(state="normal")
        sleep_entry.configure(state="normal")

def shutdown_sleep_entry(shutdown_entry, sleep_entry):
    #check if the shutdown and sleep entry is empty
    global is_restart_timer_on
    if is_restart_timer_on:
        shutdown_entry.configure(state="disabled")
        sleep_entry.configure(state="disabled")
    else:
        shutdown_entry.configure(state="normal")
        sleep_entry.configure(state="normal")

def restart_shutdown_entry(restart_entry, shutdown_entry):
    #check if the restart and shutdown entry is empty
    global is_sleep_timer_on
    if is_sleep_timer_on:
        restart_entry.configure(state="disabled")
        shutdown_entry.configure(state="disabled")
    else:
        restart_entry.configure(state="normal")
        shutdown_entry.configure(state="normal")

def wifi_off_check(shutdown_entry, restart_entry, sleep_entry, wifi_off_entry):
    global is_shutdown_timer_on
    global is_restart_timer_on
    global is_sleep_timer_on

    wifi_off_time = datetime.strptime(wifi_off_entry.get(), "%H:%M")

    if is_shutdown_timer_on:
        shutdown_time = datetime.strptime(shutdown_entry.get(), "%H:%M")
        if wifi_off_time >= shutdown_time:
            messagebox.showerror("Error", "Please enter a time before the shutdown time")
            wifi_off_entry.delete(0, 'end')
            return False
        
    elif is_restart_timer_on:     
        restart_time = datetime.strptime(restart_entry.get(), "%H:%M")
        if wifi_off_time >= restart_time:
            messagebox.showerror("Error", "Please enter a time before the restart time")
            wifi_off_entry.delete(0, 'end')
            return False

    elif is_sleep_timer_on:
        sleep_time = datetime.strptime(sleep_entry.get(), "%H:%M")
        if wifi_off_time >= sleep_time:
            messagebox.showerror("Error", "Please enter a time before the sleep time")
            wifi_off_entry.delete(0, 'end')
            return False
        

def wifi_on_check(shutdown_entry, restart_entry, sleep_entry, wifi_on_entry):
    global is_shutdown_timer_on
    global is_restart_timer_on
    global is_sleep_timer_on

    wifi_on_time = datetime.strptime(wifi_on_entry.get(), "%H:%M")

    if is_shutdown_timer_on:
        shutdown_time = datetime.strptime(shutdown_entry.get(), "%H:%M")
        if wifi_on_time >= shutdown_time:
            messagebox.showerror("Error", "Please enter a time before the shutdown time")
            wifi_on_entry.delete(0, 'end')
            return False
    elif is_restart_timer_on:
        restart_time = datetime.strptime(restart_entry.get(), "%H:%M")
        if wifi_on_time >= restart_time:
            messagebox.showerror("Error", "Please enter a time before the restart time")
            wifi_on_entry.delete(0, 'end')
            return False
    elif is_sleep_timer_on:
        sleep_time = datetime.strptime(sleep_entry.get(), "%H:%M")
        if wifi_on_time >= sleep_time:
            messagebox.showerror("Error", "Please enter a time before the sleep time")
            wifi_on_entry.delete(0, 'end')
            return False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)