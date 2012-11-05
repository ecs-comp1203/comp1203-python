#!/usr/bin/env python
"""
    Provides an easy to use python interface to all the beagle io/adc stuff
"""

from getpass import getuser
from subprocess import check_output
from time import sleep

__MUX_FOLDER = "/sys/kernel/debug/omap_mux/"
_GPIO_FOLDER = "/sys/class/gpio/"
_ENABLE_FILE = "export"
_DIRECTION_FILE = "direction"
_VALUE_FILE = "value"

_MUX = {}
_MUX[32] = ("gpmc_ad0", 7)
_MUX[33] = ("gpmc_ad1", 7)
_MUX[34] = ("gpmc_ad2", 7)
#_MUX[35] =("gpmc_ad3", 7)
#commented out as it seems to fail at the mo :(
_MUX[38] = ("gpmc_ad6", 7)
_MUX[39] = ("gpmc_ad7", 7)
_MUX[44] = ("gpmc_ad12", 7)
_MUX[45] = ("gpmc_ad13", 7)
_MUX[70] = ("lcd_data0", 27)
_MUX[71] = ("lcd_data1", 27)


_LED_DIRECTORY = "/sys/devices/platform/leds-gpio/leds/"

_LED_FILES = {}
#_LED_FILES[0] = "beaglebone\:\:usr0/brightness"
# Don't use LED 0 as it's used by other parts of the OS
_LED_FILES[1] = "beaglebone::usr1/brightness"
_LED_FILES[2] = "beaglebone::usr2/brightness"
_LED_FILES[3] = "beaglebone::usr3/brightness"

_AIN = {}
_AIN[1] = "ain1"
_AIN[2] = "ain2"
_AIN[3] = "ain3"
_AIN[4] = "ain4"
_AIN[5] = "ain5"
_AIN[6] = "ain6"
_AIN_DIRECTORY = "/sys/devices/platform/omap/tsc/"


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
    fname = _AIN_DIRECTORY + _AIN[io]
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
    return io in _MUX.keys()


def _check_ain(io):
    """
        Checks that an ADC is known about and has therefore had it perms set
    """
    return io in _AIN.keys()


def _check_led(led):
    """
        Checks to make sure you aren't trying to turn on a non existent LED
    """
    return led in _LED_FILES.keys()


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


def _led_filename(no):
    """
        Creates the filename to control the LED based on led number
    """
    return _LED_DIRECTORY + _LED_FILES[no]


def _setup_mux(io):
    """
        Sets up the mux values as needed for the IO stuff
    """
    fname, mux = _MUX[io]
    filename = __MUX_FOLDER + fname
    f = open(filename, "w")
    f.write("%d" % mux)
    f.close()


def _enable_io(io):
    """
        Enables the driver for a specific IO
    """
    fname = _GPIO_FOLDER + _ENABLE_FILE
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

def _setup_serials():
    """
        Muxes the serial ports into existence
    """
    check_output("echo 0 > /sys/kernel/debug/omap_mux/uart1_txd", shell=True)
    check_output("echo 20 > /sys/kernel/debug/omap_mux/uart1_rxd", shell=True)
    check_output("echo 1 > /sys/kernel/debug/omap_mux/spi0_d0", shell=True)
    check_output("echo 21 > /sys/kernel/debug/omap_mux/spi0_sclk", shell=True)
    check_output("echo 06 > /sys/kernel/debug/omap_mux/gpmc_wpn", shell=True)
    check_output("echo 26 > /sys/kernel/debug/omap_mux/gpmc_wait0", shell=True)
    check_output("echo 4 >  /sys/kernel/debug/omap_mux/lcd_data8", shell=True)
    check_output("echo 24 >  /sys/kernel/debug/omap_mux/lcd_data9", shell=True)

def _setup():
    """
        Setups up the muxing, enabling, kernel mod and permissions for all io
        type operations
    """
    if not _check_root():
        raise Exception("Not root so cannot continue")
    _install_analog_driver()
    for io in _MUX:
        _setup_mux(io)
        _enable_io(io)
        sleep(0.5)
        _change_ownership(_direction_filename(io))
    _change_ownership(_LED_DIRECTORY + "*")
    _setup_serials()
    led_on(2)  # Turn on LED as a sign it's succeded


if __name__ == "__main__":
    _setup()
