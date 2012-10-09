#!/usr/bin/env python
"""
    Provides an easy to use python interface to all the beagle io/adc stuff
"""

from getpass import getuser
from subprocess import check_output
from time import sleep

MUX_FOLDER = "/sys/kernel/debug/omap_mux/"
GPIO_FOLDER = "/sys/class/gpio/"
ENABLE_FILE = "export"
DIRECTION_FILE = "direction"
VALUE_FILE = "value"

MUX = {}
MUX[32] = ("gpmc_ad0", 7)
MUX[33] = ("gpmc_ad1", 7)
MUX[34] = ("gpmc_ad2", 7)
#MUX[35] =("gpmc_ad3", 7)
#commented out as it seems to fail at the mo :(
MUX[38] = ("gpmc_ad6", 7)
MUX[39] = ("gpmc_ad7", 7)
MUX[45] = ("gpmc_ad13", 7)
LED_DIRECTORY = "/sys/devices/platform/leds-gpio/leds/"

LED_FILES = {}
#LED_FILES[0] = "beaglebone\:\:usr0/brightness"
# Don't use LED 0 as it's used by other parts of the OS
LED_FILES[1] = "beaglebone::usr1/brightness"
LED_FILES[2] = "beaglebone::usr2/brightness"
LED_FILES[3] = "beaglebone::usr3/brightness"

AIN = {}
AIN[1] = "ain1"
AIN[2] = "ain2"
AIN[3] = "ain3"
AIN[4] = "ain4"
AIN[5] = "ain5"
AIN[6] = "ain6"
AIN_DIRECTORY = "/sys/devices/platform/omap/tsc/"


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


def get_ain(io):
    """
        Gets the value from and adc, converts it to an int and returns it
    """
    if not _check_ain(io):
        raise Exception("Unknown ADC, you should be using a different number")
    fname = AIN_DIRECTORY + AIN[io]
    try:
        f = open(fname, "r")
        reading = f.read()
        f.close()
        return int(reading)

    except IOError:
        raise Exception("Unable to read ADC please contact a demonstrator")


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
        print "%s" % reading
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
    return io in MUX.keys()


def _check_ain(io):
    """
        Checks that an ADC is known about and has therefore had it perms set
    """
    return io in AIN.keys()


def _check_led(led):
    """
        Checks to make sure you aren't trying to turn on a non existent LED
    """
    return led in LED_FILES.keys()


def _direction_filename(io):
    """
        Creates the filename for the direction file based on io number
    """
    return GPIO_FOLDER + "gpio%d" % io + "/" + DIRECTION_FILE


def _value_filename(io):
    """
        Creates the filename for the value file based on io number
    """
    return  GPIO_FOLDER + "gpio%d" % io + "/" + VALUE_FILE


def _led_filename(no):
    """
        Creates the filename to control the LED based on led number
    """
    return LED_DIRECTORY + LED_FILES[no]


def _setup_mux(io):
    """
        Sets up the mux values as needed for the IO stuff
    """
    fname, mux = MUX[io]
    filename = MUX_FOLDER + fname
    f = open(filename, "w")
    f.write("%d" % mux)
    f.close()


def _enable_io(io):
    """
        Enables the driver for a specific IO
    """
    fname = GPIO_FOLDER + ENABLE_FILE
    f = open(fname, "w")
    f.write("%d" % io)
    f.close()


def _install_analog_driver():
    """
        Installs the kernal module required for the analog stuff to work
    """
    check_output("modprobe ti_tscadc", shell=True)


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


def _setup():
    """
        Setups up the muxing, enabling, kernel mod and permissions for all io
        type operations
    """
    if not _check_root():
        raise Exception("Not root so cannot continue")
    _install_analog_driver()
    for io in MUX:
        _setup_mux(io)
        _enable_io(io)
        sleep(0.5)
        _change_ownership(_direction_filename(io))
    _change_ownership(LED_DIRECTORY + "*")
    led_on(2)  # Turn on LED as a sign it's succeded


if __name__ == "__main__":
    _setup()
