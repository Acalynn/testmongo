import requests
import json
import sys
import time

from DFRobot_MAX17043 import DFRobot_MAX17043
import RPi.GPIO as GPIO

gauge = DFRobot_MAX17043()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

def interruptCallBack(channel):
  gauge.clear_interrupt()
  print('Low power alert interrupt!')
  #put your battery low power alert interrupt service routine here
  
GPIO.add_event_detect(7, GPIO.FALLING, callback = interruptCallBack, bouncetime = 5)

rslt = gauge.begin()

while rslt != 0:
  print('gauge begin faild')
  time.sleep(2)
  rslt = gauge.begin()
  
  
gauge.set_interrupt(32) #use this to modify alert threshold as 1% - 32% (integer)
print('gauge begin successful')

url = 'https://ap-southeast-1.aws.data.mongodb-api.com/app/data-tsyze/endpoint/data/v1/action/updateOne'
headers = {
    'Content-Type': 'application/json',
    'api-key': 'uHmJBOxG6d3QuSmQ3UpduGfHkOY0rQth2vPNOEHwQwonsRJkAFSp3u1YlfoWHFRw',
    'Accept': 'application/ejson'
}


iteration = 1

print("START LOOP PROGRAM")

while True:

  voltage = f'votlage_{iteration}'
  percent = f'percent_{iteration}' 
    
    
  print('voltage: ' + str(gauge.read_voltage()) + 'mV')
  print('percentage: ' + str(round(gauge.read_percentage(), 2)) + '%')
  
  
  data = {
    "dataSource": "Cluster0",
    "database": "Dock",
    "collection": "Parameter",
    "filter": {
      "_id": { "$oid": "65ad6f1cec75483f9a3a15e7" }
    },
    "update":{
        "$set":{
            "voltage":{
                       "voltage": gauge.read_voltage()
            },
            "percent":{
                       "percent": round(gauge.read_percentage(), 2)
            },
            }
        },
    }  

  
  response = requests.post(url, headers=headers, data=json.dumps(data))
  try:
    response.raise_for_status()
    print(json.dumps(response.json()))
  except requests.exceptions.HTTPError as err:
    print(err)
    
  time.sleep(300)
  iteration += 1