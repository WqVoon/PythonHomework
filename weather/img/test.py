import tkinter as tk

top = tk.Tk()
top.geometry('300x300')
label = tk.Label(top)

def action():
    global label
    global top
    img = tk.PhotoImage(file='lei.gif')
    print(img)
    label.configure(image = img)
    label.image = img

btn = tk.Button(top, text='Click', command=action)
btn.grid(sticky='w')
label.grid(sticky='w')

top.mainloop()