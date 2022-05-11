from vectors import vector

class configHandler:
    
    

    def __init__(self, _display_name):
        self.display_name = _display_name
        self.state = None
        self.aceptedValue = []
        self.active = False
        
        
    def checkAcpeted(self, value):
        try:
            valI = self.aceptedValue.index(value.lower())
            return valI
        except ValueError:
            return False
    
    def changeVal(self, value):
        newVal = self.checkAcpeted(value)
        if newVal != False:
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
            return self.aceptedValue[self.state]
        else:
            raise ValueError("configHandler not verified")

    def getName(self):
        if self.active:
            return self.display_name
        else:
            raise ValueError("configHandler not verified")
    def verify(self):
        v = (self.state != None and len(self.aceptedValue) > 1)
        self.active = v
        return v
            



class rectHandler:
    
    
    def __init__(self, dat, datParcing, color = null):
        print("!")
        self.corner = [""]*4
        
        parcing_options = [self._setupOneC, self._setupCent, self._setupTwoC]
        
        parcing_options[datParcing](dat)
        
        #self.color = color  tmp
        
    
    
    def getDrawData(self, id):
        exportList = []
        self.cId = id
        for i in range(len(self.corner)):
            exportList.append(self.corner[i].x)
            exportList.append(self.corner[i].y)
        return exportList
    
    
    def _setupOneC(dat):
        self.corner[0] = vector(dat[0], dat[1])
        self.corner[1] = vector(dat[0] + dat[2], dat[1])
        self.corner[2] = vector(dat[0] + dat[2], dat[1] + dat[3])
        self.corner[3] = vector(dat[0], dat[1] + dat[3])
        
    def _setupCent(dat):
        xoff = dat[2]/2
        yoff = dat[3]/2
        self.corner[0] = vector(dat[0] - xoff, dat[1] - yoff)
        self.corner[1] = vector(dat[0] + xoff, dat[1] - yoff)
        self.corner[2] = vector(dat[0] + xoff, dat[1] + yoff)
        self.corner[3] = vector(dat[0] - xoff, dat[1] + yoff)
        
    def _setupTwoC(dat):
        
        tmpCorner = [""]*4
        tmpCorner[0] = vector(dat[0], dat[1])
        tmpCorner[1] = vector(dat[2], dat[1])
        tmpCorner[2] = vector(dat[2], dat[3])
        tmpCorner[3] = vector(dat[0], dat[3])
        
        checkX = False
        checkY = False
        
        while checkX and checkY:
            checkX = False
            checkY = False
            if tmpCorner[0].x > tmpCorner[1].x:
                extratmp = [""]*4
                extratmp[0] = tmpCorner[1]
                extratmp[1] = tmpCorner[0]
                extratmp[2] = tmpCorner[3]
                extratmp[3] = tmpCorner[2]
                tmpCorner = extratmp
            else:
                checkX = True
            
            if tmpCorner[0].y > tmpCorner[2].y1:
                extratmp = [""]*4
                extratmp[0] = tmpCorner[3]
                extratmp[1] = tmpCorner[2]
                extratmp[2] = tmpCorner[1]
                extratmp[3] = tmpCorner[0]
                tmpCorner = extratmp
            else:
                checkY = True
        self.corner = tmpCorner
        
if __name__ == '__main__':
    a = configHandler("Test")
    
    a.state = 0
    a.aceptedValue = ["yes", "no", "fuck"]
    
    
    a.verify()
    
    print(a.getName())
    print(a.getState(), a.getStateStr())

    
    
    
    
    
    a.changeVal("fuck")

    print(a.getState(), a.getStateStr())
    