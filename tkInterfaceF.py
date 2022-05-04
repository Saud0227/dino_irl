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
    
    
    def rect(x, y, xS, yS):
        