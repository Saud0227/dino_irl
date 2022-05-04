import math as m



"""
    When importing, import only the vector class and definitely not *
"""

def pRound(n, decimals=0):
    multiplier = 10 ** decimals
    return m.floor(n*multiplier + 0.5) / multiplier


class vector():

    @staticmethod
    def degWrapping(deg):

        if(deg<0):
            return(360-deg)
        elif(deg>360):
            return(deg-360)
        else:
            return(deg)

    @classmethod
    def make2D(cls, deg):
        deg = cls.degWrapping(deg)
        invdeg = m.radians(cls.degWrapping(180-deg))

        tmpX = pRound(m.sin(invdeg),2)
        if(deg>180):
            tmpX*=-1
        tmpY = pRound(m.cos(invdeg),2)

        return(cls(tmpX,tmpY))
    @classmethod
    def checkVector(cls, obj):
        return(isinstance(obj,cls))



    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def mag(self):
        return pRound(m.sqrt(self.x*self.x + self.y*self.y),2)
    
    def __str__(self):
        return(str(self.x) +","+ str(self.y))
    def __repr__(self):
        return f"Vector:{self.x},{self.y}  id:{id(self)}\n"

    def normalize(self):
        tmpMag = self.mag()
        self.x = self.x/tmpMag
        self.y = self.y/tmpMag

    def deg(self):
        cMag = self.mag()*-1
        topSideEq = cMag**2 + cMag**2 - ((cMag-self.y)**2 + self.x**2)
        bottomSideEq = 2 * cMag**2
        deg = m.degrees(m.acos(topSideEq/bottomSideEq))
        if(self.x<0):
            deg = 360-deg
        return pRound(deg,2)


    def add(self,x,y=0):
        if (isinstance(x,int) or isinstance(x,float)) and (isinstance(y,int) or isinstance(y,float)):
            self.x+=x
            self.y+=y
        elif vector.checkVector(x):
            self.x+=x.x
            self.y+=x.y

    def mult(self,x,y=" "):
        if (isinstance(x,int) or isinstance(x,float)) and (isinstance(y,int) or isinstance(y,float)):
            self.x*=x
            self.y*=y
        elif isinstance(x,int) or isinstance(x,float):
            self.x*=x
            self.y*=x
        elif vector.checkVector(x):
            self.x+=x.x
            self.y+=x.y

    def limit(self,l):
        cMag = self.mag()
        if cMag > l:
            rScaler = cMag/l
            self.x/=rScaler
            self.y/=rScaler
            # print(cMag, l, self.mag())

    def human(self):
        return("x:{}\nY:{}\nMag:{}".format(self.x,self.y,self.mag()))

def main():

    tmpV = vector(4,4)
    print(tmpV.human())
    #tmpV.normalize()
    print(tmpV.deg())
    #tmpV.add(10,10)
    #tmpV.add(vector(-10,-10))
    tmpV.mult(2)
    tmpV.limit(8)
    print(tmpV.human())
    print(tmpV)
    """
    for i in range(12):
        #print(360/12*i)
        print(vector.make2D(360/12*i).human())
    """


if __name__ == "__main__":
    main()