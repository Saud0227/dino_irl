from time import sleep
import tkinter as Tk

from vectors import vector


from tkInterfaceF import tkInterface


a = tkInterface(Tk)

while a.alive():
    a.preLoop()

    a.update()


