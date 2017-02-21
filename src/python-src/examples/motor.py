import RPi.GPIO as GPIO
import time
import sys


try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    print("Setup Done !!!!! yay Woho")
    ##The servos position is controlled by the pulsewidth 
    ##of a 50 Hz PWM signal. 
    ##Hence, we need to turn the PWM sequence on at 50 Hz
    pwm=GPIO.PWM(18, 50)

    ##Typically, the servo will go to the 
    ##  full left position when it sees a pulse width of 1 millisecond,  
    ##  middle position when it sees a pulse width of 1.5 millisecond, 
    ##  full right position when it sees a pulse width of 2 millisecond.
    ## DutyCycle = PulseWidth/(1/frequency) = PulseWidth * frequency
    ##  So in short
    ##   full left:  1ms,  5% duty cycle,  pwm.start(5)
    ##   middle position: 1.5ms  7.5% duty cycle, pwm.ChangeDutyCycle(7.5)
    ##   full right position: 2ms 10% duty cycle, pwm.ChangeDutyCycle(10)

    pwm.start(50)
    time.sleep(5)
    print("Started yayyyyyyyy mottttttoooooooooooeerrrrrr")

    pwm.ChangeDutyCycle(90)
    time.sleep(5)
    print("changed duty cycle")
    pwm.ChangeDutyCycle(10)
    pwm.stop()
    print("HALT")

except:
    print("ohhh nooooooooooooo", sys.exc_info()[0])
    print
finally:
    GPIO.cleanup()

