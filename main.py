from pydoc import cli
from time import sleep
import tkinter as Tk
from vectors import vector
from tkInterfaceF import tkInterface
from random import randint, random

from blockers import blocker

#GAME SHITS
#------------------------------------------------------------
pauseList = {}
globalTick = 0.01
ground = 700
#------------------------------------------------------------



# DINO SHITS
#------------------------------------------------------------
jumpActive = False
jumpH = 40
jumpReduce = 1.5
height = 120
width = 90
dPosY = ground-height
dPosYStart = dPosY
dinoDeltaY = 0
crouchActive = False
#------------------------------------------------------------

#BLOCKER SHITS
#------------------------------------------------------------
bList = []
dC = 0
blocker.typeYVal = {0:700, 1:700, 2:600, 3:400}
blocker.typeXSize = {0:20, 1:20, 2:50, 3:50}
blocker.typeYSize = {0:40, 1:50, 2:30, 3:30}
blocker.moveSpeed = 10
spawnTimeDelta = 1

#------------------------------------------------------------

def smartInsert(list, clsItm):
    for i in range(len(list)):
        if list[i].killMe:
            list[i] = clsItm
            print("Place was recycled")
            return True
    list.append(clsItm)

def pause(tag: str, cDelay: int):
    global pauseList, globalTick
    try:
        cTime = pauseList[tag.lower()]
        pauseList[tag.lower()] = cTime - 1
        if cTime == -2:
            pauseList[tag.lower()] = cDelay/globalTick
            return False
        return cTime < 0
    except KeyError:
        pauseList[tag.lower()] = cDelay/globalTick
        return False

def checkPause(tag: str):
    global pauseList, globalTick
    try:
        cTime = pauseList[tag.lower()]
        return cTime
    except KeyError:
        return "Error"
def jump():
    global dPosY, dPosYStart, dinoDeltaY, jumpActive, jumpH, jumpReduce, crouchActive
    if crouchActive:
        return
    dinoDeltaY = jumpH
    jumpActive = True


def jumpReset():
    global dPosY, dPosYStart,  dinoDeltaY, jumpActive

    jumpActive = False
    dPosY = dPosYStart
    dinoDeltaY = 0


def jumpTick():
    global dPosY, dPosYStart,  dinoDeltaY, jumpActive, jumpH, jumpReduce
    if not jumpActive:
        return None

    if dPosY > dPosYStart+dinoDeltaY:
        jumpReset()
        return None
    dinoDeltaY -= jumpReduce
    dPosY -= dinoDeltaY

a = tkInterface(Tk, True)


def spawnTRNG():
    rngSpawn = randint(0,100)
    if rngSpawn < 40:
        return 1

    if rngSpawn < 60:
        return 2

    if rngSpawn < 80:
        return 3

    return 0



def spawner():
    global dC, bList, spawnTimeDelta
    spawnTimeDelta = 1-dC/100
    if spawnTimeDelta < 0.2:
        spawnTimeDelta == 0.2
    if pause("spawn", int(spawnTimeDelta)):
        dC +=1
        blocker.moveSpeed +=dC/20
        spawnX = a.getSize().x*1.2

        toSpawn = spawnTRNG()

        if toSpawn == 0:
            xDelta = spawnX
            for i in range(randint(1,4)):
                smartInsert(bList, blocker(0, xDelta))
                xDelta += randint(blocker.typeXSize[0], blocker.typeXSize[0]*2)
        else:
            smartInsert(bList, blocker(toSpawn, spawnX))






if __name__ == '__main__':
    while a.alive():


        a.strokeW(0)
        a.fill(0,255,0)

        if crouchActive:
            if jumpActive:
                jumpReset()
            a.rect(100, dPosY+(height-width+10), height, width-10)
        else:
            a.rect(100, dPosY, width, height)



        a.strokeW(5)
        a.line(0,ground,1560,ground)




        for i in range(len(bList)):
            bList[i].update(a)

        a.text(100,100,checkPause("spawn"), "asd")
        a.text(100,150,blocker.moveSpeed, "asd")
        a.text(100,200,spawnTimeDelta, "asd")
        a.update()


        jumpTick()
        sleep(globalTick)
        a.postloop()

        spawner()





