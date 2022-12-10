from paho.mqtt import client as mqtt
import random
import psutil
from configparser import ConfigParser
import time


# Read Config
config = ConfigParser()
config.read("config.ini")
broker_info = config['BROKER']
sys_info = config['SYS']

# Set up and connect to mqtt broker
broker = broker_info["ip"]
port = int(broker_info["port"])
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = broker_info["username"]
password = broker_info["password"]
name = sys_info["name"]

def connect():
    global client
    client = mqtt.Client(client_id)
    client.on_connect = print('Connected!')
    client.connect(broker, port)
    return client

while True:

    try:
        connect()
    except:
        print('Something Went Wrong')


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
        print('Info was sent')
    except:
        print('Info was unable to be sent')


    client.disconnect
    print('Disconnected')

    time.sleep(60)
