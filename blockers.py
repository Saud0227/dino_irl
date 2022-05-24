


class blocker:

    typeYVal = {}
    typeXSize = {}
    typeYSize = {}
    moveSpeed = 0

    typeAssets = {}

    def __init__(self, _type:int, _x: int):
        self.type = _type
        self.x = _x
        self.y = self.typeYVal[self.type]
        self.xS = self.typeXSize[self.type]
        self.yS = self.typeYSize[self.type]

        self.currentCollision = None


        self.killMe = False



    def update(self, a):
        if self.killMe:
            return None
        self.x -= self.moveSpeed
        if self.x < a.getSize().x:
            pass
            #display graphic
        #if self.x < a.getSize().x/2:
        if self.x < a.getSize().x:
            a.fill(255,0,0)
            self.currentCollision = a.rect(self.x, self.y-self.yS, self.xS, self.yS, True)


        if self.x < self.xS*-1:
            self.killMe = True
            print("Kill me")
