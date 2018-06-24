from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
import time

import smbus            #import SMBus module of I2C
from time import sleep  #import sleep
import math

#some MPU6050 Registers and their Address
Register_A     = 0              #Address of Configuration register A
Register_B     = 0x01           #Address of configuration register B
Register_mode  = 0x02           #Address of mode register

X_axis_H    = 0x03              #Address of X-axis MSB data register
Z_axis_H    = 0x05              #Address of Z-axis MSB data register
Y_axis_H    = 0x07              #Address of Y-axis MSB data register
declination = -0.931          #define declination angle of location where measurement going to be done
pi          = 3.14159265359     #define pi value

#initialize the gpio module / initialise le GPIO
gpio.init()


#Configure la broche PG7 (equivalent au GPIO21 du Raspberry) comme une sortie
gpio.setcfg(port.PG6, gpio.OUTPUT) # forward front right   h
gpio.setcfg(port.PG7, gpio.OUTPUT) # reverse front right  h
gpio.setcfg(port.PG8, gpio.OUTPUT) # reverse front left  l
gpio.setcfg(port.PG9, gpio.OUTPUT) # forward front left  l

gpio.setcfg(port.PA2, gpio.OUTPUT) # back left reverse  h
gpio.setcfg(port.PC3, gpio.OUTPUT) # back left forward  h
gpio.setcfg(port.PA21, gpio.OUTPUT) # back right forward h
gpio.setcfg(port.PA18, gpio.OUTPUT) #  back right reverse h

gpio.setcfg(port.PA13, gpio.OUTPUT)
gpio.setcfg(port.PA14, gpio.OUTPUT)
gpio.setcfg(port.PD14, gpio.OUTPUT)
gpio.setcfg(port.PC4, gpio.OUTPUT)

gpio.setcfg(port.PA20, gpio.OUTPUT)
gpio.setcfg(port.PA10, gpio.OUTPUT)
gpio.setcfg(port.PA9, gpio.OUTPUT)
gpio.setcfg(port.PA8, gpio.OUTPUT)

gpio.setcfg(port.PA6, gpio.OUTPUT)
gpio.setcfg(port.PA1, gpio.INPUT)

sTmr =  0.003

def Magnetometer_Init():
        #write to Configuration Register A
        bus.write_byte_data(Device_Address, Register_A, 0x70)

        #Write to Configuration Register B for gain
        bus.write_byte_data(Device_Address, Register_B, 0xa0)

        #Write to mode Register for selecting mode
        bus.write_byte_data(Device_Address, Register_mode, 0)

def read_raw_data(addr):
        #Read raw 16-bit value
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from module
        if(value > 32768):
            value = value - 65536
        return value

bus = smbus.SMBus(0)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x1e   # HMC5883L magnetometer device address
Magnetometer_Init()     # initialize HMC5883L magnetometer 


def USDistance():
	gpio.output(port.PA6, gpio.HIGH)
	sleep(0.00001)
	gpio.output(port.PA6, gpio.LOW)
	while gpio.input(port.PA1) == 0:
		pulse_start = time.time()
	while gpio.input(port.PA1) == 1:
		pulse_end = time.time()
	pulse_duration  = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance , 2)
	#print("distance :" + str(distance) + "cm")
	return distance;

#stepper
def RightClk():
	i=1
	while i < 50 :

		gpio.output(port.PA13, gpio.HIGH)
		sleep(sTmr)
		gpio.output(port.PA13, gpio.LOW)

		gpio.output(port.PA14, gpio.HIGH)
		sleep(sTmr)
		gpio.output(port.PA14, gpio.LOW)

		gpio.output(port.PD14, gpio.HIGH)
		sleep(sTmr)
		gpio.output(port.PD14, gpio.LOW)

		gpio.output(port.PC4, gpio.HIGH)
		sleep(sTmr)
		gpio.output(port.PC4, gpio.LOW)
		i += 1
		if i > 50:
			break

def RightAClk():
	i=1
	while i < 50 :

	        gpio.output(port.PC4, gpio.HIGH)
        	sleep(sTmr)
	        gpio.output(port.PC4, gpio.LOW)

	        gpio.output(port.PD14, gpio.HIGH)
        	sleep(sTmr)
	        gpio.output(port.PD14, gpio.LOW)

	        gpio.output(port.PA14, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA14, gpio.LOW)

	        gpio.output(port.PA13, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA13, gpio.LOW)
       		i += 1
	        if i > 50:
        	        break


def LeftClk() :
	#stepper 
	i=1
	while i < 50 :

        	gpio.output(port.PA20, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA20, gpio.LOW)

	        gpio.output(port.PA10, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA10, gpio.LOW)

        	gpio.output(port.PA9, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA9, gpio.LOW)

	        gpio.output(port.PA8, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA8, gpio.LOW)
	        i += 1
        	if i > 50:
                	break

def LeftAClk() :
	i=1
	while i < 50 :

        	gpio.output(port.PA8, gpio.HIGH)
	        sleep(sTmr)
        	gpio.output(port.PA8, gpio.LOW)

        	gpio.output(port.PA9, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA9, gpio.LOW)

        	gpio.output(port.PA10, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA10, gpio.LOW)

	        gpio.output(port.PA20, gpio.HIGH)
	        sleep(sTmr)
	        gpio.output(port.PA20, gpio.LOW)
	        i += 1
	        if i > 50:
        	        break

