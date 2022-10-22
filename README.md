# micropython-example

Examples on how to use Drogue Cloud with micropython! There are two examples:

* [HTTP](src/http.py)
* [MQTT](src/mqtt.py)

Both of them read some sensor data and reports this data periodically. The device also accepts
commands for turning on or off an on-board LED.

## Prerequisites 

### Hardware

For this example, we're using [Raspberry Pi Pico W](), but it should work on any board that can run
micropython, provided you modify the hardware-specific sensor reading.

## Software

Install [micropython]() on your device. Circuitpython should also work, but may require some
changes.

On your PC/Mac, you need the following tools installed:

* `drg` - Download the [latest release]() for your platform.

These instructions assume that you'll be using the [Drogue Cloud Sandbox](https://sandbox.drogue.cloud), but you can also [install Drogue Cloud]() yourself.

## Configuring Drogue Cloud

Log in to the sandbox (or another Drogue Cloud instance):

```
drg login https://api.sandbox.drogue.cloud
```

This will open a browser window where you can log in using your GitHub account.

Next, create the application and device with credentials:

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

Connect your device, and copy your application to the device. You can view the debug output
connecting the serial device that appears when you've connected your device.

## Streaming the data

You can consume the data using MQTT or WebSockets, but for the sake of simplicity you can use the `drg` tool for that as well:

```
drg stream --application example-app
```

## Troubleshooting

...
