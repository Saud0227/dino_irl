import tkinter as tk
from time import sleep

from serviceH import configHandler, rectHandler

from vectors import vector

class tkInterface:


    def __init__(self, _tk):
        self.tkroot = _tk.Tk()
        self._alive = True
        self.root = _tk.Canvas(self.tkroot, width=1536,height=864, bg="white")
        self.root.pack()
        self.tkroot.attributes('-fullscreen', True)
        self.tkroot.bind('<Escape>',lambda e: self.unalive())
        
        self.itemIdIndex = 0
        self.itemIdPrefix = "CanvRootObj"
        
        #---------------------------------------
        self.rectMode = configHandler("rectmode")
        self.rectMode.state = 0
        self.rectMode.aceptedValue = ["onecorner", "center", "twocorner"]
        self.rectMode.verify()
        print(self.rectMode.active)
        
        
        
        #---------------------------------------



    def update(self):
        self.tkroot.update()
        
    def postloop(self):
        self.root.delete("all")
        self.itemIdIndex = 0
    
    def unalive(self):
        self._alive = False
        self.tkroot.destroy()
    
    
    def alive(self):
        return self._alive
    
    
    def _getItemId(self):
        id = self.itemIdPrefix + str(self.itemIdIndex)
        self.itemIdIndex+=1
        return id
        
    
    def _rectPolyDraw(self, rectHand):
        id = self._getItemId()
        posL = rectHand.getDrawData(id)
        obj = self.root.create_polygon(posL[0],posL[1],posL[2],posL[3],posL[4],posL[5],posL[6],posL[7], fill='red', tags=id)
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
        
        processed = []
        
        if inType == 0:
            for i in args:
                processed.append(i)
        if inType == 2:
            i = 0
            for itm in args:
                processed.append(itm.x)
                i+=1
                processed.append(itm.y)
                i+=1
        
        print(processed)
        
        rectObj = rectHandler(processed, self.rectMode.state())
        
        #print(corn)
        #id = self._rectPolyDraw(corn)
        
        #return id


if __name__ == '__main__':
    a = tkInterface(tk)
    dX = 550
    while a.alive():
        a.rectMode.changeVal("twocorner")
        print(a.rectMode.getState())
        id = a.rect(500, 500, dX, 100)
        
        
        
        dX+=5
        # canvas
        a.update()
        sleep(3)

        a.postloop()
    
        a.update()
        sleep(3)
       
        sleep(0.01)
    
    