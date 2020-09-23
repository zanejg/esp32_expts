def get_free():
    """
    To return how much storage etc that I have free
    """
    st = uos.statvfs('/')
    tot = st[0]*st[2]
    free = st[0]*st[3]
    used = tot - free

    print("Total:{} Free:{} Used:{}".format(tot,
                                            free,
                                            used))


# Complete project details at https://RandomNerdTutorials.com
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


def web_page():
    if led.value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"

    html = """<html>
    <head> 
        <title>ESP Web Server</title> 
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,"> 
        <style>
            html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
            h1{color: #0F3376; padding: 2vh;}
            p{font-size: 1.5rem;}
            .button{display: inline-block; 
                    background-color: #e7bd3b; 
                    border: none; 
                    border-radius: 4px; 
                    color: white; 
                    padding: 16px 40px; 
                    text-decoration: none; 
                    font-size: 30px; 
                    margin: 2px; 
                    cursor: pointer;}
            .redbutton{background-color: red;}
            .bluebutton{background-color: blue;}
            .greenbutton{background-color: green;}
        </style>
    </head>
    <body> 
        <h1>Zane's ESP Web Server</h1> 
        <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
        <p><a href="/?led=on"><button class="button greenbutton">FWD</button></a></p>
        <p><a href="/?led=off"><button class="button redbutton">STOP</button></a></p>
        <p><a href="/?led=on"><button class="button bluebutton">REV</button></a></p>
    </body>
    </html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
controller = a4988_controller()
controller.enable()


while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
        print('LED ON')
        led.value(1)
    if led_off == 6:
        print('LED OFF')
        led.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

