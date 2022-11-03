import network
import time
import machine
import ussl
import gc
from umqtt.simple import MQTTClient

# Customize these if you're not using the sandbox
HOST = "mqtt.sandbox.drogue.cloud"
PORT = 443

# TODO: You _must_ edit these settings
APPLICATION = "" # "example-app"
DEVICE = "" # "device1"
PASSWORD = "" # "hey-rodney"
WIFI_SSID = ""
WIFI_PSK = ""

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
TOPIC = b"pico"
ssl_params = {
    "server_hostname": HOST,
    "cert_reqs": ussl.CERT_NONE,
}


client = MQTTClient(CLIENT_ID,
                    server=HOST,
                    user=DEVICE + "@" + APPLICATION,
                    password=PASSWORD,
                    port=PORT,
                    ssl=True,
                    ssl_params=ssl_params)

print("Connecting to MQTT...")
client.connect()

print("Connected to MQTT, sending sensor data every 10 seconds")
while True:
    data = sensor.read_u16() * conversion_factor  
    # Conversion from datasheet
    temperature = 27 - (data - 0.706) / 0.001721
    payload = b"{\"temp\":" + str(temperature) + b"}"
    client.publish(TOPIC, payload)
    gc.collect()
    time.sleep(10)
