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
        return

    def jumpCh(self):
        return GPIO.input(self.jumpPin)

    def leftCh(self):
        return GPIO.input(self.left)

    def rightCh(self):
        return GPIO.input(self.right)