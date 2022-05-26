from vectors import vector

class configHandler:



    def __init__(self, _display_name):
        self.display_name = _display_name
        self.state = None
        self.acceptedValue = []
        self.active = False


    def checkAccepted(self, value):
        try:
            valI = self.acceptedValue.index(value.lower())
            return valI
        except ValueError:
            return -1

    def changeVal(self, value):
        newVal = self.checkAccepted(value)
        if newVal > -1:
            self.state = newVal
        else:
            print(f"{value} not known")

    def getState(self):
        if self.active:
            return self.state
        else:
            raise ValueError("configHandler not verified")

    def getStateStr(self):
        if self.active:
            return self.acceptedValue[self.state]
        else:
            raise ValueError("configHandler not verified")

    def getName(self):
        if self.active:
            return self.display_name
        else:
            raise ValueError("configHandler not verified")
    def verify(self):
        v = (self.state != None and len(self.acceptedValue) > 1)
        self.active = v
        return v




class rectHandler:




    @staticmethod
    def checkCollision(r1,r2):
        # Box vs box collision check
        return (
        r1.corner[0].x<r2.corner[2].x
        and r1.corner[2].x > r2.corner[0].x
        and r1.corner[0].y<r2.corner[2].y
        and r1.corner[2].y > r2.corner[0].y
        )



    def __init__(self, dat, datParsing, drawFunc = None):

        self.corner = [""]*4

        parsing_options = [self._setupOneC, self._setupCent, self._setupTwoC]

        parsing_options[datParsing](dat)

        if drawFunc is not None:
            self.cId = drawFunc(self.getDrawData())

    def getDrawData(self):
        exportList = []
        for i in range(len(self.corner)):
            exportList.append(self.corner[i].x)
            exportList.append(self.corner[i].y)
        return exportList


    def _setupOneC(self,dat):
        self.corner[0] = vector(dat[0], dat[1])
        self.corner[1] = vector(dat[0] + dat[2], dat[1])
        self.corner[2] = vector(dat[0] + dat[2], dat[1] + dat[3])
        self.corner[3] = vector(dat[0], dat[1] + dat[3])

    def _setupCent(self,dat):
        xOff = dat[2]/2
        yOff = dat[3]/2
        self.corner[0] = vector(dat[0] - xOff, dat[1] - yOff)
        self.corner[1] = vector(dat[0] + xOff, dat[1] - yOff)
        self.corner[2] = vector(dat[0] + xOff, dat[1] + yOff)
        self.corner[3] = vector(dat[0] - xOff, dat[1] + yOff)

    def _setupTwoC(self,dat):

        tmpCorner = [""]*4
        tmpCorner[0] = vector(dat[0], dat[1])
        tmpCorner[1] = vector(dat[2], dat[1])
        tmpCorner[2] = vector(dat[2], dat[3])
        tmpCorner[3] = vector(dat[0], dat[3])

        checkX = True
        checkY = True

        while checkX or checkY:
            checkX = True
            checkY = True
            if tmpCorner[0].x > tmpCorner[1].x:
                extraTmp = [""]*4
                extraTmp[0] = tmpCorner[1]
                extraTmp[1] = tmpCorner[0]
                extraTmp[2] = tmpCorner[3]
                extraTmp[3] = tmpCorner[2]
                tmpCorner = extraTmp
            else:
                checkX = False

            if tmpCorner[0].y > tmpCorner[2].y:
                extraTmp = [""]*4
                extraTmp[0] = tmpCorner[3]
                extraTmp[1] = tmpCorner[2]
                extraTmp[2] = tmpCorner[1]
                extraTmp[3] = tmpCorner[0]
                tmpCorner = extraTmp
            else:
                checkY = False
        self.corner = tmpCorner



if __name__ == '__main__':
    a = configHandler("Test")

    a.state = 0
    a.acceptedValue = ["yes", "no", "fuck"]


    a.verify()

    print(a.getName())
    print(a.getState(), a.getStateStr())






    a.changeVal("fuck")

    print(a.getState(), a.getStateStr())
