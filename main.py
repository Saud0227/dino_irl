#!/bin/python


from time import sleep
import datetime
import keyboard
import tkinter as Tk
from random import randint
from os import system

from vectors import vector
from tkInterfaceF import tkInterface
from blockers import blocker


pinLogic = False

try:
    from pins import pinHandler
    pinLogic = True
except ModuleNotFoundError:
    print("No Pins, running in computer")


#APP SHITS
#------------------------------------------------------------
appState = 0
pauseList = {}
globalTick = 0.01
screenSetup = False
jumpDeath = False

assets = {"dino1":"assets\Dino_1.png", "dino2":"assets\Dino_2.png", "cact1":"assets\Kaktus_2.png", "fly1":"assets\Fågel_1.png", "fly2":"assets\Fågel_2.png"}


testingKeyboard = False

if pinLogic:
    pinH = pinHandler(11, 13, 15)

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
score = 0
scoreRaw = 0


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
blocker.typeXSize = {0:40, 1:40, 2:100, 3:100}
blocker.typeYSize = {0:80, 1:100, 2:60, 3:60}
blocker.moveSpeed = 10
spawnTimeDelta = 1.3
# Spawner tweak
#------------------------------------------------------------

dCCutoff = 0.7
dCChangeVal = 70
speedCutoff = 30
speedChangeVal = 10

#------------------------------------------------------------
def logout():
    global pinLogic
    system('killSession.sh')


a = tkInterface(Tk, False)


assets = tkInterface.assetHandle(assets)

if pinLogic:
    a.unaliveTasks.append(pinH.clearLib)
    a.unaliveTasks.append(logout)



def reset(toState: int):
    global bList, dC, spawnTimeDelta, jumpActive, jumpH, jumpReduce, dinoHeight
    global dinoWidth, dPosY, dPosYStart, dinoDeltaY, crouchActive, dAlive
    global pauseList, appState, ground, score, scoreRaw
    ground = a.getSize().y*0.9

    blocker.typeYVal = {0:ground, 1:ground, 2:ground-100, 3:ground-300}


    bList = []
    dC = 0
    blocker.moveSpeed = 10
    spawnTimeDelta = 1.3
    jumpActive = False
    jumpH = 40
    jumpReduce = 1.5
    dinoHeight = 120
    dinoWidth = 90
    dPosY = ground-dinoHeight
    dPosYStart = dPosY
    dinoDeltaY = 0
    crouchActive = False
    dAlive = True
    pauseList = {}
    score = 0
    scoreRaw = 0




    appState = toState


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
    global appState, jumpPad, jumpDeath
    if _state:
        #print("DEAD")
        jumpDeath = jumpPad
        appState = 1



def game():
    global a, crouchActive, jumpActive, dPosY
    global dinoWidth, dinoHeight, globalTick, ground, bList, score, scoreRaw


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
    screenS = a.getSize()
    a.line(0,ground,screenS.x,ground)
    scoreRaw += blocker.moveSpeed
    score = int(scoreRaw/500)
    a.text(screenS.x*0.7, screenS.y*0.1,score, "title")

    a.update()
    jumpTick()
    sleep(globalTick)
    a.postloop()
    spawner()
    # print("!")


def gameOver():
    global a, crouchActive, jumpActive, dPosY
    global dinoWidth, dinoHeight, globalTick, ground, bList, score, jumpDeath, jumpPad


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
    a.text(screenSize.x/2, screenSize.y/3, f"SCORE: {score}", "title")
    a.text(screenSize.x/2-150, screenSize.y*2/3, "LEFT: MENU", "subtitle")
    a.text(screenSize.x/2+150, screenSize.y*2/3, "RIGHT: SAVE", "subtitle")
    a.text(screenSize.x/2, screenSize.y*2/3+50, "JUMP: RESTART", "subtitle")

    if not jumpPad:
        jumpDeath = False
    if jumpPad and not jumpDeath:
        reset(0)
    a.update()
    a.postloop()

    sleep(globalTick)


def hub():
    global a




stateMains = [game, gameOver]

if __name__ == '__main__':
    print(ground)
    print(a.getSize())



    while a.alive():
        stateMains[appState]()
        if not screenSetup:
            reset(0)
            screenSetup = True
        if testingKeyboard or not pinLogic:
            jumpPad =  keyboard.is_pressed("s")
            crouchLeft = keyboard.is_pressed("q")
            crouchRight = keyboard.is_pressed("e")
        elif a.alive and pinLogic:
            jumpPad =  not pinH.jumpCh()
            crouchLeft = pinH.leftCh()
            crouchRight = pinH.rightCh()


