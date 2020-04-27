#import RPi.GPIO as gpio
from machine import Pin
import time
import sys

#gpio.setwarnings(False)
#gpio.setmode(gpio.BCM)

ENABLE_PIN = Pin(33, Pin.OUT) #orange
DIR_PIN = Pin(25, Pin.OUT)   #yellow
PULSE_PIN = Pin(26, Pin.OUT) #green


# speed setting pins
SPEED_PINS = [
    Pin(17, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(27, Pin.OUT),
]


speed_array= {
    1.0: [0,0,0],
    1/2: [1,0,0],
    1/4: [0,1,0],
    1/8: [1,1,0],
    1/16:[1,1,1]
}


#step_delay = 0.01
# assuming 1.8 degrees per step
full_step_degrees = 1.8
step_degrees = full_step_degrees

between_steps = 0.001
step_pulse = 0.001



def set_speed(speed):
    setting = speed_array[speed]
    # M1,M2,M3
    mpins = SPEED_PINS

    for pin_num in range(0,3):
        if setting[pin_num] == 1:
            mpins[pin_num].on()
        else:
            mpins[pin_num].off()
           
    # now we need to recalculate how many steps per revolution
    step_degrees = full_step_degrees * speed




def turn_motor(direction, degrees):
    """
    If direction is negative rotate one way
    If positive rotate the other
    Because the the step number is 1.8 degrees the rotation amount is only
    likely to be approximate
    """
    if direction > 0:
        DIR_PIN.on()
        #gpio.output(DIRECTION, gpio.HIGH)
    else:
        DIR_PIN.off()
        #gpio.output(DIRECTION, gpio.LOW)

    step_num = int(degrees / step_degrees)
    print("steps={} stepdegs={} ".format(step_num,step_degrees))

    for cc in range(0,step_num):
        PULSE_PIN.on()
        #gpio.output(STEP, gpio.HIGH)
        time.sleep(step_pulse)
        PULSE_PIN.off()
        #gpio.output(STEP, gpio.LOW)
        time.sleep(between_steps)


if len(sys.argv) < 3:
    print("Usage scriptname direction degrees")
else:

def run_motor(direction, degrees)
    ENABLE_PIN.off()
    #gpio.output(ENABLE, gpio.LOW)
    
    # direction = int(sys.argv[1])
    # degrees = int(sys.argv[2])

    set_speed(1)
    turn_motor(direction,degrees)
    turn_motor(direction * -1, degrees)

    set_speed(1/2)
    turn_motor(direction,degrees)
    turn_motor(direction * -1, degrees)

    ENABLE_PIN.on()
    # gpio.output(ENABLE, gpio.HIGH)
