
from time import sleep
import Adafruit_BBIO.GPIO as GPIO



def silnikrobibrr(enA='P9_23',in1="P9_25",in2="P9_27"):
    
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    sleep(0.1)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)

silnikrobibrr()