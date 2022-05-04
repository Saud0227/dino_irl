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
            
            
            
if __name__ == '__main__':
    a = configHandler("Test")
    
    a.state = 0
    a.aceptedValue = ["yes", "no", "fuck"]
    
    
    a.verify()
    
    print(a.getName())
    print(a.getState(), a.getStateStr())

    
    
    
    
    
    a.changeVal("fuck")

    print(a.getState(), a.getStateStr())
    