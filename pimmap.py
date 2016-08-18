#!/usr/bin/env python
#  How to access GPIO registers via Python & mmap on the Raspberry-Pi
#  Adapted from C program by Dom and Gert, 15-Feb-2013
#  See http://elinux.org/RPi_Low-level_peripherals
# You'll also need
# http://www.raspberrypi.org/wp-content/uploads/2012/02/BCM2835-ARM-Peripherals.pdf
# to follow what's going on. Page numbers refer to this PDF.

import mmap
import struct
import time

BCM2708_PERI_BASE = 0x3F000000
GPIO_BASE = (BCM2708_PERI_BASE + 0x200000)    # GPIO controller
PAGE_SIZE = (4*1024)
BLOCK_SIZE = (4*1024)

LED = 13

# Set up gpio pointer for direct register access. When we perform the mmap.mmap() call below,
# this will become an array of bytes which is memory-mapped into the physical address space of
# the processor. Normal Python array operations (e.g. slices) are available.
gpio = []

def read_from_ptr(ofs):
    # Read a 32-bit word (four bytes)
    return struct.unpack("<L", gpio[4*ofs:4*ofs+4])[0]

def write_to_ptr(ofs, data):
    # Write a 32-bit word (four bytes)
    gpio[4*ofs:4*ofs+4] = struct.pack("<L", data)

# GPIO setup macros. The function select registers shown on pages 92 thru 94 assign 3 bits
# to control each GPIO pin, and have 10 pins per register. That's why you see "g / 10" and
# "((g % 10) * 3)" so frequently in the following functions. The three bit codes are 000
# for input, 001 for output, and 010-111 map to alternate functions 0 thru 5, described on
# pages 102 and 103. In Dom and Gert's code, it was necessary to call INP_GPIO on any pin
# before using OUT_GPIO or SET_GPIO_ALT in order to set the three bits to a known value (000)
# but I've rewritten those functions to clear the bits before ORing in the new value.

def INP_GPIO(g):
    shift = ((g % 10) * 3)
    x = read_from_ptr(g / 10)
    x &= ~(7 << shift)
    write_to_ptr(g / 10, x)

def OUT_GPIO(g):
    shift = ((g % 10) * 3)
    x = read_from_ptr(g / 10)
    x = (x & ~(7 << shift)) | (1 << shift)
    write_to_ptr(g / 10, x)

def SET_GPIO_ALT(g, a, m={0:4, 1:5, 2:6, 3:7, 4:3, 5:2}):
    # See three bit codes at the top of page 92
    shift = ((g % 10) * 3)
    x = read_from_ptr(g / 10)
    x = (x & ~(7 << shift)) | (m[a] << shift)
    write_to_ptr(g / 10, x)

def GPIO_SET(data):
    # Set bits which are 0, ignore bits which are 1
    write_to_ptr(7, data)     # See GPSET0 register on page 90

def GPIO_CLR(data):
    # Clears bits which are 1, ignore bits which are 0
    write_to_ptr(10, data)    # See GPCLR0 register on page 90

if __name__ == '__main__':
    with open('/dev/mem', 'r+b') as f:
        gpio = mmap.mmap(f.fileno(), BLOCK_SIZE, offset=GPIO_BASE)

        # Switch GPIO 13 to output mode
        OUT_GPIO(13)
        try:
            # flash some LEDs
            while True:
                GPIO_SET(1 << 13)
                #time.sleep(0.25)
                GPIO_CLR(1 << 13)
                #time.sleep(0.25)

        except KeyboardInterrupt:
            GPIO_CLR(1 << 13)