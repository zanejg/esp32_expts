
# def do_connect():
#     import network
#     sta_if = network.WLAN(network.STA_IF)
#     if not sta_if.isconnected():
#         print('connecting to network...')
#         sta_if.active(True)
#         sta_if.connect('bedzone', 'Quardle Wardle Oodle')
#         while not sta_if.isconnected():
#             pass
#     print('network config:', sta_if.ifconfig())

from machine import Pin, SPI
import time
import sys



#gpio.setwarnings(False)
#gpio.setmode(gpio.BCM)

class a4988_controller():


    ENABLE_PIN = Pin(33, Pin.OUT) #orange
    DIR_PIN = Pin(25, Pin.OUT)   #yellow
    PULSE_PIN = Pin(26, Pin.OUT) #green


    # speed setting pins
    SPEED_PINS = [
        Pin(12, Pin.OUT),  # purple
        Pin(14, Pin.OUT),  # grey
        Pin(27, Pin.OUT),  #  blue
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
    

    between_steps = 0.003
    step_pulse = 0.001


    def __init__(self):
        self.step_degrees = self.full_step_degrees

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




    def turn_motor(self, direction, degrees):
        """
        If direction is negative rotate one way
        If positive rotate the other
        Because the the step number is 1.8 degrees the rotation amount is only
        likely to be approximate
        """
        if direction > 0:
            self.DIR_PIN.on()
            #gpio.output(DIRECTION, gpio.HIGH)
        else:
            self.DIR_PIN.off()
            #gpio.output(DIRECTION, gpio.LOW)

        step_num = int(degrees / self.step_degrees)
        print("steps={} stepdegs={} ".format(step_num,self.step_degrees))

        for cc in range(0,step_num):
            self.PULSE_PIN.on()
            #gpio.output(STEP, gpio.HIGH)
            time.sleep(self.step_pulse)
            self.PULSE_PIN.off()
            #gpio.output(STEP, gpio.LOW)
            time.sleep(self.between_steps)




def read_spi():
    vspi = SPI(2, 
               baudrate=500000, 
               polarity=0, 
               phase=0, 
               bits=8, 
               firstbit=0, 
               sck=Pin(18), 
               mosi=Pin(23), 
               miso=Pin(19))

    buf = bytearray(5)     # create a buffer

    try:
        while True:
            vspi.readinto(buf)       # read into the given buffer (reads 50 bytes in this case)
            if buf != bytearray(b'\xff\xff\xff\xff\xff'):
                print(buf)
    except Exception as ex:
        print(x)








def run_motor(direction, degrees):

    controller = a4988_controller()

    controller.enable()
    #ENABLE_PIN.off()
    #gpio.output(ENABLE, gpio.LOW)
    
    # direction = int(sys.argv[1])
    # degrees = int(sys.argv[2])

    controller.set_speed(1)
    controller.turn_motor(direction,degrees)
    controller.turn_motor(direction * -1, degrees)

    controller.set_speed(1/2)
    controller.turn_motor(direction,degrees)
    controller.turn_motor(direction * -1, degrees)

    controller.disable()
    # gpio.output(ENABLE, gpio.HIGH)
