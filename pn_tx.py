import time
import operator as op
import RPi.GPIO as GPIO
#Output helper functions
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
def processPN(pn): #interveave pn sequence with 1s
	i = 0
	j = 0
	pn1 = []
	while(j<32):
		if(i%2==0):
			pn1.append(1)
		else:
			pn1.append(pn[j])
			j = j+1
		i = i + 1
	pn1.insert(0,0)
	pn1.insert(0,0)
	return pn1
def Output(out): #Output values
	i=0
	while(i<len(out)):
		if(out[i]==1):
			GPIO.output(11,False)
			out[i]=0
		else:
			GPIO.output(11,True)
			out[i]=1
		print "OUT : ",out[i]
		time.sleep(0.05)
		i = i + 1
	print "Finished transmission. Transmission length: ",len(out)
#Setting up hardware. GPIO Pins
GPIO.setmode(GPIO.BOARD)
#Initialize pin 11 as output with pull down resistor and give initial value
GPIO.setup(11,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
GPIO.output(11,False)
num = input("Enter 2 digit number: ")
n0 = num%10
n1 = num/10
bin0 = []
bin1 = []
bin0 = getCode(n0)
bin1 = getCode(n1)
pn0 = getPN(bin0)
pn1 = getPN(bin1)
proc0 = processPN(pn0)
proc1 = processPN(pn1)
out = proc1+proc0 + [0,0,0,0]
print len(out)
Output(out)
try:
    GPIO.cleanup() #Resets GPIO pins of RPi when finish
except KeyboardInterrupt:
    GPIO.cleanup() #Resets GPIO pins of RPi when force close
