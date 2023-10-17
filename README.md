# Lightning Simulator for Tuya Smart Bulbs

This is a port of a lightning effect orginally made for Arduino.
It was created by secretreeve and can be found at
https://forum.arduino.cc/t/lightning-effect-with-3-leds/1010662/30

This version is made for smart bulbs powered by Tuya (which is plenty).
The ones I'm using are e-luminate Smart Candle E14, which can be acquired
for £5 from Home Bargains in the UK (it's set to control three of them).
Intstructions for setting up the bulbs and getting the dev keys can be found at
https://pypi.org/project/tinytuya/

Once you have these, add the details to the bulb objects and have a play with
the variables that control things like timings, if you like. It should then
run as a standard python script.

Notes and TODOs:

- You can fix the sequence of bulb flashes rather than use random ones.
    This can allow flahes that spread through different rooms in order.
    Check the comments for details.

- It doesn't wait for a response from the bulbs, in order to speed things up.
    However, this means some flashes are missed - I may fix it, but the 
    randomness isn't too bad.

- I need to play with the brightness adjustments again as I think I messed
    those parts up, meaning full power with every flash.

- It's a standalone program at the moment but I'm making an API that integrates it,
    along with some other scenes. They can then be triggered from other devices.

- Oh, and I'm setting this lightning scene up for a Halloween display, but I haven't
    verified the security of the bulbs, nor how much is tracked (beyond a brief network 
    packet check). I'm not sure if I'll keep them up year-long, so use at your own 
    discretion, as you should with all IoT devices.