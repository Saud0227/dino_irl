#!/bin/python

import json
from time import sleep
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
appState = 2
pauseList = {}
globalTick = 0.01
screenSetup = False
jumpDeath = False

assets = {"dino1":"assets/Dino_1.png", "dino2":"assets/Dino_2.png", "cact1":"assets/Kaktus_2.png", "cact2":"assets/Kaktus_1.png", "fly1":"assets/Fågel_1.png", "fly2":"assets/Fågel_2.png", "dino_c1":"assets/Dino_l1.png", "dino_c2":"assets/Dino_l2.png", "gg":"assets/gameOver.png"}


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
animationTick = 0
animationOn = True

# DINO SHITS
#------------------------------------------------------------
jumpActive = False
jumpH = 40
jumpReduce = 1.5
dinoHeight = 160
dinoWidth = 90
dPosY = ground-dinoHeight
dPosYStart = dPosY
dinoDeltaY = 0
crouchActive = False

#BLOCKER SHITS
#------------------------------------------------------------
bList = []
dC = 0

# blocker.typeYVal and blocker.moveSpeed are reset
blocker.typeYVal = {0:700, 1:700, 2:300, 3:300}
blocker.typeXSize = {0:100, 1:105, 2:250, 3:200}
blocker.typeYSize = {0:140, 1:170, 2:135, 3:135}
blocker.typeAssets = {0:"cact1", 1:"cact2", 2:True, 3:True}
blocker.moveSpeed = 15
spawnTimeDelta = 1.3
# Spawner tweak
#------------------------------------------------------------

dCCutoff = 0.7
dCChangeVal = 70
speedCutoff = 30
speedChangeVal = 10

#------------------------------------------------------------




# Json Scoreboard Loading Crap
#------------------------------------------------------------
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","å","ä","ö"]


try:
    f = open("scoreboard.json", "r")
    scoreboardDat  = json.load(f)
    f.close()
except FileNotFoundError:
    scoreboardDat = []

def writeScoreboardToFile():
    global scoreboardDat
    jsonObject = json.dumps(scoreboardDat)
    with open("scoreboard.json", "w") as outfile:
        outfile.write(jsonObject)

def returnSec(itm):
    return itm[1]

def scoreAdd(tag:str, val:int):
    global scoreboardDat
    scoreboardDat.append((tag, val))
    scoreboardDat.sort(key=returnSec, reverse=True)
    writeScoreboardToFile()



def getName(a):
    global alphabet
    a.postloop()
    active = True
    word = []
    strWord = ''
    sleep(0.5)
    while active:
        screenSize = a.getSize()
        strWord = ''.join(word)
        a.text(screenSize.x/2, screenSize.y/4, "INPUT", "title")
        a.text(screenSize.x/2, screenSize.y/3.5, strWord, "title")
        a.update()
        a.postloop()
        sleep(0.1)

        cKey = keyboard.read_key()
        if cKey == "enter":
            active = False
        elif cKey == "backspace":
            if len(word) > 0:
                word.pop(-1)
        elif cKey == "space":
            if len(word) > 0 and word[-1] != " ":
                word.append(" ")
        else:
            if cKey in alphabet:
                if len(word) < 1:
                    word.append(cKey.capitalize())
                elif word[-1] == " ":
                    word.append(cKey.capitalize())
                else:
                    word.append(cKey)





    return strWord
#getName()
#------------------------------------------------------------
def logout():
    global pinLogic
    system('./killSession.sh')


a = tkInterface(Tk, False)


assets = tkInterface.assetHandle(assets)
a.assets = assets


if pinLogic:
    a.unaliveTasks.append(pinH.clearLib)
    a.unaliveTasks.append(logout)



def reset(toState: int):
    global bList, dC, spawnTimeDelta, jumpActive, jumpH, jumpReduce, dinoHeight
    global dinoWidth, dPosY, dPosYStart, dinoDeltaY, crouchActive, dAlive
    global pauseList, appState, ground, score, scoreRaw, animationTick, animationOn
    ground = a.getSize().y*0.9

    blocker.typeYVal = {0:ground, 1:ground, 2:ground-150, 3:ground-300}


    bList = []
    dC = 0
    blocker.moveSpeed = 15
    spawnTimeDelta = 1.3
    jumpActive = False
    jumpH = 40
    jumpReduce = 1.5
    dinoHeight = 190
    dinoWidth = 180
    dPosY = ground-dinoHeight
    dPosYStart = dPosY
    dinoDeltaY = 0
    crouchActive = False
    dAlive = True
    pauseList = {}
    score = 0
    scoreRaw = 0
    animationTick = 0
    animationOn = True




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

        blocker.moveSpeed = 15 + dC / (speedChangeVal*(1+int(blocker.moveSpeed>speedCutoff)))
        if blocker.moveSpeed > 70:
            blocker.moveSpeed = 70
        spawnX = a.getSize().x*1.2 + randint(-int(a.getSize().x*0.15),200)

        toSpawn = spawnTRNG()

        if toSpawn == 0:
            xDelta = spawnX
            for i in range(randint(1,4)):
                smartInsert(bList, blocker(0, xDelta))
                xDelta += randint(blocker.typeXSize[0], blocker.typeXSize[0]*1)
        else:
            smartInsert(bList, blocker(toSpawn, spawnX))




def gameOverCh(_state:bool):
    global appState, jumpPad, jumpDeath, animationOn
    if _state:
        #print("DEAD")
        jumpDeath = jumpPad
        appState = 1
        animationOn = False



