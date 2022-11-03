import network
import time
import machine
import ussl
import gc
import urequests
import ubinascii
import json

# Customize these if you're not using the sandbox
HOST = "http.sandbox.drogue.cloud"
PORT = 443
URL = "https://" + HOST + ":" + str(PORT) + "/v1/pico?ct=10"

# TODO: You _must_ edit these settings
APPLICATION = "" # "example-app"
DEVICE = "" # "device1"
PASSWORD = "" # "hey-rodney"
WIFI_SSID = ""
WIFI_PSK = ""


headers = {}
headers['Content-Type'] = 'application/json'
headers['Authorization'] = 'Basic ' + ubinascii.b2a_base64(DEVICE + "@" + APPLICATION + ":" + PASSWORD).decode('utf-8').strip()
# print("Headers", str(headers))

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PSK)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect...")
    time.sleep(1)

print(wlan.ifconfig())

# Read analog temperature
sensor = machine.ADC(4)
conversion_factor = 3.3 / 65535

# LED
led = machine.Pin("LED", machine.Pin.OUT)

while True:
    data = sensor.read_u16() * conversion_factor
    # Conversion from datasheet
    temperature = 27 - (data - 0.706) / 0.001721
    payload = json.dumps({"temp": temperature})

    print("Reporting sensor data: ", payload)
    response = urequests.post(URL, data=payload, headers=headers)
    if len(response.content) > 0:
        try:
            state = json.loads(response.content)
            print("Got command", str(state))
            if state['led'] == "on":
                led.on()
            else:
                led.off()
        except Exception as e:
            print("Error parsing command", e)

    response.close()
    # Ensures micropython doesn't run out of memory
    gc.collect()
    # time.sleep(5)
