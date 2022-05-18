from time import sleep
import tkinter as Tk
from vectors import vector
from tkInterfaceF import tkInterface



ground = 700
jumpTime = 5


height = 90
width = 90


a = tkInterface(Tk)
if __name__ == '__main__':
    while a.alive():






        a.line(0,700,1560,700)
        a.update()


        sleep(0.05)
        a.postloop()





