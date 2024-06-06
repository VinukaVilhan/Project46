import tkinter as tk

def on_button_click():
    print("Button clicked")
    user_text=entry.get()
    label.config(text=f"You clicked the button, {user_text}!")

#create the main window
root = tk.Tk()
root.title("App")


# create a label
label = tk.Label(root, text="Welcome to my App")
label.pack(pady=100)
label.pack(padx=100)

# create an entry widget
entry = tk.Entry(root)
entry.pack(pady=20)
entry.pack(padx=20)

#create a button 
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=10)
button.pack(padx=10)

root.mainloop()