#!/usr/bin/env python
import math
import os
import rospy
import time
import utm
import numpy as np
import matplotlib.pyplot as plt
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import PoseStamped, TwistStamped, Twist, Vector3, Pose
from mavros_msgs.srv import *
from mavros_msgs.msg import Waypoint, WaypointList, GlobalPositionTarget

path_to_waypoint_file = '/home/vishalsamal/ardupilot/way.txt'

shapes= [[10, 10], [20, 20]]

global longitude
global latitude
longitude =0
latitude = 0
global new_longitude
global new_latitude
new_longitude = 0
new_latitude = 0

def form(longitude, latitude):
    pi = math.pi
    r_earth = 6371000
    print(((shapes[0][0] - shapes[1][0])*0.000008983*1000, "<-- generated latitude deviation"))
    new_latitude  = latitude  + (shapes[0][0] - shapes[1][0])*0.000008983
    new_longitude = longitude + ((shapes[0][1] - shapes[1][1])*0.000008983/ math.cos(latitude * pi/180))
    print(latitude, longitude, "----", new_latitude, new_longitude)
    next_waypoint(2, new_latitude, new_longitude)

def next_waypoint(vehicle_number, latitude, longitude):
    publisher = rospy.Publisher('/vehicle' + str(vehicle_number) + '/mavros/setpoint_raw/global', GlobalPositionTarget, queue_size=10)
    pub = GlobalPositionTarget()
    pub.longitude = longitude
    pub.latitude = latitude
    publisher.publish(pub)


def get_position(data):
    longitude = data.longitude
    latitude = data.latitude
    form(longitude, latitude)


def start(master):
    rospy.init_node("listerner", anonymous=True)
    rospy.Subscriber("/vehicle" + str(master) + "/mavros/global_position/global", NavSatFix, get_position) 
    rospy.spin()

start(1)