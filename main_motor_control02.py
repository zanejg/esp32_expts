

from machine import Pin, SPI
import time
import sys
from math import pi


#gpio.setwarnings(False)
#gpio.setmode(gpio.BCM)

class a4988_controller():

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
    

    between_steps = 0.003
    step_pulse = 0.001


    def __init__(self, config, control):
        """
        Takes a dict with the pin config and
        a dict for the values for controlling the motor loop.
        This will consist of a target speed and how fast we want to
        accelerate to it. The loop will then continue at that speed until 
        told otherwise. The target will be a float between -1 and 1.
        And the acceleration will be a float between just above 0 and 10.
        """

        # control pins
        self.ENABLE_PIN = Pin(config['enable'], Pin.OUT) #orange
        self.DIR_PIN = Pin(config['dir'], Pin.OUT)   #yellow
        self.PULSE_PIN = Pin(config['pulse'], Pin.OUT) #green

        # speed setting pins
        self.SPEED_PINS = [
            Pin(config['speed'][0], Pin.OUT),  # purple
            Pin(config['speed'][1], Pin.OUT),  # grey
            Pin(config['speed'][2], Pin.OUT),  #  blue
        ]
        # initialise this to full step
        self.step_degrees = self.full_step_degrees

        # get the vars to read for motor control
        # and set them to 0 initially
        self.target = control['target'] = 0
        self.accel = control['accel'] = 0



    def enable(self):
        self.ENABLE_PIN.off()
    def disable(self):
        self.ENABLE_PIN.on()

    def set_speed(self, speed):
        setting = self.speed_array[speed]
        # M1,M2,M3
        mpins = self.SPEED_PINS

        for pin_num in range(0,3):
            if setting[pin_num] == 1:
                mpins[pin_num].on()
            else:
                mpins[pin_num].off()
            
        # now we need to recalculate how many steps per revolution
        self.step_degrees = self.full_step_degrees * speed


    def set_direction(self, direction):
        """
        Given direction as either 1 or -1 set the appropriate pins
        """
        if direction > 0:
            self.DIR_PIN.on()
            #gpio.output(DIRECTION, gpio.HIGH)
        else:
            self.DIR_PIN.off()
            #gpio.output(DIRECTION, gpio.LOW)


    ###############################################################################
    def linear_gen(self, start,end,stepnum):
        """
        To give floating point range type function.
        Step num is how many steps a required
        """
        if stepnum < 3:
            raise ValueError("Need more steps")
        
        diff = end - start
        step_size = diff/(stepnum -1)
        i = start
        for j in range(0,stepnum):
            yield i
            i+=step_size

    def acceleration_seq(self, accel):
        """
        To produce a sequence to control the stepper motor acceleration.
        It will start at 1/32 speed and end at full speed.
        The accel will be linear.
        accel: is a number between 1 and 10
        """
        
        stepnum = int(100/accel)
        min_step_time = self.between_steps
        max_step_time = min_step_time * 2
        for this_speed in [1/16,1/8,1/4,1/2,1]:
            for step_time in self.linear_gen(max_step_time,
                                            min_step_time,
                                            stepnum):
                yield (this_speed, step_time)
    
    #def acelerate_one_speed_seq(self):
        
    ############################################################################
    def main_loop(self):
        """
        Will continuously run until a None is put into target.
        """
        last_target = self.target

        set the loop speed

        while(self.target is not None):
            """
            Loop for running motor
            """
            if newtarget is different
            else

        



    ################################################################################




    def accelerate_and_run(self, direction,accel,duration): #, start_speed, end_speed, acc):
        """
        Given direction, 
        accel as number between 1 and 10,
        duration in seconds.
        Accelerate from 1/32 speed to full then run.
        """
        
        self.set_direction(direction)
        
        time_to_run = float(duration)
        accel_seq = self.acceleration_seq(accel)

        
        for accel_tuple in accel_seq:
            self.set_speed(accel_tuple[0])
            self.PULSE_PIN.on()
            #gpio.output(STEP, gpio.HIGH)
            time.sleep(self.step_pulse)
            self.PULSE_PIN.off()
            #gpio.output(STEP, gpio.LOW)
            time.sleep(accel_tuple[1])
            time_to_run -= (self.step_pulse + accel_tuple[1])
            if time_to_run < 0:
                break
        
        self.set_speed(1)
        while time_to_run > 0:
            self.PULSE_PIN.on()
            #gpio.output(STEP, gpio.HIGH)
            time.sleep(self.step_pulse)
            self.PULSE_PIN.off()
            #gpio.output(STEP, gpio.LOW)
            time.sleep(self.between_steps)
            time_to_run -= (self.step_pulse + self.between_steps)
            


            
        
    #####################################################################################

# ENABLE_PIN = Pin(33, Pin.OUT) #orange
# DIR_PIN = Pin(25, Pin.OUT)   #yellow
# PULSE_PIN = Pin(26, Pin.OUT) #green


# # speed setting pins
# SPEED_PINS = [
#     Pin(12, Pin.OUT),  # purple
#     Pin(14, Pin.OUT),  # grey
#     Pin(27, Pin.OUT),  #  blue
# ]




controller_a = {
    "enable": 33, #orange
    "dir":    25,   #yellow
    "pulse":  26, #green
    # speed setting pins
    "speed":[12,14,27], 
}
controller_b = {
    "enable": 17, #orange
    "dir":    23,   #yellow
    "pulse":  22, #green
    # speed setting pins
    "speed":[18,19,21], 
}







def brun_motor(direction,accel, duration):
    controller = a4988_controller(controller_b)
    controller.enable()

    controller.accelerate_and_run(direction,accel,duration)
    controller.disable()

def arun_motor(direction,accel, duration):
    controller = a4988_controller(controller_a)
    controller.enable()

    controller.accelerate_and_run(direction,accel,duration)
    controller.disable()

