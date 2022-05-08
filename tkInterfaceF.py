import tkinter as tk
from time import sleep

from serviceH import configHandler

from vectors import vector

class tkInterface:


    def __init__(self, _tk):
        self.tkroot = _tk.Tk()
        self._alive = True
        self.root = _tk.Canvas(self.tkroot, width=1536,height=864, bg="white")
        self.root.pack()
        self.tkroot.attributes('-fullscreen', True)
        self.tkroot.bind('<Escape>',lambda e: self.unalive())
        
        #---------------------------------------
        self.rectMode = configHandler("rectmode")
        self.rectMode.state = 0
        self.rectMode.aceptedValue = ["onecorner", "center", "twocorner"]
        self.rectMode.verify()
        print(self.rectMode.active)
        
        
        
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
        ccr = ["iiii", "vv"]
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
        
        print(self.rectMode.getState())
        
        
        
        if self.rectMode.getState() == 0:
            
            if inType == 0:
                corn = [args[0],args[1],args[0]+args[2],args[1],args[0]+args[2],args[1]+args[3],args[0],args[1]+args[3]]

            elif inType == 1:
                corn = [args[0].x,args[0].y,args[0].x+args[1].x,args[0].y,args[0].x+args[1].x,args[0].y+args[1].y,args[0].x,args[0].y+args[1].y]
        
        elif self.rectMode.getState() == 1:
            
            if inType == 0:
                corn = [(args[0]-args[2]/2),(args[1]-args[3]/2),(args[0]+args[2]/2),(args[1]-args[3]/2),(args[0]+args[2]/2),(args[1]+args[3]/2),(args[0]-args[2]/2),(args[1]+args[3]/2)]

            elif inType == 1:
                corn = [(args[0].x-args[1].x/2),(args[0].y-args[1].y/2),(args[0].x+args[1].x/2),(args[0].y-args[1].y/2),(args[0].x+args[1].x/2),(args[0].y+args[1].y/2),(args[0].x-args[1].x/2),(args[0].y+args[1].y/2)]
        elif self.rectMode.getState() == 2:
            
            if inType == 0:
                corn = [args[0],args[1],args[2], args[1],args[2],args[3],args[0],args[3]]
                
            elif inType == 1:
                corn = [args[0].x,args[0].y,args[1].x, args[0].y,args[1].x,args[1].y,args[0].x,args[1].y]
            
        
        print(corn)
        id = self._rectPolyDraw(corn)
        
        return id


if __name__ == '__main__':
    a = tkInterface(tk)
    dX = 500
    while a.alive():
        a.preLoop()
        a.rectMode.changeVal("twocorner")
        print(a.rectMode.getState())
        id = a.rect(500, 500, dX, 100)
        dX+=5
        # canvas
        print("!")
        a.update()
        sleep(0.01)
    
    