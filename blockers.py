


class blocker:

    typeYVal = {}
    typeXSize = {}
    typeYSize = {}
    typeAssets = {}
    moveSpeed = 0

    typeAssets = {}

    def __init__(self, _type:int, _x: int):
        self.type = _type
        self.x = _x
        self.y = self.typeYVal[self.type]
        self.xS = self.typeXSize[self.type]
        self.yS = self.typeYSize[self.type]

        self.asset = self.typeAssets[self.type]

        self.currentCollision = None


        self.killMe = False
        self.checkCol = False



    def update(self, a, aT:int, active=True):
        if self.killMe:
            return None
        if active:
            self.x -= self.moveSpeed + self.moveSpeed*0.5*int(self.type > 1)


        if self.x < a.getSize().x:
            if self.asset == True:
                if aT < 5:
                    a.drawImage(self.x, self.y-self.yS, "fly1")
                else:
                    a.drawImage(self.x, self.y-self.yS, "fly2")

            else:
                a.drawImage(self.x, self.y-self.yS, self.asset)
        if self.x < a.getSize().x/2:
            a.fill(255,0,0)
            self.checkCol = True
            self.currentCollision = a.rect(self.x, self.y-self.yS, self.xS, self.yS, False)


        if self.x < self.xS*-1:
            self.killMe = True
            #print("Kill me")
