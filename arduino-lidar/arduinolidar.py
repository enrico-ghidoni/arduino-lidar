# ---------------------------License Notice------------------------------------------
# Copyright (C) 2019 Enrico Ghidoni (enrico.ghidoni2@studio.unibo.it)
# Copyright (C) 2019 Luca Ottavio Serafini (lucaottavio.serafini@studio.unibo.it)
#
# This file is part of arduino-lidar.
#
# arduino-lidar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# arduino-lidar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with arduino-lidar.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------License Notice------------------------------------------


import serial
import sys
import glob
import numpy
import time
import argparse
import open3d

parser = argparse.ArgumentParser()
parser.add_argument('--serial-port', dest='serial_port', default=None, help='serial port the Arduino is connected to, if not specified the first detected port is used')
parser.add_argument('--baud-rate', dest='baud_rate', default=115200)

def run(serial_port=None, baud_rate=115200):
    if serial_port is None:
        port = serial_ports()[0]
    else:
        port = serial_port

    ser =serial.Serial(port, baud_rate)
    # wait a few seconds for the Arduino
    time.sleep(5);

    # send the command to start the scan
    ser.write(b'python')
    # read out 'connection established' message
    ser.readline()

    # initialize empty point cloud
    points = []
    pcd = open3d.PointCloud()
    pcd.points = open3d.Vector3dVector(points)

    # create open3d visualizer and bind it to the point cloud
    vis = open3d.Visualizer()
    vis.create_window()

    line = get_line(ser)
    while line != '0 181 181':
        # convert read line to [x, y, z]
        point = get_xyz(line)
        print(point)
        pcd.points.append(point)

        # update point cloud visualizer
        vis.add_geometry(pcd)
        vis.update_geometry()
        vis.poll_events()
        vis.update_renderer()

        line = get_line(ser)
    
    input('Press \'enter\' to continue')
    vis.destroy_window()

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def get_line(ser):
    return ser.readline().decode('utf-8').replace('\r\n', '')

def get_xyz(string):
    print(string)
    splitstr = string.split(' ')
    distance = splitstr[0]
    x_angle = splitstr[1]
    y_angle = splitstr[2]
    x_angle = float(x_angle) * numpy.pi / 180
    y_angle = float(y_angle) * numpy.pi / 180
    distance= float(distance)
    print(x_angle, y_angle, distance)
    x = distance * numpy.sin(y_angle) * numpy.cos(x_angle)
    y = distance * numpy.sin(y_angle) * numpy.sin(x_angle)
    z = distance * numpy.cos(y_angle)

    return [x, y, z]

if __name__ == '__main__':
    args = parser.parse_args()
    run(args.serial_port, args.baud_rate)
