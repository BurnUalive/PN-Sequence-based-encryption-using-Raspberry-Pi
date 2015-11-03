import time
import operator as op
import RPi.GPIO as GPIO
inputSignal= []
#Input helper functions
def getCode(n): #Generates code for the numbers
	code = []
	if(n==0):
		code = [1,0,0,0,0]
	elif(n==1):
		code = [1,0,0,0,1]
	elif(n==2):
		code = [1,0,0,1,0]
	elif(n==3):
		code = [1,0,0,1,1]
	elif(n==4):
		code = [1,0,1,0,0]
	elif(n==5):
		code = [1,0,1,0,1]
	elif(n==6):
		code = [1,0,1,1,0]
	elif(n==7):
		code = [1,0,1,1,1]
	elif(n==8):
		code = [1,1,0,0,0]
	elif(n==9):
		code = [1,1,0,0,1]
	return code
def getPN(init): #Generates PN Sequence
	n = 5
	l = pow(2,n)-1
	pn = []
	i = 0
	while(i<l+1):
		t = op.xor(init[0],init[4])
		j=4
		pn.append(init[4])
		while(j>0):
			init[j] = init[j-1]
			j=j-1
		init[0] = t
		i=i+1
	return pn
def split(inputSignal):
	sig1 = inputSignal[0:len(inputSignal)-4]
	inproc0 = sig1[len(sig1)/2+2:]
	inproc1 = sig1[2:len(sig1)/2]
	i = 0
	inPN0 = []
	inPN1 = []
	while(i<len(inproc0)):

		if(i%2!=0):
			inPN0.append(inproc0[i])
			inPN1.append(inproc1[i])
		i=i+1
	inN0 = recoverPN(inPN0)
	inN1 = recoverPN(inPN1)
	Sig = 10*int(inN1) + int(inN0)
	return Sig

def recoverPN(inPN):
	flag = 0
	i = 0
	while(flag ==0):
		count = 0
		for x, y in zip(inPN, getPN(getCode(i))):
			count = count + 1
        		if x != y:
				break
		if(count==32):
			return i
		i = i + 1
		if(i==10):
			print "invalid sequence"
#Main
def processInput(check): #Get input
	print "test"
	print "Check : ", check
	global inFlag
	if(inFlag == 0):
		inputSig = []
		while True:

			print "GPIO.input(7) : ",GPIO.input(7)
			if(GPIO.input(7) == True):
				inputSig.append(0)
			else:
				inputSig.append(1)
			time.sleep(0.05)
			if(len(inputSig)==136):
				print "Input complete. Signal length : ",len(inputSig)
				break
		global inputSignal
		inputSignal = inputSig
		print "inputSignal : ",inputSig,len(inputSig)
		inFlag = 1
inFlag = 0
#Setting up hardware. GPIO Pins
GPIO.setmode(GPIO.BOARD)
#Initialize pin 7 as input with pull down resistor
GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
try:
	print "GPIO.input(7) : ",GPIO.input(7)
	while(inFlag==0):
		if(GPIO.input(7)==1):
			processInput(1)
		random =1
	while(inFlag != 2):
		random =1
		if(inFlag==1):
            recoveredSignal = split(inputSignal)
			print "Recovered Signal : ",recoveredSignal
			inFlag = 2
	GPIO.cleanup() #Resets GPIO pins of RPi when complete

except KeyboardInterrupt:
	GPIO.cleanup() #Resets GPIO pins of RPi when force close
