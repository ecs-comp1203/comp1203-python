#!/usr/bin/env python
from bottle import route, run
import rpi_io                                                             
from time import sleep                                                          
#this sets up a web server on port 8080. 
# Access it with a web browser at http://YourPiIP:8080
# or on the Pi's web browser at http://localhost:8080
LED = 13                                                                    
# this sets up the url /hello/name which prints "Hello name" if requested
@route('/hello/:name')
@route('/hello')
def index(name='World'):
    return '<b>Hello %s!</b>' % name

# this defines a URL which flashes the LED once
@route('/ledon')
def index(name='ledon'):
    rpi_io.on(LED)                                                     
    sleep(0.5)                                                             
    rpi_io.off(LED) 

# thus makes a url /adc which returns the adc reading
@route('/adc')
def index(name='adc'):
    return '<p> %s</p>' % rpi_io.get_ain(0)

run(host='0.0.0.0', port=8080)
