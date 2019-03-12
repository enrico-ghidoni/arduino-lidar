# -*- coding: utf-8 -*-
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

#avrebbe senso rendere le operazioni che fa il TFMini interrompibili? Se si come fare?
#Da parte dell'arduino basta inserire un ascoltatore di serial events
#da parte python? Polling? Controllo se c'è qualche classe che ispeziona eventi seriali

# This Python file uses the following encoding: utf-8
import os, sys

import serial
import sys
import glob
import numpy
import time
import argparse
import open3d
import math

parser = argparse.ArgumentParser()
parser.add_argument('--serial-port', dest='serial_port', default=None, help='serial port the Arduino is connected to, if not specified the first detected port is used')
parser.add_argument('--baud-rate', dest='baud_rate', default=115200)
parser.add_argument('--update-interval', dest='update_interval', default=100, help='points to gather before updating point cloud rendering')



def run(serial_port=None, baud_rate=115200, update_interval=100):
    if serial_port is None:
        port = serial_ports()[0]
    else:
        port = serial_port
    ser =serial.Serial(port, baud_rate)

    # wait a few seconds for the Arduino
    time.sleep(5);
    
    #user configurable data
    max_x_angle = input('input max X angle:\t')
    max_y_angle = input('input max Y angle:\t')
    min_x_angle = input('input min X angle:\t')
    min_y_angle = input('input min Y angle:\t')
    spawn_x = input('input spawn on X axes:\t')
    spawn_y = input('input spawn on Y axes:\t')
    velocity = 0
    while float(velocity) < 10 :
    	velocity = input('input velocity of Servo in ms:\n ALLERT: Max velocity=10ms \n\t\t')
    
    # send the command to start the scan
    config_string = min_x_angle + ' ' + min_y_angle + ' ' + max_x_angle + ' ' + max_y_angle + ' ' + spawn_x + ' ' + spawn_y  + ' ' + velocity + ' ' 
    ser.write(config_string.encode('utf-8'))

    # read out 'connection established' message
    ser.readline()

    # initialize empty point cloud
    points = []
    pcd = open3d.PointCloud()
    pcd.points = open3d.Vector3dVector(points)

    # initialize counter for render update
    update_counter = 1

    # create open3d visualizer and bind it to the point cloud
    vis = open3d.Visualizer()
    vis.create_window()
    line = get_line(ser)
    while line != '0 181 181':
        # convert read line to [x, y, z]
        point = get_xyz(line,ser)
        pcd.points.append(point)
        #speed up performance
        pcd.colors.append([ 0, 0, 0 ])
        # increment counter
        update_counter += 1

        if update_counter > update_interval:

            # update point cloud visualizer
            vis.add_geometry(pcd)
            vis.update_geometry()
            vis.poll_events()
            vis.update_renderer()

            # reset counter
            update_counter = 1

        line = get_line(ser)
    pcd = color_point_cloud(pcd)
    open3d.draw_geometries([pcd])
    reply = input('Do you want to save? [yes/no]')
    if 'yes' in reply:
    	name = input('Type the name without extension:');
    	name = name+'.pcd'
    	open3d.write_point_cloud(name, pcd)


def color_point_cloud(pcd):
   max_count = len(pcd.points)
   distance_vector = []
   for i in range(max_count):
   	distance_vector.append(math.sqrt( math.pow( pcd.points[i][0] , 2 ) + math.pow( pcd.points[i][1] , 2 )))

   max_distance = max(distance_vector)
   min_distance = min(distance_vector)
   pcd.colors = open3d.Vector3dVector()
   for i in range(max_count):
   	pcd.colors.append(rewrite_point(pcd.points[i],min_distance,max_distance,distance_vector[i]))
   return pcd
   

def rewrite_point(point,min_distance,max_distance,actual_distance):
    color = float((actual_distance - min_distance) / (max_distance - min_distance))

    red = 4 * float(0.5 - color)

    if red < 0:
    	red = 0
    
    if red == 0:
    	blue = 4 * float(color - 0.5)
    else :
    	blue = 0

    if blue < 0:
    	blue = 0
    if blue > 1:
    	blue = 1

    if red < 2 and red != 0:
    	yellow = float(4 * (color))
    elif blue < 2 and blue != 0:
    	yellow = 4 * float(1 - color)
    else :
    	yellow = 0

    if yellow > 1:
    	yellow = 1
    if red > 1:
    	red = 1
    if yellow < 0:
    	yellow = 0
    
    return [red, yellow, blue]

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

def get_xyz(string,ser):
    if 'TF Mini' in string:
    	ser.readline()
    	ser.readline()
    	return [ 0, 0, 0 ]

    splitstr = string.split(' ')
    distance = splitstr[0]
    x_angle = splitstr[1]
    y_angle = splitstr[2]
    x_angle = float(x_angle) * numpy.pi / 180
    y_angle = float(y_angle) * numpy.pi / 180
    distance= float(distance)

    if distance > 1200:
    	distance = 0
 
    x = distance * numpy.sin(y_angle) * numpy.cos(x_angle)
    y = distance * numpy.sin(y_angle) * numpy.sin(x_angle)
    z = distance * numpy.cos(y_angle)
    
    return [x, y, z]

if __name__ == '__main__':
    args = parser.parse_args()
    run(args.serial_port, args.baud_rate)