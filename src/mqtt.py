import network
import time
import machine
from umqtt.simple import MQTTClient

# TODO: Customize settings
HOST = "mqtt.sandbox.drogue.cloud"
APPLICATION = "example-app"
DEVICE = "device1"
PASSWORD = "hey-rodney"
WIFI_SSID = "..."
WIFI_PSK = "..."


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(WIFI_SSID, WIFI_PSK)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())

# Read analog temperature
sensor = machine.ADC(4)
conversion_factor = 3.3 / 65535                

# MQTT and TLS settings
CLIENT_ID = "myclientid"
TOPIC = b"foo"
ssl_params = {"server_hostname": HOST}  

client = MQTTClient(CLIENT_ID,
                    server=HOST,
                    user="device1@example-app",
                    password="hey-rodney",
                    port=443,
                    ssl=True,
                    ssl_params=ssl_params)
client.connect()

while True:
    data = sensor.read_u16() * conversion_factor  
    # Conversion from datasheet
    temperature = 27 - (data - 0.706) / 0.001721
    client.publish(TOPIC, json.dumps({"temp": temperature}))
    time.sleep(10)
