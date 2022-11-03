# micropython-examples

Examples on how to use Drogue Cloud with micropython! There are two examples:

* [HTTP](src/http.py)
* [MQTT](src/mqtt.py)

Both of them read some sensor data and reports this data periodically. The device also accepts commands for turning on or off an on-board LED.

## Prerequisites 

### Hardware

For this example, we're using [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/), but it should work on any board that can run
micropython, provided you modify the hardware-specific sensor reading.

Have a look at [this reference](https://docs.micropython.org/en/latest/rp2/quickref.html) to learn more on how to interact with the peripherals.

## Software

### Micropython

Install [micropython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) on your device:

* Plug in your board, a USB storage device should appear
* Copy the .uf2 file for your board onto the USB storage device

Keep your device powered for a few seconds until micropython has been flashed to the device.

### PC tools

On your PC/Mac, you need the following tools installed:

* `drg` - Download the [latest release](https://github.com/drogue-iot/drg/releases) for your platform.
* `mpremote` - Run `pip3 install mpremote` (assumes you have Python installed)

#### Installing dependencies

To run the MQTT example, you need to install the MQTT client library as well:

``` yaml
mpremote mip install umqtt.simple
```

## Configuring Drogue Cloud

These instructions assume that you'll be using the [Drogue Cloud Sandbox](https://sandbox.drogue.cloud), but you can also [install Drogue Cloud](https://book.drogue.io/drogue-cloud/dev/admin-guide/index.html) yourself.

Log in to the sandbox (or another Drogue Cloud instance):

```
drg login https://api.sandbox.drogue.cloud
```

This will open a browser window where you can log in using your GitHub account.

Next, create the application and device with credentials (replace example-app with whatver application you wish to use):

```
drg create application example-app
drg create device --application example-app device1
drg set password device1 hey-rodney --application example-app
```
NOTE: Applications are global in Drogue Cloud, so if you're using the sandbox, make sure you choose a unique application name.

## Configuring the application

Use the [mqtt.py](src/mqtt.py) example if you want to use MQTT, or [http.py](http.py) if you want to use HTTP. In order to run the application, you need to modify a few variables:

* WIFI\_SSID - You local wifi access point SSID.
* WIFI\_PSK - You local wifi access point key.
* APPLICATION - The Drogue Cloud application you'll be using.
* DEVICE - The Drogue Cloud device you'll be authenticating as.
* PASSWORD - The device credentials you've entered previously.
* (Optional) `HOST` - If you're using a server different from the Drogue Cloud sandbox, change this.
* (Optional) `PORT` - If you're using a server different from the Drogue Cloud sandbox, change this.

## Running the application

Use the `mpremote` command to run the example:

``` yaml
mpremote run src/mqtt.py
```

Logs from your application will appear in the console, and the device should start to publish the temperature once it's connected.

## Streaming the data

You can consume the data from Drogue Cloud using MQTT or WebSockets, but for the sake of simplicity you can use the `drg` tool for that as well:

```
drg stream --application example-app
```

## Troubleshooting

...
