import serial
import sys
import serial.tools.list_ports
import time

# Code for using the spaceship controller with Python (or any lang that can read from serial)
#               
#                                     `. ___
#                                    __,' __`.                _..----....____
#                        __...--.'``;.   ,.   ;``--..__     .'    ,-._    _.-'
#                  _..-''-------'   `'   `'   `'     O ``-''._   (,;') _,'
#                ,'________________                          \`-._`-','
#                 `._              ```````````------...___   '-.._'-:
#                    ```--.._      ,.                     ````--...__\-.
#                            `.--. `-`                       ____    |  |`
#                              `. `.                       ,'`````.  ;  ;`
#                                `._`.        __________   `.      \'__/`
#                                   `-:._____/______/___/____`.     \  `
#                                               |       `._    `.    \
#                                               `._________`-.   `.   `.___
#                                                             SSt  `------'`
#
# Author: Ulrik Guenther <hello@ulrik.is>
#
# The spaceship controller needs to be driven with at least 7.5V to the CAN bus connector in
# the back of the controller. 5V doesn't seem to be enough and the CAN bus spec declares anything
# between 5V and 24V as alright. Pin 6 of the DB9 connector is Ground, Pin 9 is PWR.
#
# The USB connector on the back of the controller does not do anything, but connect to the physical
# keyboard on the controller.
#
# The serial connector uses a standard RS232 protocol, with 115.2kbaud, no flow control, 8 data bits,
# one stop bit.
#
# Pads:
#  * E0 - Magnification
#  * E1 - Stigmator X
#  * E2 - Stigmator Y
#  * E3 - Aperture X
#  * E4 - Aperture Y
#  * EA - Scan Rotate
#  * E5 - Shift X
#  * E6 - Shift Y
#  * E7 - Brightness
#  * E8 - Contrast
#  * E9 - Focus
#
# Buttons:
#  * S0 - Reduced
#  * S1 - Wobble
#  * S2 - Freeze
#  * S3 - Exchange
#  * S4 - Resume
#  * S5 - Camera
#  * S6 - Minus
#  * S7 - Plus
def __main__(argv):
    print("Spaceship controller")
    print("Available COM ports:")
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
    	print(p)
    print("----------------------------")
    print("Connecting to " + argv[1])
    ser = serial.Serial(argv[1], 115200, xonxoff=False, rtscts=False, dsrdtr=False)
    print("connected to: " + ser.portstr)

    seq = []
    count = 1

    # state of the keys and pads is stored in a dictionary,
    # values for the pads are relative to the initial position,
    # values for the buttons are toggleable (0 or 1).
    state = dict()

    while True:
        # This will read all the characters coming in from the serial port,
	    # stopping at new line. The general format of each command packet sent by
	    # the spaceship controller is:
	    # 
	    #    +---------+---------+---------+---------+
	    #    | GARGAGE | TYPE    | CHANGE  | LFCR    |
	    #    | 4 Bytes | 2 Bytes | 4 Bytes | 2 Bytes |
	    #    +---------+---------+---------+---------+
	    #
		# Example: ____E0+012\n\r - signifying a change of 12 in pad 0
		#
		# The garbage part I haven't been able to decipher, but it's always the same,
		# so probably does not have any special meaning.
        for c in ser.read():
            seq.append(chr(c))
            joined_seq = ''.join(str(v) for v in seq)

            if chr(c) == '\n':
				# This splits the read string into the part that contains the switch name,
				# and the current change. We might receive empty packets, so we strip the change
				# and check for length > 0.
                switch = joined_seq[6:8]
                change = joined_seq[8:12].strip()

                if len(change) == 0:
                    seq = []
                    count += 1
                    break

                # We got a change in a control pad.
                if switch[0] == 'E':
                    if switch in state: 
                        state[switch] = state[switch] + int(change)
                    else:
                        state[switch] = int(change)
		        # We got a change in a toggleable switch, so toggle it.
                if switch[0] == 'S':
                    if switch in state:
                        state[switch] = state[switch] ^ int(change)
                    else:
                        state[switch] = int(change)

                print("State of " + switch + "=" + str(state[switch]))
                seq = []
                count += 1
                break
        
    ser.close()

__main__(sys.argv)
