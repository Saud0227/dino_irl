import RPi.GPIO as GPIO





class pinHandler:



    def __init__(self, p1: int, p2: int, p3: int):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(p1, GPIO.IN)
        GPIO.setup(p2, GPIO.IN)
        GPIO.setup(p3, GPIO.IN)

        self.jumpPin = p1
        self.left = p2
        self.right = p3


    def clearLib(self):
        GPIO.cleanup()
        print("GPIO clear")
        return

    def jumpCh(self):
        pinV = GPIO.input(self.jumpPin)
        print("jump: " + str(pinV))
        return pinV

    def leftCh(self):
        pinV =  GPIO.input(self.left)
        print("left: " + str(pinV))
        return pinV

    def rightCh(self):
        pinV =  GPIO.input(self.right)
        print("right: " + str(pinV))
        return pinV