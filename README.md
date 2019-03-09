# Arduino - LIDAR

`arduino-lidar` is a tool to gather LIDAR readings from an Arduino board in order to build and visualize a point cloud in real time.

## Requirements

 - Python 3.6

## Installation

It is recommended to use a Python virtual environment (checkout `virtualenv`) for running this tool.

## Usage

A trivial interaction protocol is used for communication between the python script and the Arduino board. Every message is sent through the serial port the board is connected to.

1. the Arduino board waits for a `python` message
2. the Arduino starts sending LIDAR data in spherical coordinates with the format `distance x-angle y-angle` (whitespace separated values)
3. once all data has been sent, the Arduino board sends an **end-of-data** signal with the following message `0 181 181`

```
usage: arduinolidar.py [-h] [--serial-port SERIAL_PORT]
                       [--baud-rate BAUD_RATE]
                       [--update-interval UPDATE_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  --serial-port SERIAL_PORT
                        serial port the Arduino is connected to, if not
                        specified the first detected port is used
  --baud-rate BAUD_RATE
  --update-interval UPDATE_INTERVAL
                        points to gather before updating point cloud rendering
```