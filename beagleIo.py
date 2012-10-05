# Useful I/O functions for the Beagle Bone
from MuxSettings import MuxSettings

from time import sleep

MUX_FOLDER = "/sys/kernel/debug/omap_mux/"
GPIO_FOLDER = "/sys/class/gpio/"
ENABLE_FILE = "export"
DIRECTION_FILE = "direction"

MUX = {}
MUX[32] = MuxSettings("gpmc_ad0", 7)
MUX[33] = MuxSettings("gpmc_ad1", 7)
MUX[34] = MuxSettings("gpmc_ad2", 7)
#MUX[35] = MuxSettings("gpmc_ad3", 7)
#commented out as it seems to fail at the mo :(
MUX[38] = MuxSettings("gpmc_ad6", 7)
MUX[39] = MuxSettings("gpmc_ad7", 7)

LED_DIRECTORY = "/sys/devices/platform/leds-gpio/leds/"

LED_FILES = {}
#LED_FILES[0] = "beaglebone\:\:usr0/brightness"
# Don't use LED 0 as it's used by other parts of the OS
LED_FILES[1] = "beaglebone::usr1/brightness"
LED_FILES[2] = "beaglebone::usr2/brightness"
LED_FILES[3] = "beaglebone::usr3/brightness"

AIN = {}
AIN[2] = "ain2"
AIN_DIRECTORY = "/sys/devices/platform/omap/tsc/"

def get_number(port, number):
    """
        Maps from the port and number identifier to the IO number
        eg. 1.3 = 35
    """
    io = 32 * port + number
    return io

def checkIo(io):
    """
        Checks that an io port has been muxed and therefore is usable
    """
    return io in MUX.keys()

def checkAin(io):
    """
        Checks that an ADC is known about and has therefore had it perms set
    """
    return io in AIN.keys()

def checkLed(led):
    """
        Checks to make sure you aren't trying to turn on a non existent LED
    """
    return led in LED_FILES.keys()

def ledOff(led):
    """
        Turns one of the LEDs to the right of the RJ45 off
    """
    if checkLed(led):
        try:
            filename = LED_DIRECTORY + LED_FILES[led]
            f = open(filename, "w")
            f.write("0")
            f.close()
        except IOError:
            print "Unable to turn LED off"
    else:
        print "Invalid LED number"

def ledOn(led):
    """
        Turns one of the LEDs to the right of the RJ45 on
    """
    if checkLed(led):
        try:
            filename = LED_DIRECTORY + LED_FILES[led]
            f = open(filename, "w")
            f.write("1")
            f.close()
        except IOError:
            print "Unable to turn LED on"
    else:
        print "Invalid LED number"


def on(io):
    fname = GPIO_FOLDER + "gpio%d" % io + "/" + DIRECTION_FILE
    try:
        f = open(fname, "w")
        f.write("high")
        f.close()
    except IOError:
        print("File does not exist.  Has IO %d been enabled?" % io)

def off(io):
    fname = GPIO_FOLDER + "gpio%d" % io + "/" + DIRECTION_FILE
    try:
        f = open(fname, "w")
        f.write("low")
        f.close()
    except IOError:
        print("File does not exist.  Has IO %d been enabled" % io)

def getAdc(io):
    fname = AIN_DIRECTORY + AIN[io]
    try:
        f = open(fname, "r")
        reading = f.read()
        f.close()
        return int(reading)

    except IOError:
        print("File does not exist.  Has IO %d been enabled" % io)

"""
 Functions from here on are todo with the initialisation of the system
 and so shouldn't need to be called as part of the practical
"""
def setupMux(io):
    filename = MUX_FOLDER + MUX[io].fname
    f = open(filename, "w")
    f.write("%d" % MUX[io].mux)
    f.close()

def enableIo(io):
    fname = GPIO_FOLDER + ENABLE_FILE
    f = open(fname, "w")
    f.write("%d" % io)
    sleep(0.5)
    f.close()
