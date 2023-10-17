#!/usr/bin/python3

# Lightning Simulator for Tuya Smart Bulbs

# This is a port of a lightning effect orginally made for Arduino.
# It was created by secretreeve and can be found at
# https://forum.arduino.cc/t/lightning-effect-with-3-leds/1010662/30

# This version is made for smart bulbs powered by Tuya (which is plenty).
# The ones I'm using are e-luminate Smart Candle E14, which can be acquired
# for £5 from Home Bargains in the UK (it's set to control three of them).
# Intstructions for setting up the bulbs and getting the dev keys can be found at
# https://pypi.org/project/tinytuya/

# Once you have these, add the details to the bulb objects and have a play with
# the variables that control things like timings, if you like. It should then
# run as a standard python script.

# See included readme for more details

from tinytuya import BulbDevice
from enum import Enum
import random
import time

start_time = round(time.time()*1000)

# rename these BulbDevice variables if you wish, then add to enum below
first_light = BulbDevice(
    dev_id='DEV_ID_HERE',
    address='IP_ADDRESS_HERE',
    local_key='LOCAL_KEY_HERE', 
    version=3.4) # Check the version number and adjust if needed
first_light.set_socketPersistent(True)

second_light = BulbDevice(
    dev_id='DEV_ID_HERE',
    address='IP_ADDRESS_HERE',
    local_key='LOCAL_KEY_HERE', 
    version=3.4) # Check the version number and adjust if needed
second_light.set_socketPersistent(True)

third_light = BulbDevice(
    dev_id='DEV_ID_HERE',
    address='IP_ADDRESS_HERE',
    local_key='LOCAL_KEY_HERE', 
    version=3.4) # Check the version number and adjust if needed
third_light.set_socketPersistent(True)

# If you renamed the BulbDevices, add the names here
class Bulbs(str, Enum):
    first_lightbulb = "first_light"
    second_lightbulb = "second_light"
    third_lightbulb = "third_light"

class States(str, Enum):
    state_new = "state_new"
    state_main_flash = "state_main_flash"
    state_second_flash = "state_second_flash"
    state_third_flash = "state_third_flash"
    
current_state =States.state_new
just_entered_this_state = True
current_millis : int
previousPulse : int
pulse_interval = 500
pulse_state : bool
how_many_bulbs = len(Bulbs)

flash_lengths = [0, 0, 0] # will be populated each time, between the min and max
flash_lengths_min = [100, 100, 75] # experiment with these
flash_lengths_max = [300, 300, 250]
intervals = [0, 0, 0] #will be populated each time, between the min and max
intervals_min = [1000, 5, 5] # between 3nd flash and new main flash, main and 2nd, 2nd and 3rd
intervals_max = [2500, 30, 30]
second_flash_intensity = 800 # experiment with these
third_flash_intensity = 300
flash_is_done = False
random_numbers = [0, 3] # TODO: Change magic numbers for these
HIGH = 1000
LOW = 0

bulb_sequence = [0, 1, 2] # <-- Use this fixed sequence by commenting out makrked line further down
entered_this_state_at_millis = 0
flash_ended_at_millis = 0

def get_bulb(bulb):
    if bulb is Bulbs.first_lightbulb or bulb == 0:
        return first_light
    elif bulb is Bulbs.second_lightbulb or bulb == 1:
        return second_light
    else:
        return third_light

def reset_bulbs():
    for bulb in Bulbs:
        this_bulb = get_bulb(bulb)
        this_bulb.turn_on(nowait=True)
        this_bulb.set_white(1000, 1000, nowait=True)
        this_bulb.turn_off(nowait=True)

def randomize_sequence():
    global bulb_sequence
    print(" Sequence: ", end='')
    bulb_sequence[0] = random.randrange(0, 3)
    bulb_sequence[1] = random.randrange(0, 3)
    bulb_sequence[2] = random.randrange(0, 3)
    print(bulb_sequence[0], end='')
    print(bulb_sequence[1], end='')
    print(bulb_sequence[2])

    while bulb_sequence[1] == bulb_sequence[0]:
        bulb_sequence[1] = random.randrange(0, 3)
    print(bulb_sequence[1])

    while (bulb_sequence[2] == bulb_sequence[0]) or (bulb_sequence[2] == bulb_sequence[1]):
        bulb_sequence[2] = random.randrange(0, 3)
    print(bulb_sequence[2])

