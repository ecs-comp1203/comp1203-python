"""
    Provides an easy to use python interface to all the adc stuff
    Assumes Raspberry Pi with MCP3008 ADC
    By Laurie Kirkcaldy
"""

import spidev


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=400000

def get_ain(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        r = spi.xfer2([1,(8+adcnum)<<4,0])
        data = ((r[1]&3) << 8) + r[2]
        return data
        

