import RPi.GPIO as GPIO
import time
import sys

pin=32 #12 on board
#pin=12 #18 on board, default hardware pwm port. in our case, it does not work
#pin=16 #23 on board. does not support pwm

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([pin], GPIO.OUT)
    print("Setup Done !!!!! yay Woho")
    
    #GPIO.output(pin, 1)
    #time.sleep(20)
    #GPIO.output(pin, 0)
    #print("set to low now")
    #time.sleep(20)
    print("start pwm")

    ##The servos position is controlled by the pulsewidth 
    ##of a 50 Hz PWM signal. 
    ##Hence, we need to turn the PWM sequence on at 50 Hz
    pwm=GPIO.PWM(pin, 50)

    ##Typically, the servo will go to the 
    ##  full left position when it sees a pulse width of 1 millisecond,  
    ##  middle position when it sees a pulse width of 1.5 millisecond, 
    ##  full right position when it sees a pulse width of 2 millisecond.
    ## DutyCycle = PulseWidth/(1/frequency) = PulseWidth * frequency
    ##  So in short
    ##   full left:  1ms,  5% duty cycle,  pwm.start(5)
    ##   middle position: 1.5ms  7.5% duty cycle, pwm.ChangeDutyCycle(7.5)
    ##   full right position: 2ms 10% duty cycle, pwm.ChangeDutyCycle(10)
    time.sleep(10)

    print("start 5 ...")
    pwm.start(5)
    time.sleep(10)

    print("7.5 ...")
    pwm.ChangeDutyCycle(7.5)
    time.sleep(10)
    print("10 ...")
    pwm.ChangeDutyCycle(10)
    time.sleep(10)
    print("6 ...")
    pwm.ChangeDutyCycle(6)
    time.sleep(10)
    print("0 ...")
    pwm.ChangeDutyCycle(0)
    time.sleep(10)

    #pwm.ChangeDutyCycle(20)
    #pwm.ChangeDutyCycle(40)
    #pwm.ChangeDutyCycle(70)
    print("stop ...")
    pwm.stop()
    time.sleep(10)
    
    print("HALT")

except:
    print("ohhh nooooooooooooo", sys.exc_info()[0])
finally:
    GPIO.cleanup()

