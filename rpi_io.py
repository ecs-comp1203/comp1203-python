#!/usr/bin/env python
"""
    Provides an easy to use python interface to all the io/adc stuff
"""

from getpass import getuser
from subprocess import check_output
from time import sleep
import spidev

_GPIO_FOLDER = "/sys/class/gpio/"
_ENABLE_FILE = "export"
_DIRECTION_FILE = "direction"
_VALUE_FILE = "value"

spi = spidev.SpiDev()
spi.open(0,0)

def led_off(led):
    """
        Turns one of the LEDs to the right of the RJ45 off
    """
    if _check_led(led):
        try:
            filename = _led_filename(led)
            f = open(filename, "w")
            f.write("0")
            f.close()
        except IOError:
            raise Exception("Unable to turn off LED, please contact a demonstrator")
    else:
        raise Exception("unknown LED, are you sure you have the right number?")


def led_on(led):
    """
        Turns one of the LEDs to the right of the RJ45 on
    """
    if _check_led(led):
        try:
            filename = _led_filename(led)
            f = open(filename, "w")
            f.write("1")
            f.close()
        except IOError:
            raise Exception("Unable to turn on LED, please contact a demonstrator")
    else:
        raise Exception("unknown LED, are you sure you have the right number?")


def on(io):
    """
        Turns on a gpio pin
    """
    if not _check_io(io):
        raise Exception("The IO isn't enabled, you should be using a different one")
    fname = _direction_filename(io)
    try:
        f = open(fname, "w")
        f.write("high")
        f.close()
    except IOError:
        raise Exception("Unable to toggle output, please contact a demonstrator")


def off(io):
    """
        Turns off a gpio pin
    """
    if not _check_io(io):
        raise Exception("The IO isn't enabled, you should be using a different one")
    fname = _direction_filename(io)
    try:
        f = open(fname, "w")
        f.write("low")
        f.close()
    except IOError:
        raise Exception("Unable to toggle output, please contact a demonstrator")



# read SPI data from MCP3008 ADC chip, 8 channels (adcnum 0 to 7)
def get_ain(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        r = spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout

def get_din(io):
    """
        Returns the status of the digital input as a boolean
    """
    if not _check_io(io):
        raise Exception("The IO isn't enabled, you should be using a different one")
    fname = _value_filename(io)
    try:
        f = open(fname, "r")
        reading = f.read().strip()
        f.close()
        return reading == "1"
    except IOError:
        raise Exception("Unable to read ADC please contact a demonstrator")

#  Functions from here on are todo with the initialisation of the system
#  and so shouldn't need to be called as part of the practical


def _get_number(port, number):
    """
        Maps from the port and number identifier to the IO number
        eg. 1.3 = 35
    """
    io = 32 * port + number
    return io


def _check_io(io):
    """
        Checks that an io port has been muxed and therefore is usable
    """
    return True


def _check_led(led):
    """
        Checks to make sure you aren't trying to turn on a non existent LED
    """
    return True
    #return led in _LED_FILES.keys()


def _gpio_foldername(io):
    """
        Creates the folder name for the io file specified
    """
    return _GPIO_FOLDER + "gpio%d" % io

def _direction_filename(io):
    """
        Creates the filename for the direction file based on io number
    """
    return _GPIO_FOLDER + "gpio%d" % io + "/" + _DIRECTION_FILE


def _value_filename(io):
    """
        Creates the filename for the value file based on io number
    """
    return  _GPIO_FOLDER + "gpio%d" % io + "/" + _VALUE_FILE


def set_output(io):
    """
        Enables the driver for a specific IO
    """
    fname = _direction_filename(io)
    f = open(fname, "w")
    f.write("out")
    f.close()

def set_input(io):
    """
        Enables the driver for a specific IO
    """
    fname = _direction_filename(io)
    f = open(fname, "w")
    f.write("in")
    f.close()

def _enable_io(io):
    """
        Enables the driver for a specific IO
    """
    fname = _GPIO_FOLDER + _ENABLE_FILE
    f = open(fname, "w")
    f.write("%d" % io)
    f.close()

def _check_root():
    """
        Checks to make sure that the script is being run by root,
        required as only root can make the changes needed to setup
    """
    return getuser() == "root"


def _change_ownership(filename):
    """
        Gives everyone write permissions on the files to save having to run as
        root.  Could use stricter permissions but this is easiest and security
        isn't a priority
    """
    check_output("/bin/chmod -R 777 %s" % filename, shell=True)
    #Using an external call as it's easy to check for failure

def setup():
    """
        Sets up up the muxing, enabling, kernel mod and permissions for all io
        type operations
    """
    for io in _BERRYCLIP:
        #print "%d" % _BERRYCLIP[io]
        #_enable_io(_BERRYCLIP[io])
        on(io)
        sleep(0.2)
        off(io)


if __name__ == "__main__":
    setup()
