from bottle import route, run
import beagle_io                                                             
from time import sleep                                                          
#this sets up a web server on port 8080. 
# Access it with a web browser at http://10.0.0.10:8080/       
                                                                                
# this sets up the url /hello/name which prints "Hello name" if requested
@route('/hello/:name')
@route('/hello')
def index(name='World'):
    return '<b>Hello %s!</b>' % name

# this defines a URL which flashes the LED on port38
@route('/ledon')
def index(name='ledon'):
    beagle_io.on(38)                                                     
    sleep(0.5)                                                             
    beagle_io.off(38) 

# thus makes a url /adc which returns the adc reading of adc1
@route('/adc')
def index(name='adc'):
    return '<p> %s</p>' % beagle_io.getAdc(2)

run(host='0.0.0.0', port=8080)