def game():
    global a, crouchActive, jumpActive, dPosY
    global dinoWidth, dinoHeight, globalTick, ground, bList, score, scoreRaw, animationTick


    a.strokeW(0)
    a.fill(0,255,0)
    if crouchActive:
        if jumpActive:
            jumpReset()
        dinoCol = a.rect(100, dPosY+dinoWidth*0.4, dinoHeight*1.3, dinoWidth*0.6, False)
        if animationTick % 2 == 1:
            a.drawImage(100, dPosY+70, "dino_c2")
        else:
            a.drawImage(100, dPosY+70, "dino_c1")
    else:
        dinoCol = a.rect(100, dPosY, dinoWidth, dinoHeight, False)
        if not jumpActive and animationTick % 2 == 1:
            a.drawImage(100, dPosY, "dino2")
        else:
            a.drawImage(100, dPosY, "dino1")

    for i in range(len(bList)):
        bList[i].update(a, animationTick)
        if bList[i].checkCol:
            gameOverCh(a.checkColRect(dinoCol,bList[i].currentCollision))


    if jumpPad:
            jump()

    crouchActive = crouchLeft and crouchRight


    # Spawn Vals Screen Print =Z S.V.S.P.
    """
    a.text(100,100,checkPause("spawn"), "asd")

    a.text(100,200,spawnTimeDelta, "asd")
    """
    a.text(100,150,blocker.moveSpeed, "asd")


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


def drawScoreBoard():
    global a, scoreboardDat
    a.strokeW(0)
    screenSize = a.getSize()
    a.fill(90,90,90)
    a.rect(screenSize.x*0.745, screenSize.y*0.04, screenSize.x*0.23, screenSize.y*0.22)

    a.text(screenSize.x*0.86, screenSize.y*0.02, "SCORE", "title")
    a.fill(110,110,110)

    for i in range(10):
        fillVal = 110 + (i % 2) * 20
        a.fill(fillVal, fillVal, fillVal)
        a.rect(screenSize.x*0.75, screenSize.y*(0.05+0.02*i), screenSize.x*0.22, screenSize.y*0.02)



    a.fill(0,0,0)
    toDisplay = len(scoreboardDat)
    if toDisplay > 10:
        toDisplay = 10
    for i in range(toDisplay):
        a.text(screenSize.x*0.753, screenSize.y*(0.05+0.02*i), scoreboardDat[i][0])
        a.text(screenSize.x*0.865, screenSize.y*(0.05+0.02*i), scoreboardDat[i][1])


    a.stroke(0, 0, 0)
    a.strokeW(3)
    a.line(screenSize.x*0.86, screenSize.y*0.05, screenSize.x*0.86, screenSize.y*0.25)


def gameOver():
    global a, crouchActive, jumpActive, dPosY
    global dinoWidth, dinoHeight, globalTick, ground, bList, score, jumpDeath, jumpPad, crouchLeft, crouchRight


    a.strokeW(0)
    a.fill(0,255,0)
    if crouchActive:
        if animationTick % 2 == 1:
            a.drawImage(100, dPosY+70, "dino_c2")
        else:
            a.drawImage(100, dPosY+70, "dino_c1")
    else:
        if not jumpActive and animationTick % 2 == 1:
            a.drawImage(100, dPosY, "dino2")
        else:
            a.drawImage(100, dPosY, "dino1")



    for i in range(len(bList)):
        bList[i].update(a, animationTick, False)

    screenSize = a.getSize()


    a.strokeW(5)
    a.line(0,ground,screenSize.x,ground)


    drawScoreBoard()

    a.text(screenSize.x/2, screenSize.y/4, "GAME OVER", "title")
    a.text(screenSize.x/2, screenSize.y/3, f"SCORE: {score}", "title")
    a.text(screenSize.x/2-150, screenSize.y*2/3, "LEFT: MENU", "subtitle")
    a.text(screenSize.x/2+150, screenSize.y*2/3, "RIGHT: SAVE", "subtitle")
    a.text(screenSize.x/2, screenSize.y*2/3+50, "JUMP: RESTART", "subtitle")

    if not jumpPad:
        jumpDeath = False
    if jumpPad and not jumpDeath:
        reset(0)
    if crouchLeft:
        reset(2)
    if crouchRight:
        scoreAdd(getName(a), score)
        reset(2)
    a.update()
    a.postloop()

    sleep(globalTick)


def hub():
    global a, crouchActive, jumpActive, dPosY
    global dinoWidth, dinoHeight, globalTick, ground, bList, score, jumpDeath, jumpPad, crouchLeft, crouchRight


    a.strokeW(0)
    a.fill(0,255,0)
    if animationTick % 2 == 1:
        a.drawImage(100, dPosY, "dino2")
    else:
        a.drawImage(100, dPosY, "dino1")

    drawScoreBoard()
    screenSize = a.getSize()


    a.strokeW(5)
    a.line(0,ground,screenSize.x,ground)

    a.text(screenSize.x/2, screenSize.y/4, "DINO GAME", "title")
    a.text(screenSize.x/2, screenSize.y/3.5, "JUMP  TO START", "title")

    if crouchLeft and crouchRight:
        reset(0)
    a.update()
    a.postloop()

    sleep(globalTick)




stateMains = [game, gameOver, hub]

if __name__ == '__main__':
    print(ground)
    print(a.getSize())



    while a.alive():
        stateMains[appState]()
        if not screenSetup:
            reset(2)
            screenSetup = True
        if testingKeyboard or not pinLogic:
            jumpPad =  keyboard.is_pressed("s")
            crouchLeft = keyboard.is_pressed("q")
            crouchRight = keyboard.is_pressed("e")
        elif a.alive and pinLogic:
            jumpPad =  not pinH.jumpCh()
            crouchLeft = pinH.leftCh()
            crouchRight = pinH.rightCh()
        if animationOn:
            animationTick += 1
            if animationTick > 9:
                animationTick = 0