def randomize_intervals():
    global intervals
    intervals[0] = random.randrange(intervals_min[0], intervals_max[0])
    print(" Main interval: ", end='')
    print(intervals[0])
    intervals[1] = random.randrange(intervals_min[1], intervals_max[1])
    print(" 2nd interval: ", end='')
    print(intervals[1])
    intervals[2] = random.randrange(intervals_min[2], intervals_max[2])
    print(" 3rd interval: ", end='')
    print(intervals[2])

def randomize_flash_lengths():
    global flash_lengths
    flash_lengths[0] = random.randrange(flash_lengths_min[0], flash_lengths_max[0])
    print(" Main flash: ", end='')
    print(flash_lengths[0])
    flash_lengths[1] = random.randrange(flash_lengths_min[1], flash_lengths_max[1])
    print(" 2nd flash: ", end='')
    print(flash_lengths[1])
    flash_lengths[2] = random.randrange(flash_lengths_min[2], flash_lengths_max[2])
    print(" 3rd flash: ", end='')
    print(flash_lengths[2])

def do_lightning():
    global current_state
    global just_entered_this_state
    global entered_this_state_at_millis
    global current_millis
    global intervals
    global flash_is_done
    global flash_lengths
    global flash_ended_at_millis
    global second_flash_intensity
    global third_flash_intensity

    if current_state is States.state_new:
        if just_entered_this_state == True:
            print("state_new")
            randomize_sequence() # <-- Comment this out to use the fixed sequence futher up
            randomize_intervals()
            randomize_flash_lengths()
            just_entered_this_state = False
            entered_this_state_at_millis = current_millis

        if current_millis - entered_this_state_at_millis >= intervals[0]:
            current_state = States.state_main_flash
            just_entered_this_state = True
        
    elif current_state is States.state_main_flash:
        this_bulb = get_bulb(bulb_sequence[0])
        if just_entered_this_state == True:
            print("state_main_flash")
            entered_this_state_at_millis = current_millis
            this_bulb.set_brightness(HIGH, nowait=True)
            this_bulb.turn_on(nowait=True)
            print("     main_flash ON ", end='')
            print(current_millis)
            flash_is_done = False
            just_entered_this_state = False

        if flash_is_done == False and current_millis - entered_this_state_at_millis >= flash_lengths[0]: # This is the flash
            flash_is_done = True
            flash_ended_at_millis = current_millis
            this_bulb.turn_off(nowait=True)
            print("     main_flash OFF ", end='')
            print(current_millis)

        if flash_is_done and current_millis - flash_ended_at_millis >= intervals[1]: # This is the inter-flash interval
            current_state = States.state_second_flash
            just_entered_this_state = True

    elif current_state is States.state_second_flash:
        this_bulb = get_bulb(bulb_sequence[1])
        if just_entered_this_state == True:
            print("state_second_flash")
            entered_this_state_at_millis = current_millis
            this_bulb.set_brightness(second_flash_intensity, nowait=True)
            this_bulb.turn_on(nowait=True)
            print("     2nd_flash ON ", end='')
            print(current_millis)
            flash_is_done = False
            just_entered_this_state = False

        if flash_is_done == False and current_millis - entered_this_state_at_millis >= flash_lengths[1]: # This is the flash
            flash_is_done = True
            flash_ended_at_millis = current_millis
            this_bulb.turn_off(nowait=True)
            print("     2nd_flash OFF ", end='')
            print(current_millis)

        if flash_is_done and current_millis - flash_ended_at_millis >= intervals[2]: # This is the inter-flash interval
            current_state = States.state_third_flash
            just_entered_this_state = True

    elif current_state is States.state_third_flash:
        this_bulb = get_bulb(bulb_sequence[2])
        if just_entered_this_state == True:
            print("state_3rd_flash")
            entered_this_state_at_millis = current_millis
            this_bulb.set_brightness(third_flash_intensity, nowait=True)
            this_bulb.turn_on(nowait=True)
            print("     3rd_flash ON ", end='')
            print(current_millis)
            flash_is_done = False
            just_entered_this_state = False

        if flash_is_done == False and current_millis - entered_this_state_at_millis >= flash_lengths[2]: # This is the flash
            flash_is_done = True
            flash_ended_at_millis = current_millis
            this_bulb.turn_off(nowait=True)
            print("     3rd_flash OFF ", end='')
            print(current_millis)

        if flash_is_done:
            current_state = States.state_new
            just_entered_this_state = True
            print("*** Heading back to the start... ***")

reset_bulbs()

while True: # Main loop
    current_millis = int(time.time() * 1000) - start_time
    do_lightning()