def StopWheel():
	gpio.output(port.PG6, gpio.LOW)
        gpio.output(port.PG8, gpio.LOW)
        gpio.output(port.PA2, gpio.LOW)
        gpio.output(port.PA18, gpio.LOW)
	gpio.output(port.PG7, gpio.LOW)
        gpio.output(port.PG9, gpio.LOW)
        gpio.output(port.PC3, gpio.LOW)
        gpio.output(port.PA21, gpio.LOW)
	return;

def MoveBack(tmr):
	# Move
	gpio.output(port.PG6, gpio.HIGH)
	gpio.output(port.PG8, gpio.HIGH)
	gpio.output(port.PA2, gpio.HIGH)
	gpio.output(port.PA18, gpio.HIGH)
	sleep(tmr)
	gpio.output(port.PG6, gpio.LOW)
	gpio.output(port.PG8, gpio.LOW)
	gpio.output(port.PA2, gpio.LOW)
	gpio.output(port.PA18, gpio.LOW)
	#sleep(0.5)
	return;

def MoveFront():
	gpio.output(port.PG7, gpio.HIGH)
	gpio.output(port.PG9, gpio.HIGH)
	gpio.output(port.PC3, gpio.HIGH)
	gpio.output(port.PA21, gpio.HIGH)
	#sleep(1)
	gpio.output(port.PG7, gpio.LOW)
	gpio.output(port.PG9, gpio.LOW)
	gpio.output(port.PC3, gpio.LOW)
	gpio.output(port.PA21, gpio.LOW)
	sleep(0.5)
	return;

def SetRotation() :
	# rotational setup
	LeftClk()
	RightAClk()
	return;

def ResetRotation() :
	# reset rotational setup
	RightClk()
	LeftAClk()
 	return;


def TurnRight():
	RightClk()
	LeftClk()

def TurnLeft():
	LeftAClk()
	RightAClk()

def RotateClock(tmr):
	gpio.output(port.PG6, gpio.HIGH) # right front Reverse
	gpio.output(port.PA18, gpio.HIGH) #  right rear reverse
	gpio.output(port.PG9, gpio.HIGH) # left front forward
	gpio.output(port.PC3, gpio.HIGH) # left rear  forward

	sleep(tmr)
	gpio.output(port.PG6, gpio.LOW)
	gpio.output(port.PA18, gpio.LOW)
	gpio.output(port.PG9, gpio.LOW)
	gpio.output(port.PC3, gpio.LOW)

def RotateAClock(tmr):
	gpio.output(port.PA2, gpio.HIGH) # left Rear reverse
        gpio.output(port.PG8, gpio.HIGH) # left  front reverse
	gpio.output(port.PA21, gpio.HIGH) # right forward  
	gpio.output(port.PG7, gpio.HIGH) # right  forward
	sleep(tmr)
        gpio.output(port.PA2, gpio.LOW) # left Rear reverse
        gpio.output(port.PG8, gpio.LOW) # left  front reverse
	gpio.output(port.PG7, gpio.LOW)
	gpio.output(port.PA21, gpio.LOW)

def UTurnClk():
	StopWheel()
        SetRotation()
        RotateClock(1.2)
	ResetRotation()
        MoveBack(1)
        SetRotation()
        RotateClock(1.2)
        ResetRotation()

def UTurnAClk():
        StopWheel()
        SetRotation()
        RotateAClock(1.2)
        ResetRotation()
        MoveBack(1)
        SetRotation()
        RotateAClock(1.2)
        ResetRotation()

def ReadCompass():
       #Read Accelerometer raw value
        x = read_raw_data(X_axis_H)
        z = read_raw_data(Z_axis_H)
        y = read_raw_data(Y_axis_H)

        heading = math.atan2(y, x) + declination

        #Due to declination check for >360 degree
        if(heading > 2*pi):
                heading = heading - 2*pi

        #check for sign
        if(heading < 0):
                heading = heading + 2*pi

        #convert into angle
        heading_angle = int(heading * 180/pi)

        print ("Heading Angle =  " + str(heading_angle))
	return heading_angle



north = 213
east = 337
west = 87
south = 32

def TurnCompass90Clock():
	SetRotation()
	curpos = ReadCompass()
	if(curpos < north and curpos > west):
		while(curpos < north ):
			RotateClock(.002)
			curpos = ReadCompass()

	if(curpos > south  and curpos < west):
                while(curpos < west ):
                        RotateClock(.002)
                        curpos = ReadCompass()

	ResetRotation()


TurnCompass90Clock()



ReadCompass()

CTurn = 1
j = 50;
while j < 3 :

	reachedend = 0;
	i = 0;

	while i < 1 :
		dis = USDistance()
		if dis > 10:
			MoveBack(0.2)
	        	print("Ret distance :" + str( dis )  + "cm")
		else:
			if CTurn == 0 :
				UTurnClk()
				CTurn =  1
			else :
				UTurnAClk()
				CTurn = 0
			break
	j += 1







StopWheel()

#SetRotation()
#RotateClock()
#sleep(2)
#RotateAClock()
#ResetRotation()

#TurnLeft()
#MoveFront()

#TurnRight()
#TurnRight()
#MoveBack()
#MoveFront()
#TurnLeft()
