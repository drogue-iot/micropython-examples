# micropython-examples

Examples on how to use Drogue Cloud with micropython! There are two examples:

* [HTTP](src/http.py)
* [MQTT](src/mqtt.py)

Both of them read some sensor data and reports this data periodically. The device also accepts commands for turning on or off an on-board LED.

The overall architecture looks like this:

``` yaml
+--------+                      +--------------+                    +-----+
| Device | <-- MQTT or HTTP --> | Drogue Cloud | <-- MQTT or WS --> | App |
+--------+                      +--------------+                    +-----+
```

As the "App", we'll be using the `drg` command line utility, but you can use any MQTT or WebSocket-cabable client.

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

Next, create the application and device with credentials (replace `example-app` and `device1` with the application name and device name you want to use):

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
* APPLICATION - The Drogue Cloud application name.
* DEVICE - The Drogue Cloud device name.
* PASSWORD - The device credentials.
* (Optional) `HOST` - If you're using a server different from the Drogue Cloud sandbox, change this.
* (Optional) `PORT` - If you're using a server different from the Drogue Cloud sandbox, change this.

## Running the application

Use the `mpremote` command to run the examples:

For MQTT:

``` yaml
mpremote run src/mqtt.py
```

For HTTP:

``` yaml
mpremote run src/http.py
```

Logs from your application will appear in the console, and the device should start to publish the temperature once it's connected.

To learn more about how to send data to Drogue Cloud, have a look at the [endpoint documentation](https://book.drogue.io/drogue-cloud/dev/user-guide/endpoint-http.html).

## Streaming the data

You can consume the data from Drogue Cloud using MQTT or WebSockets, but for the sake of simplicity you can use the `drg` tool for that as well:

```
drg stream --application example-app
```

For more information about connection applications to MQTT or WebSockets, have a look at [the documentation](https://book.drogue.io/drogue-cloud/dev/user-guide/integration.html).

## Sending commands

To send a command back to the device, you can use the `drg command` command:

``` yaml
drg command --app <app> -p '{"led":"on"}' <device> pico
```

Replace `<app>` and `<device>` with the Drogue Cloud application and device you're sending the command to. The `pico` keyword corresponds to the channel the device is sending telemetry to, using the default from the example is fine.

For more information about sending commands to device

## Troubleshooting

### I'm getting a Conflict when creating the application and/or device

Application names are global, which means that if someone else has already created this application on the Drogue Cloud instance, it is already taken and you need to choose a different name.

### I'm sending commands but the device does not print them

For the device to accept commands, it must be connected to the endpoint when the command is sent. Drogue Cloud does not queue the commands for the device, since in a typical IoT application you need to provide the
'response' to the command at the application layer anyway.
