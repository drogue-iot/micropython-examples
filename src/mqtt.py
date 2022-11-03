import network
import time
import machine
import ussl
import gc
import json
import time
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

# LED
led = machine.Pin("LED", machine.Pin.OUT)

# MQTT and TLS settings
CLIENT_ID = "myclientid"
TOPIC = b"pico"
ssl_params = {
    "server_hostname": HOST,
    "cert_reqs": ussl.CERT_NONE,
}

# Callback
def command(topic, msg):
    try:
        print("Got command", str(msg))
        state = json.loads(msg)
        if state['led'] == "on":
            led.on()
        else:
            led.off()
    except Exception as e:
        print("Error parsing command", e)

client = MQTTClient(CLIENT_ID,
                    server=HOST,
                    user=DEVICE + "@" + APPLICATION,
                    password=PASSWORD,
                    port=PORT,
                    ssl=True,
                    ssl_params=ssl_params)

client.set_callback(command)
print("Connecting to MQTT...")
client.connect()
client.subscribe("command/inbox//#")

print("Connected to MQTT, sending sensor data every 10 seconds")
while True:
    # Ensures micropython doesn't run out of memory
    gc.collect()

    data = sensor.read_u16() * conversion_factor  
    # Conversion from datasheet
    temperature = 27 - (data - 0.706) / 0.001721
    payload = json.dumps({"temp": temperature})

    print("Publishing payload " + str(payload))
    client.publish(TOPIC, payload)
    end = time.time() + 10
    while time.time() < end:
        client.check_msg()
        time.sleep_ms(10)
