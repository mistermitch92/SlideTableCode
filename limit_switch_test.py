import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
Far_lim=23
Near_lim=24
GPIO.setup(Far_lim, GPIO.IN)
GPIO.setup(Near_lim, GPIO.IN)

i=1
while True:
    print(i)
    i=i+1
    if (GPIO.input(Far_lim) == False):
        print('Far is False')
    elif (GPIO.input(Near_lim) == False):
        print('Near is False')
    else:
        print('neither')

