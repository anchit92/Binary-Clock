#!/usr/bin/python2
import spidev
import ws2812
from time import sleep
import datetime
import traceback

import RPi.GPIO as gpio
from time import sleep

#gpio setup
BtnPin = 15                  
gpio.setmode(gpio.BOARD)
gpio.setup(BtnPin, gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.setup(10,gpio.OUT,gpio.HIGH)

#spi setup
spi = spidev.SpiDev()
spi.open(0,0)
#color setup 
HH_COLOR = [0,10,10]
MM_COLOR = [10,10,0]
SS_COLOR = [10,0,10]
EMPTY_LED = [0,0,0]

#Led ids for each column. most significant first least significant last

Hh =[7,6]
hH =[18,17,8,5]
Mm =[16,9,4]
mM =[19,15,10,3]
Ss =[14,11,2]
sS =[20,13,12,1]

def Led_list(time):
    """ 
    Create list with correct values for led to display
    will create an array with 21 elements(21 leds in my clock)
    [0,0,0] for off
    0th LED always off
    """

    hour_tens= "{0:02b}".format(int(time.hour/10))
    hour_units= "{0:04b}".format(int(time.hour%10))
    minute_tens= "{0:03b}".format(int(time.minute/10))
    minute_units= "{0:04b}".format(int(time.minute%10))
    second_tens= "{0:03b}".format(int(time.second/10))
    second_units= "{0:04b}".format(int(time.second%10))
    LED_ARRAY=[EMPTY_LED]
    #Empty LED Array!!
    for i in range (21):
        LED_ARRAY.append(EMPTY_LED)
    #hours leds
    #hour tens
    for index,i in enumerate(hour_tens):
        if i=="1":
            LED_ARRAY[Hh[index]]=HH_COLOR
    #hour units
    for index,i in enumerate(hour_units):
        if i=="1":
            LED_ARRAY[hH[index]]=HH_COLOR
    #Minutes Leds
    #Minutes Tens
    for index,i in enumerate(minute_tens):
        if i=="1":
            LED_ARRAY[Mm[index]]=MM_COLOR
    #Minutes Units
    for index,i in enumerate(minute_units):
        if i=="1":
            LED_ARRAY[mM[index]]=MM_COLOR
    #Seconds Leds
    #Seconds Tens
    for index,i in enumerate(second_tens):
        if i=="1":
            LED_ARRAY[Ss[index]]=SS_COLOR
    #Seconds Units
    for index,i in enumerate(second_units):
        if i=="1":
            LED_ARRAY[sS[index]]=SS_COLOR
    return LED_ARRAY

def test_off(spi, nLED):
    """
    Clears LED to show blank
    """
    ws2812.write2812(spi, [[0,0,0]*nLED])

def clock(time,Led_old):
    Led_data=Led_list(time)
    if Led_old!=Led_data:
        ws2812.write2812(spi,Led_data)
    return Led_data

def button_check(Display):
    input_value = gpio.input(BtnPin)
    if input_value == False:
        sleep(.5)
        Display=not Display
    return Display

def sleep_time(Display,time):
    if Display==True:
        if time.hour == 00 and time.second == 00 and time.minute==00:
            Display=False
            return Display
    if Display == False:
        if time.hour == 6 and time.second ==00 and time.minute == 00:
            Display=True
    return Display

def main():
    Led_old=0
    Led_data=1
    Display=True #if True show clock, if False dont show clock
    try:
        while True:
            time=datetime.datetime.time(datetime.datetime.now())
            Display=button_check(Display) 
            Display=sleep_time(Display,time)
            if Display:
                Led_data=clock(time,Led_old)
                Led_old=Led_data
            else:
                test_off(spi,21)
            sleep(.01)
    except KeyboardInterrupt:
        print ("Keyboard Interrupt caught")
        test_off(spi,21)
        raise
    except Exception as e:
        trace = traceback.format_exc()
        print (trace)
        test_off(spi,21)
    return

if __name__ == '__main__':
    main()

