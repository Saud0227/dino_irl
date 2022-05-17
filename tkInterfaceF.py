import tkinter as tk
from time import sleep

from serviceH import configHandler, rectHandler

from vectors import vector

class tkInterface:


    def __init__(self, _tk):
        self.tkRoot = _tk.Tk()
        self._alive = True

        self.tkRoot.attributes('-fullscreen', True)
        self.tkRoot.bind('<Escape>',lambda e: self.unalive())

        self.root = _tk.Canvas(self.tkRoot, width=int(self.tkRoot.winfo_screenwidth()),height=int(self.tkRoot.winfo_screenwidth()), bg="white")
        self.root.pack()

        self.itemIdIndex = 0
        self.itemIdPrefix = "CanvasRootObj"

        #---------------------------------------
        self.rectMode = configHandler("rectmode")
        self.rectMode.state = 0
        self.rectMode.acceptedValue = ["onecorner", "center", "twocorner"]
        self.rectMode.verify()
        print(self.rectMode.active)

        #---------------------------------------

    def getMousePos(self):
        return vector(self.tkRoot.winfo_pointerx(),self.tkRoot.winfo_pointery())

    def update(self):
        if not self._alive:
            return None
        self.tkRoot.update()

    def postloop(self):
        if not self._alive:
            return None
        self.root.delete("all")
        self.itemIdIndex = 0

    def unalive(self):
        self._alive = False
        self.tkRoot.destroy()


    def alive(self):
        return self._alive


    def _getItemId(self):
        id = self.itemIdPrefix + str(self.itemIdIndex)
        self.itemIdIndex+=1
        return id


    def _rectPolyDraw(self, posL):
        id = self._getItemId()
        obj = self.root.create_polygon(posL[0],posL[1],posL[2],posL[3],posL[4],posL[5],posL[6],posL[7], fill='red', tags=id)
        return(id)



    def rect(self, *args):

        #Detects input type
        processed = [""]*4
        for i,itm in enumerate(args):
            if type(itm) == int:
                processed[i] = int(itm)
            else:
                raise ValueError("Non supported input (use int or vector)")




        #Rect mode determens draw mode
        rectObj = rectHandler(processed, self.rectMode.getState(), self._rectPolyDraw)
        return rectObj


if __name__ == '__main__':
    a = tkInterface(tk)
    while a.alive():
        a.rectMode.changeVal("onecorner")
        rectH1 = a.rect(500, 500, 100, 100)

        mPos = a.getMousePos()
        a.rectMode.changeVal("center")
        rectH2 = a.rect(mPos.x, mPos.y, 50, 50)

        print(rectHandler.checkCollision(rectH1, rectH2))
        # canvas
        a.update()
        #sleep(3)

        a.postloop()

        #sleep(3)

        sleep(0.01)

