from paho.mqtt import client as mqtt
import random
import psutil
import time
import os
import logging as log



# Set up and connect to mqtt broker
broker = '192.168.0.13' #os.getenv('BROKER_IP')
port = int(os.getenv('BROKER_PORT', '1883'))
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = os.getenv('BROKER_UNAME')
password = os.getenv('BROKER_PASS')
name = os.getenv('SERVER_NAME', 'Server_' + str(client_id))

def connect():
    global client
    client = mqtt.Client(client_id)
    client.on_connect = log.info('Connected To Broker')
    client.connect(broker, port)
    return client

log.basicConfig(format='%(levelname)s: %(message)s',level=log.INFO)

while True:

    try:
        connect()
    except:
        log.error('Could Not Connect To Broker')


    cpu_use = str(psutil.cpu_percent(interval=1))
    t = psutil.sensors_temperatures()
    for x in ['cpu-thermal', 'cpu_thermal', 'coretemp', 'soc_thermal']:
        if x in t:
            cpu_temp = t[x][0].current
    mem_use = str(psutil.virtual_memory().percent)
    disk_use = str(psutil.disk_usage('/').percent)

    try:
        client.publish('homeassistant/sensor/{name}-cpu-use/state'.format(name = name.lower()), payload = cpu_use, qos = 0, retain = False)
        client.publish('homeassistant/sensor/{name}-cpu-temp/state'.format(name = name.lower()), payload = cpu_temp, qos = 0, retain = False)
        client.publish('homeassistant/sensor/{name}-mem-use/state'.format(name = name.lower()), payload = mem_use, qos = 0, retain = False)
        client.publish('homeassistant/sensor/{name}-disk-use/state'.format(name = name.lower()), payload = disk_use, qos = 0, retain = False)
        log.info('Info was sent')
    except:
        log.error('Info was unable to be sent')


    client.disconnect
    log.info('Disconnected From Broker')

    time.sleep(60)
