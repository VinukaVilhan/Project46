import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime, timedelta

# Parse the time entered by the user
def shutdown():
    shutdown_time = entry.get()
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
        if messagebox.askyesno("Confirmation", f"Your computer will shutdown at {shutdown_time.strftime('%H:%M')}"):
            # If the user confirms, the computer will shutdown. After the delay the function will be called and the process will proceed
            root.after(int(delay), shutdown_computer)

    except ValueError:
        messagebox.showerror("Error", "Please enter the time in the format HH:MM")

def shutdown_computer():
    if os.name == 'nt':
        os.system("Shutdown /s /t 1")
    else:
        os.system("shutdown -h now")

#created a window frame object
root = tk.Tk()
root.title("Power Control")

#change the bcakground color of the window
root.configure(bg='lightblue')

# Label
label = tk.Label(root, text="Enter shutdown time (HH:MM):")
label.pack(pady=20)
label.pack(padx=20)

# Entry widget for time
entry = tk.Entry(root)
entry.pack(pady=20)
entry.pack(padx=20)

# Create a button to schedule shutdown
button = tk.Button(root, text="Schedule Shutdown", command=shutdown)
button.pack(pady=10)
button.pack(padx=10)

root.mainloop()
