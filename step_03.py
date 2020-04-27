import RPi.GPIO as gpio
import time
import sys

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(2, gpio.OUT)
gpio.setup(3, gpio.OUT)
gpio.setup(4, gpio.OUT)

gpio.setup(17, gpio.OUT) # M3
gpio.setup(27, gpio.OUT) # M2
gpio.setup(22, gpio.OUT) # M1


speed_array= {
    1.0: [0,0,0],
    1/2: [1,0,0],
    1/4: [0,1,0],
    1/8: [1,1,0],
    1/16:[1,1,1]
}


# control pins
ENABLE = 2
DIRECTION = 3
STEP = 4

# speed setting pins
M1 = 22
M2 = 27
M3 = 17


#step_delay = 0.01
# assuming 1.8 degrees per step
full_step_degrees = 1.8
step_degrees = full_step_degrees

between_steps = 0.001
step_pulse = 0.001



def set_speed(speed):
    setting = speed_array[speed]
    # M1,M2,M3
    mpins = [22,27,17]

    for pin_num in range(0,3):
        if setting[pin_num] == 1:
           pin_setting = gpio.HIGH
        else:
           pin_setting = gpio.LOW
        gpio.output(mpins[pin_num], pin_setting)
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
        gpio.output(DIRECTION, gpio.HIGH)
    else:
        gpio.output(DIRECTION, gpio.LOW)

    step_num = int(degrees / step_degrees)
    print("steps={} stepdegs={} ".format(step_num,step_degrees))

    for cc in range(0,step_num):
        gpio.output(STEP, gpio.HIGH)
        time.sleep(step_pulse)
        gpio.output(STEP, gpio.LOW)
        time.sleep(between_steps)


if len(sys.argv) < 3:
    print("Usage scriptname direction degrees")
else:
    gpio.output(ENABLE, gpio.LOW)

    direction = int(sys.argv[1])
    degrees = int(sys.argv[2])

    set_speed(1)
    turn_motor(direction,degrees)
    turn_motor(direction * -1, degrees)

    set_speed(1/2)
    turn_motor(direction,degrees)
    turn_motor(direction * -1, degrees)

    gpio.output(ENABLE, gpio.HIGH)
