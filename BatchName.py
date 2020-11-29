import tkinter as tk
from tkinter import ttk
def create_acc():
    root = tk.Tk()
    root.title('Batch Name')
    root.geometry('500x250')
    root.resizable(0, 0)
    batch_names = ''
    def batch():
        n.get()
        print(n.get())
        batch_names.join(n.get())
        
        root.destroy()



    ttk.Label(root, text="Name of new Batch :",
              font=("Times New Roman", 10)).place(x=75,y=55)

    n = tk.StringVar()
    name = ttk.Entry(root, textvariable=n).place(x=190,y=55)
    new_batch = ttk.Button(root, text='Create New Batch',command=batch).place(x=195, y=135)
    root.mainloop()

    return batch_names


def create_acc_call():
    global batch_names
    batch_name = create_acc()
    print(batch_name)
    return batch_name