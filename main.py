from time import sleep
import tkinter as Tk
from vectors import vector
from tkInterfaceF import tkInterface
from random import randint

from blockers import blocker


import keyboard

#APP SHITS
#------------------------------------------------------------
appState = 0
pauseList = {}
globalTick = 0.01




#Buttons
#------------------------------------------------------------
jumpPad = False
crouchLeft= False
crouchRight = False

buttonDebug = True

#LIVE SHITS
#------------------------------------------------------------
dAlive = True
ground = 700


# DINO SHITS
#------------------------------------------------------------
jumpActive = False
jumpH = 40
jumpReduce = 1.5
dinoHeight = 120
dinoWidth = 90
dPosY = ground-dinoHeight
dPosYStart = dPosY
dinoDeltaY = 0
crouchActive = False

#BLOCKER SHITS
#------------------------------------------------------------
bList = []
dC = 0
blocker.typeYVal = {0:700, 1:700, 2:600, 3:400}
blocker.typeXSize = {0:20, 1:20, 2:50, 3:50}
blocker.typeYSize = {0:40, 1:50, 2:30, 3:30}
blocker.moveSpeed = 10
spawnTimeDelta = 1
# Spawner tweak
#------------------------------------------------------------

dCCutoff = 0.7
dCChangeVal = 70
speedCutoff = 30
speedChangeVal = 10

#------------------------------------------------------------



a = tkInterface(Tk, True)




def smartInsert(list, clsItm):
    for i in range(len(list)):
        if list[i].killMe:
            list[i] = clsItm
            # print("Place was recycled")
            return True
    list.append(clsItm)

def pause(tag: str, cDelay: int):
    global pauseList, globalTick
    try:
        cTime = pauseList[tag.lower()]
        pauseList[tag.lower()] = cTime - 1
        if cTime == -2:
            pauseList[tag.lower()] = int(cDelay/globalTick)
            return False
        return cTime < 0
    except KeyError:
        pauseList[tag.lower()] = int(cDelay/globalTick)
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
    if crouchActive or jumpActive:
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
    global dCCutoff, dCChangeVal, speedChangeVal, speedCutoff
    if pause("spawn", spawnTimeDelta):
        dC +=1



        spawnTimeDelta = 1.3 - dC / dCChangeVal+int(spawnTimeDelta<dCCutoff)*(dC / dCChangeVal -dCCutoff)/2
        if spawnTimeDelta < 0.1:
            spawnTimeDelta = 0.1

        blocker.moveSpeed = 10 + dC / (speedChangeVal*(1+int(blocker.moveSpeed>speedCutoff)))
        if blocker.moveSpeed > 70:
            blocker.moveSpeed = 70
        spawnX = a.getSize().x*1.2 + randint(-int(a.getSize().x*0.15),200)

        toSpawn = spawnTRNG()

        if toSpawn == 0:
            xDelta = spawnX
            for i in range(randint(1,4)):
                smartInsert(bList, blocker(0, xDelta))
                xDelta += randint(blocker.typeXSize[0], blocker.typeXSize[0]*2)
        else:
            smartInsert(bList, blocker(toSpawn, spawnX))





def gameOverCh(_state:bool):
    global appState
    if _state:
        print("DEAD")
        appState = 1



def game():
    global a, crouchActive, jumpActive, dPosY
    global dinoWidth, dinoHeight, globalTick, ground, bList


    a.strokeW(0)
    a.fill(0,255,0)
    if crouchActive:
        if jumpActive:
            jumpReset()
        dinoCol = a.rect(100, dPosY+(dinoHeight-dinoWidth+10), dinoHeight, dinoWidth-10)
    else:
        dinoCol = a.rect(100, dPosY, dinoWidth, dinoHeight)

    for i in range(len(bList)):
        bList[i].update(a)
        if bList[i].checkCol:
            gameOverCh(a.checkColRect(dinoCol,bList[i].currentCollision))


    if jumpPad:
            jump()

    crouchActive = crouchLeft and crouchRight


    # Spawn Vals Screen Print =Z S.V.S.P.
    """
    a.text(100,100,checkPause("spawn"), "asd")
    a.text(100,150,blocker.moveSpeed, "asd")
    a.text(100,200,spawnTimeDelta, "asd")
    """


    a.strokeW(5)
    a.line(0,ground,1560,ground)

    a.update()
    jumpTick()
    sleep(globalTick)
    a.postloop()
    spawner()
    # print("!")


def gameOver():
    global a, crouchActive, jumpActive, dPosY
    global dinoWidth, dinoHeight, globalTick, ground, bList


    a.strokeW(0)
    a.fill(0,255,0)
    if crouchActive:
        a.rect(100, dPosY+(dinoHeight-dinoWidth+10), dinoHeight, dinoWidth-10)
    else:
        a.rect(100, dPosY, dinoWidth, dinoHeight)



    for i in range(len(bList)):
        bList[i].update(a, False)


    a.strokeW(5)
    a.line(0,ground,1560,ground)


    screenSize = a.getSize()

    a.text(screenSize.x/2, screenSize.y/4, "GAME OVER", "title")

    a.update()
    a.postloop()

    sleep(globalTick)


def hub():
    global a




stateMains = [game, gameOver]

if __name__ == '__main__':



    while a.alive():
        stateMains[appState]()
        jumpPad =  keyboard.is_pressed("s")
        crouchLeft = keyboard.is_pressed("q")
        crouchRight = keyboard.is_pressed("e")


