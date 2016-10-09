from __future__ import division
import time
from datetime import datetime
from urllib2 import Request, urlopen, URLError
import json
# from pprint import pprint

# Import the PCA9685 module.
import Adafruit_PCA9685


temperatureRange = [-15.,35.]
pressureRange=[960.,1060.]
humidityRange=[0.,1.]
windSpeedRange=[0.,25.]
precipProbabilityRange=[0.,1.]

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

def normalize(variable,minvalue,maxvalue):
    normvar=int((variable-minvalue)/(maxvalue-minvalue)*4095.)
    if(normvar > 4095):
        normvar = 4095
    if(normvar < 0):
        normvar = 0
    return normvar

while True:

    request = Request('https://api.darksky.net/forecast/ab148019f9563243649fab9e7193e470/42.3601,-71.0942')

    try:
      response = urlopen(request)
      currentweather = response.read()
        # print currentweather
    except URLError, e:
        print 'No Weather. Got an error code:', e
    

 
    weatherdata = json.loads(currentweather)
    #pprint(weatherdata)
    temperature = (weatherdata["currently"]["temperature"] - 32.)*5./9. #in degrees C
    pressure = weatherdata["currently"]["pressure"] # in millibar
    humidity = weatherdata["currently"]["humidity"] # in percentage
    windSpeed = weatherdata["currently"]["windSpeed"]*1.151 # in knots
    precipProbability = weatherdata["currently"]["precipProbability"] # in percentage


    normTemperature=normalize(temperature,temperatureRange[0],temperatureRange[1])
    normPressure=normalize(pressure,pressureRange[0],pressureRange[1])
    normHumidity=normalize(humidity,humidityRange[0],humidityRange[1])
    normWindSpeed=normalize(windSpeed,windSpeedRange[0],windSpeedRange[1])
    normPrecipProbability=normalize(precipProbability,precipProbabilityRange[0],precipProbabilityRange[1])
    
    print "Updating:", str(datetime.now()) 
    print "Temperature", temperature, normTemperature, float(normTemperature)*5./4095.
    print "Pressure", pressure, normPressure, float(normPressure)*5./4095.
    print "Humidity", humidity, normHumidity, float(normHumidity)*5./4095.
    print "WindSpeed", windSpeed, normWindSpeed, float(normWindSpeed)*5./4095.
    print "PrecipProbability", precipProbability, normPrecipProbability, float(normPrecipProbability)*5./4095.

    pwm.set_pwm(0, 0, normTemperature)
    pwm.set_pwm(1, 0, normPressure)
    pwm.set_pwm(2, 0, normHumidity)
    pwm.set_pwm(3, 0, normWindSpeed)
    pwm.set_pwm(4, 0, normPrecipProbability)
    time.sleep(180)
    


    