
from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep
import time

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

gpio.setcfg(port.PA12, gpio.OUTPUT)
gpio.setcfg(port.PA11, gpio.INPUT)

sTmr =  0.003

def USDistance():
	gpio.output(port.PA12, gpio.HIGH)
	sleep(0.00001)
	gpio.output(port.PA12, gpio.LOW)
	while gpio.input(port.PA11) == 0:
		pulse_start = time.time()
	while gpio.input(port.PA11) == 1:
		pulse_end = time.time()
	pulse_duration  = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance , 2)
	print("distance :" + str(distance) + "cm")
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

def RotateClock():
	gpio.output(port.PG6, gpio.HIGH) # right front Reverse
	gpio.output(port.PA18, gpio.HIGH) #  right rear reverse
	gpio.output(port.PG9, gpio.HIGH) # left front forward
	gpio.output(port.PC3, gpio.HIGH) # left rear  forward

	sleep(1)
	gpio.output(port.PG6, gpio.LOW)
	gpio.output(port.PA18, gpio.LOW)
	gpio.output(port.PG9, gpio.LOW)
	gpio.output(port.PC3, gpio.LOW)

def RotateAClock():
	gpio.output(port.PA2, gpio.HIGH) # left Rear reverse
        gpio.output(port.PG8, gpio.HIGH) # left  front reverse
	gpio.output(port.PA21, gpio.HIGH) # right forward  
	gpio.output(port.PG7, gpio.HIGH) # right  forward
	sleep(1)
        gpio.output(port.PA2, gpio.LOW) # left Rear reverse
        gpio.output(port.PG8, gpio.LOW) # left  front reverse
	gpio.output(port.PG7, gpio.LOW)
	gpio.output(port.PA21, gpio.LOW)


i = 0;

while i < 1 :
	dis = USDistance()
	if dis  > 10:
		MoveBack(0.2)
	        print("Ret distance :" + str( dis )  + "cm")

	else:
		StopWheel()
		break

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
