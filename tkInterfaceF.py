import tkinter as tk
from time import sleep

from serviceH import configHandler

from vectors import vector

class tkInterface:


    def __init__(self, _tk):
        self.tkroot = _tk.Tk()
        self._alive = True
        self.root = _tk.Canvas(self.tkroot, width=1536,height=864, bg="white")
        self.tkroot.attributes('-fullscreen', True)
        self.tkroot.bind('<Escape>',lambda e: self.unalive())
        
        #---------------------------------------
        self.rectMode = configHandler("rectmode")
        self.rectMode.state = 0
        self.rectMode.aceptedValue = ["corner, center, allcorners"]
        self.rectMode.verify()
        
        
        
        #---------------------------------------



    def update(self):
        self.tkroot.update()
        
    def preLoop(self):
        self.root.delete("all")
    
    def unalive(self):
        self._alive = False
        self.tkroot.destroy()
    
    
    def alive(self):
        return self._alive
    
    
    def _rectPolyDraw(self, posL):
        id = self.root.create_polygon(posL[0],posL[1],posL[2],posL[3],posL[4],posL[5],posL[6],posL[7], fill='red')
        return(id)
    
    
    
    def rect(self, *args):
        ccr = ["iiii", "vii", "vv"]
        code = ""
        for i in args:
            if type(i) == int:
                code+="i"
            elif type(i) == vector:
                code+="v"
            else:
                raise ValueError("Non suported input (use int or vector)")
            
        try:
            inType = ccr.index(code)
        except ValueError:
            return False
        
        
        if inType == 0:
            
            corn = [args[0],args[1],args[0]+args[2],args[1],args[0]+args[2],args[1]+args[3],args[0],args[1]+args[3]]
            print(corn)
            id = self._rectPolyDraw(corn)
            
            return id
           
        
        
        
        


if __name__ == '__main__':
    a = tkInterface(tk)
    while a.alive():
        # a.preLoop()
        id = a.rect(500, 500,100,100)
        # canvas
        sleep(5)
        print("!")
        a.update()
    
    