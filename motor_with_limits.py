from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
Far_lim=23
Near_lim=24
GPIO.setup(Far_lim, GPIO.IN)
GPIO.setup(Near_lim, GPIO.IN)

kit = MotorKit(i2c=busio.I2C(board.SCL,  board.SDA, frequency=400000))

def get_temp()
	'''Call the heating setpoint and the most recent temps from the probes
	Args:
		none
	
	Output: 
		set_point (float): 
	 	probe1 (float):
	  	probe2 (float):
	 '''
	set_point = None
	probe1 = None
	probe2 = None

	return set_point, probe1, probe2

def accurate_sleep(target_duration, start_time):
    '''Accurately measure sleep time for a set duration

        Args: target_duration (float): length of sleep in seconds
              start_time (float): the starting time (use perf_counter)'''
    while True:
        current_time = time.perf_counter()
        elapsed_time = current_time - start_time
        if elapsed_time > target_duration:
            break
        
#default delays between steps (in milliseconds)
out_delay=10/1000
home_delay=5/1000

#slide table is 0.02mm/step
rate=0.02

def to_near_lim(home_delay):
	'''Move the slide table to the motorside (home position)
	Args:
		home_delay (float): minimum delay between steps (may be extra)
	Output:
		n_steps (int): # of steps taken
	'''
	n_steps = 0
	try:
		while GPIO.input(Near_lim) == True:
			step_start=time.perf_counter()
			kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
			accurate_sleep(home_delay, step_start)
			n_steps = n_steps + 1
		return n_steps
	except KeyboardInterrupt:
		return n_steps

def to_far_lim(out_delay):
	'''move the slide table to the non-motor side (far position)
	Args:
		home_delay (float): minimum delay between steps (may be extra)
	Output:
		n_steps (int): # of steps taken
	'''
	n_steps = 0
	try:
		while GPIO.input(Far_lim) == True:
			step_start=time.perf_counter()
			kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
			accurate_sleep(out_delay, step_start)
			n_steps = n_steps + 1
		return n_steps
	except KeyboardInterrupt:
		return n_steps

while True:
	travel_to = '' #initialize/reset travel_to
	travel_speed = 0 #initialize/reset travel_speed
	n_steps = 0 #intitialize/reset n_steps
	travel_to = input('Type HOME or OUT: ') #ask if homing or going out
	travel_speed = input('Travel Rate, max 4 (mm/s)): ') #how fast to move table
	travel_speed = float(travel_speed) #convert to a float
	travel_time_start = time.perf_counter() #start the time counter for the actual table travel speed
	time_delay=1/travel_speed*rate #s/mm * mm/step = s/step
	if travel_to == "HOME":
		if time_delay == 0:
			time_delay = home_delay
		print('HOMING at ',"%.2f" % travel_speed,'mm/s')
		n_steps = to_near_lim(time_delay)
		print('HOMED')
	elif travel_to == "OUT":
		if time_delay == 0:
			time_delay = out_delay
		print('Traveling OUT at ',"%.2f" % travel_speed,'mm/s')
		n_steps = to_far_lim(time_delay)
		print('Fully Extended (OUT)')


	travel_elapsed_time = time.perf_counter()-travel_time_start
	avg_speed = n_steps*rate / travel_elapsed_time #steps * mm/step / elapsed travel time
	print('Average Travel Speed = ',"%.3f" % avg_speed,'mm/s')
	print('restarting loop...')
	travel_to = None
	time_delay = None
	time.sleep(1)

