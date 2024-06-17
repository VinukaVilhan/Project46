import tkinter as tk
import ttkbootstrap as ttk

# Create a window
root = tk.Tk()
root.geometry('300x100')

# Create a Meter widget
meter = ttk.Meter(root, 
                  metersize=180, 
                  padding=5, 
                  amountused=25, 
                  metertype="semi", 
                  subtext="miles per hour", 
                  interactive=True)
meter.pack()

root.mainloop()
