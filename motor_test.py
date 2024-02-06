from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time

kit = MotorKit(i2c=busio.I2C(board.SCL,  board.SDA, frequency=400000))

#move the stepper motor n rotations
n=2
steps=200*n

#delay between steps (in milliseconds)
delay=10/1000



for i in range(steps):
    start=time.time()
    kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
    time.sleep(delay)
    elapsed=time.time()-start
    print(elapsed)

kit.stepper1.release()
