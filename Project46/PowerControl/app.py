import tkinter as tk
from tkinter import messagebox
import time
import os
from datetime import datetime

# Parse the time entered by the user
def shutdown():
        shutdown_time = entry.get()
        try:
            #parse the time entered by the user, gets default date
            shutdown_time = datetime.strptime(shutdown_time, "%H:%M")
            current_time = datetime.now()
            # set the shutdown time to the current date whiel keeping the time
            shutdown_time = current_time.replace(hour=shutdown_time.hour, minute=shutdown_time.minute, second=0, microsecond=0)

            #if the shutdown time is less than the current time, set it for the next day
            if shutdown_time < current_time:
                shutdown_time = shutdown_time.replace(day=shutdown_time.day + 1)

            delay = (shutdown_time - current_time)

            #conformation
            if messagebox.askyesno("Confirmation", f"Your computer will shutdown at {shutdown_time.strftime('%H:%M')}"):
                 #if the user confirms, the computer will shutdown. After the delay the fucntion will be called and the process will proceed
                 root.after(int(delay*1000), shutdown)

        except ValueError:
            messagebox.showerror("Error", "Please enter the time in the format HH:MM")

def shutdown_computer():
     if os.name == 'nt':
          os.system("Shutdown /s /t 1")
     else:
          os.system("shutdown -h now")

def on_button_click():
     print("Button clicked")
     user_text = entry.get()


root = tk.Tk()
root.title("Power Control")


# label
label = tk.label(root, text="Enter shutdown time (HH:MM):")
label.pack(pady=20)
label.pack(padx=20)

# entry widget for timwe
entry = tk.Entry(root)
entry.pack(pady=20)
entry.pack(padx=20)

# create a button to schedule shutdown
button = tk.Button(root, text = "Schedule Shutdown", command=shutdown)
button.pack(pady=10)
button.pack(padx=10)

root.mainloop()