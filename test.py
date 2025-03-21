import tkinter as tk
 
root = tk.Tk()
class App:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.check_var = tk.IntVar()
        self.check_button = tk.Checkbutton(self.frame,
            command=self.check_status,
            variable=self.check_var,
            text="Text")
 
        self.check_button.pack()
 
    def check_status(self):
        print(self.check_var.get())
 
app = App(root)
app2 = App(root)
root.mainloop()