from mmap import mmap
import time, struct

GPIO2_offset = 0x481ac000
GPIO2_size = 0x481acfff-GPIO2_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
LED = 1<<7

with open("/dev/mem", "r+b" ) as f:
  mem = mmap(f.fileno(), GPIO2_size, offset=GPIO2_offset)

#with open("/sys/kernel/debug/omap_mux/lcd_data1", 'wb') as f:
#  f.write('27')

reg = struct.unpack("<L", mem[GPIO_OE:GPIO_OE+4])[0]
mem[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg & ~LED)

try:
  while(True):
    mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", LED)
    #time.sleep(0.5)
    mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", LED)
    #time.sleep(0.5)

except KeyboardInterrupt:
  mem.close()
