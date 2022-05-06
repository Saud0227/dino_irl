import tkinter as tk

root = tk.Tk()

can = tk.Canvas(root, width=200, height=200)



can.create_line(10,10,20,20, fill='red')
root.mainloop()