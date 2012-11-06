/* example of memory mapped IO on beagle bone
* used instead of the /dev/ i/O as it is faster
*/
#define GPIO1_START           0x4804C000 
main()
{

    int raw_fd = open("/dev/mem", O_RDWR | O_SYNC); 

    gpio = (ulong*) mmap(NULL, 0xFFF, PROT_READ | PROT_WRITE, MAP_SHARED, 
raw_fd, GPIO1_START); 

//this will return the gpio status of the 
printf("GPIO Input register state %x ", gpio[0x138/4]);

}
