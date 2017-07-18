# Spaceship Controller
```
              
                                    `. ___
                                   __,' __`.                _..----....____
                       __...--.'``;.   ,.   ;``--..__     .'    ,-._    _.-'
                 _..-''-------'   `'   `'   `'     O ``-''._   (,;') _,'
               ,'________________                          \`-._`-','
                `._              ```````````------...___   '-.._'-:
                   ```--.._      ,.                     ````--...__\-.
                           `.--. `-`                       ____    |  |`
                             `. `.                       ,'`````.  ;  ;`
                               `._`.        __________   `.      \'__/`
                                  `-:._____/______/___/____`.     \  `
                                              |       `._    `.    \
                                              `._________`-.   `.   `.___
                                                            SSt  `------'`

```

## Setup
### Python

SpaceshipController requires:

* Python 3.6+
* [PySerial](https://pythonhosted.org/pyserial/) (`pip3 install pyserial` or `conda install pyserial`)

So far, it has only been tested on Windows, but should work on Linux/OSX as well.
	
### Power
The spaceship controller needs to be driven with at least 7.5V to the CAN bus connector in
the back of the controller. 5V doesn't seem to be enough and the CAN bus spec declares anything
between 5V and 24V as alright. Pin 6 of the DB9 connector is Ground, Pin 9 is PWR.

### USB
The USB connector on the back of the controller does not do anything, but connect to the physical
keyboard on the controller.

### Serial
The serial connector uses a standard RS232 protocol, with 115.2kbaud, no flow control, 8 data bits,
one stop bit.

## Button names
Pads:
 * E0 - Magnification
 * E1 - Stigmator X
 * E2 - Stigmator Y
 * E3 - Aperture X
 * E4 - Aperture Y
 * EA - Scan Rotate
 * E5 - Shift X
 * E6 - Shift Y
 * E7 - Brightness
 * E8 - Contrast
 * E9 - Focus

Buttons:
 * S0 - Reduced
 * S1 - Wobble
 * S2 - Freeze
 * S3 - Exchange
 * S4 - Resume
 * S5 - Camera
 * S6 - Minus
 * S7 - Plus
 
## Running

* Windows: `python spaceship.py COM1`, where COM1 is the port the controller is connected to.
* Linux/OSX: `python spaceship.py /dev/ttyS1`, where `/dev/ttyS1` is the serial device the controller is connected to.
 
## More

For more documentation of the packet format, see `spaceship.py`.