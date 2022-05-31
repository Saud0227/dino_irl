import tkinter as tk
from time import sleep
from tkinter import font

from serviceH import configHandler, rectHandler

from vectors import vector


from PIL import Image,ImageTk


class tkInterface:


    def __init__(self, _tk, _debug:bool = False):
        self.tkRoot = _tk.Tk()
        self._alive = True
        self.unaliveTasks = []


        if not _debug:
            self.tkRoot.attributes('-fullscreen', True)

        self.tkRoot.bind('<Escape>',lambda e: self.unalive())
        self.tkRoot.bind('<FocusOut>',lambda e: self.unalive())

        self.root = _tk.Canvas(self.tkRoot, width=int(self.tkRoot.winfo_screenwidth()),height=int(self.tkRoot.winfo_screenwidth()), bg="white")
        self.root.pack()

        self.itemIdIndex = 0
        self.itemIdPrefix = "CanvasRootObj"

        #---------------------------------------
        self.rectMode = configHandler("rectmode")
        self.rectMode.state = 0
        self.rectMode.acceptedValue = ["onecorner", "center", "twocorner"]
        self.rectMode.verify()

        #---------------------------------------


        self._fill = self._rgb_to_hex((255,255,255))
        self._stroke = self._rgb_to_hex((0,0,0))
        self._strokeW = 2


        #---------------------------------------

        self.textTypes = {}
        self.textTypes["middle"] = {
            "rgb":self._rgb_to_hex((200,200,200)),
            "anchor":"w",
            "styling":('Helvetica','12')
        }
        self.textTypes["standard"] = {
            "rgb":self._rgb_to_hex((200,200,200)),
            "anchor":"nw",
            "styling":('Helvetica','12')
        }
        self.textTypes["title"] = {
            "rgb":self._rgb_to_hex((0,0,0)),
            "anchor":"center",
            "styling":('Helvetica','30', 'bold')
        }
        self.textTypes["subtitle"] = {
            "rgb":self._rgb_to_hex((0,0,0)),
            "anchor":"center",
            "styling":('Helvetica','26')
        }



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
        print(self.getSize())
        for itm in self.unaliveTasks:
            itm()
        self.tkRoot.destroy()


    def alive(self):
        return self._alive

    def _rgb_to_hex(self, rgb):
        return ("#" + ('%02x%02x%02x' % rgb))

    def fill(self, r: int, g: int, b: int):
        values = [r,g,b]
        done = [""]*3
        for i, itm  in enumerate(values):
            itm = int(itm)
            if itm < 0:
                itm = 0
            if itm > 255:
                itm = 255
            done[i] = itm
        rgb  = (done[0], done[1], done[2])
        self._fill = self._rgb_to_hex(rgb)

    def stroke(self, r: int, g: int, b: int):
        values = [r,g,b]
        done = [""]*3
        for i, itm  in enumerate(values):
            itm = int(itm)
            if itm < 0:
                itm = 0
            if itm > 255:
                itm = 255
            done[i] = itm
        rgb  = (done[0], done[1], done[2])
        self._stroke = self._rgb_to_hex(rgb)


    def strokeW(self, l: int):
        if l < 0:
            l = 0
        self._strokeW = l

    def _getItemId(self):
        id = self.itemIdPrefix + str(self.itemIdIndex)
        self.itemIdIndex+=1
        return id


    def _rectPolyDraw(self, posL):
        id = self._getItemId()
        if self._strokeW > 0:
            self.root.create_polygon(posL[0],posL[1],posL[2],posL[3],posL[4],posL[5],posL[6],posL[7], fill = self._fill, outline = self._stroke, width = self._strokeW, tags=id)
        else:
            self.root.create_polygon(posL[0],posL[1],posL[2],posL[3],posL[4],posL[5],posL[6],posL[7], fill = self._fill, tags=id)
        return id



    def rect(self, x1, y1, x2, y2, draw = True):

        processed = [int(x1),int(y1), int(x2), int(y2)]

        #Rect mode determents draw mode
        if draw:
            rectObj = rectHandler(processed, self.rectMode.getState(), self._rectPolyDraw)
        else:
            rectObj = rectHandler(processed, self.rectMode.getState())
        return rectObj


    def line(self, x1, y1, x2, y2, draw = True):
        id = self._getItemId()
        self.root.create_line(x1, y1, x2, y2, fill = self._stroke, width = self._strokeW, smooth=True, tags=id)
        return id



    def text(self, x1: int, y1: int, text: str, style: str):
        try:
            textOptions = self.textTypes[style]
        except KeyError:
            textOptions = self.textTypes["standard"]
        id = self.root.create_text(x1, y1, text=text, font=textOptions["styling"], fill=textOptions["rgb"],anchor=textOptions["anchor"])


    def getSize(self):
        sizeObj = vector(self.root.winfo_width(),self.root.winfo_height())
        if sizeObj.x == sizeObj.y:
            sizeObj = vector(1920, 1080)
        return sizeObj


    @staticmethod
    def checkColRect(a, b):
        return rectHandler.checkCollision(a, b)

    @staticmethod
    def assetHandle(list):
        for i in list:
            list[i] = ImageTk.PhotoImage(Image.open(list[i]))
        return list


if __name__ == '__main__':
    a = tkInterface(tk)
    col = False
    a.strokeW(-2)
    while a.alive():
        a.strokeW(-2)
        a.rectMode.changeVal("twocorner")

        a.fill(0,0,255)
        rectH1 = a.rect(500, 500, 100, 100)

        mPos = a.getMousePos()
        a.rectMode.changeVal("center")

        if col:
            a.fill(255,0,0)
        else:
            a.fill(0,255,0)
        rectH2 = a.rect(mPos.x, mPos.y, 50, 50)

        col = a.checkColRect(rectH1, rectH2)
        a.text(mPos.x, mPos.y, "MOUSE", "standard")

        a.strokeW(5)
        a.line(300, 300, mPos.x, mPos.y)
        # canvas
        a.update()
        #sleep(3)

        a.postloop()

        #sleep(3)

        sleep(0.005)

