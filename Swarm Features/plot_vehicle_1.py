#!/usr/bin/env python
import math
import os
import rospy
#import threading
import time
import utm
import numpy as np
import matplotlib.pyplot as plt
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import PoseStamped, TwistStamped, Twist, Vector3, Pose
from mavros_msgs.srv import *
from mavros_msgs.msg import Waypoint, WaypointList 

#lock = threading.Lock()
path_to_waypoint_file = '/home/paras/Desktop/SITL/ardupilot/way.txt'


class LineBuilder:
    def __init__(self, line,ax,color):
        self.line = line
        self.ax = ax
        self.color = color
        self.xs = []
        self.ys = []
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
        self.counter = 0
        self.shape_counter = 0
        self.shape = {}
        self.precision = 5

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        if self.counter == 0:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
        if np.abs(event.xdata-self.xs[0])<=self.precision and np.abs(event.ydata-self.ys[0])<=self.precision and self.counter != 0:
            self.xs.append(self.xs[0])
            self.ys.append(self.ys[0])
            self.ax.scatter(self.xs,self.ys,s=120,color=self.color)
            self.ax.scatter(self.xs[0],self.ys[0],s=80,color='blue')
            self.ax.plot(self.xs,self.ys,color=self.color)
            self.line.figure.canvas.draw()
            self.shape[self.shape_counter] = [self.xs,self.ys]
            self.shape_counter = self.shape_counter + 1
            self.xs = []
            self.ys = []
            self.counter = 0
        else:
            if self.counter != 0:
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)
            self.ax.scatter(self.xs,self.ys,s=120,color=self.color)
            self.ax.plot(self.xs,self.ys,color=self.color)
            self.line.figure.canvas.draw()
            self.counter = self.counter + 1

def create_shape_on_image(data,cmap='jet'):
    def change_shapes(shapes):
        new_shapes = {}
        for i in range(len(shapes)):
            l = len(shapes[i][1])
            new_shapes[i] = np.zeros((l,2),dtype='int')
            for j in range(l):
                new_shapes[i][j,0] = shapes[i][0][j]
                new_shapes[i][j,1] = shapes[i][1][j]
        return new_shapes
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click to include shape markers (10 pixel precision to close the shape)')
    line = ax.imshow(data) 
    ax.set_xlim(0,data[:,:,0].shape[1])
    ax.set_ylim(0,data[:,:,0].shape[0])
    linebuilder = LineBuilder(line,ax,'red')
    plt.gca().invert_yaxis()
    plt.grid(b=None, which='major', axis='both')
    plt.show()
    new_shapes = change_shapes(linebuilder.shape)
    return new_shapes

img = np.zeros((100,100,3),dtype='uint')
shapes = create_shape_on_image(img)[0]
global longitude
global latitude
longitude =0
latitude = 0
global new_longitude
global new_latitude
new_longitude = 0
new_latitude = 0
print(shapes)
print("Ended")


# x2_utm = x*x2/x1
# y2_utm = y*y2/y1

def convert_to_utm(x_lat, y_long):
    return utm.from_latlon(x_lat, y_long)


def convert_to_latlon(easting, northing, zone_number, zone_letter):
    return utm.to_latlon(easting, northing, zone_number, zone_letter)

# longitude --> y
# latitude --> x
def form(longitude, latitude):
    #easting, northing, zone_number, zone_letter = convert_to_utm(latitude, longitude)
    # x2_easting= (easting*shapes[1][0])/shapes[0][0]
    # y2_northing = (northing*shapes[1][1])/shapes[0][1]
    # print(easting, northing, x2_easting, y2_northing, "<--------This")
    # new_longitude, new_latitude = convert_to_latlon(x2_easting, y2_northing, zone_number, zone_letter)
    pi = math.pi
    r_earth = 6371000
    print(((shapes[0][0] - shapes[1][0])*0.000008983, "<-- generated latitude deviation"))
    new_latitude  = latitude  + (shapes[0][0] - shapes[1][0])*0.000008983
    new_longitude = longitude + ((shapes[0][1] - shapes[1][1])*0.000008983/ math.cos(latitude * pi/180))
    print(latitude, longitude, "----", new_latitude, new_longitude)
    takeoff_waypoint(2, new_latitude, new_longitude)

def takeoff_waypoint(curr_count, new_latitude, new_longitude):
    waypoint_clear_client(curr_count)
    wl = WaypointList()
    with open(path_to_waypoint_file) as waypoints:
            lines = waypoints.readlines()
            for line in lines[1:]:
                values = list(line.split('\t'))
                wp = Waypoint()
                wp.is_current = bool(values[1])
                wp.frame = int(values[2])
                wp.command = int(values[3])
                wp.param1 = float(values[4])
                wp.param2 = float(values[5])
                wp.param3 = float(values[6])
                wp.param4 = float(values[7])
              #  print(latitude, longitude, "xxxxxx", new_latitude, new_longitude)                
                wp.x_lat = float(new_latitude)
                wp.y_long = float(new_longitude)
                wp.z_alt = float(values[10])
                wp.autocontinue = bool(values[11])
                wl.waypoints.append(wp)
              #  print(wl.waypoints)
    
    try:
        rospy.wait_for_service('vehicle' + str(curr_count) + '/mavros/mission/push')
        service = rospy.ServiceProxy('vehicle' + str(curr_count) + '/mavros/mission/push', WaypointPush)
        if service.call(0, wl.waypoints).success:
            print 'write mission success'
        else:
            print 'write mission error'
    except:
        print "Service call failed: %s" % e

def waypoint_clear_client(curr_count):
        try:
            response = rospy.ServiceProxy('vehicle' + str(curr_count) + '/mavros/mission/clear', WaypointClear)
            return response.call().success
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
            return False

def setArm(option = '1'):
    vehicle = '/vehicle' + str(option)
    rospy.wait_for_service(vehicle + '/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy(vehicle + '/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(True)
    except rospy.ServiceException, e:
        print "Service arm call failed: %s"%e
        

def get_position(data):
    print("aaaaaaaaaaaaaaaaaaaa")
    longitude = data.longitude
    latitude = data.latitude
    print("escaping get_position")
    form(longitude, latitude)

def start(master):
    rospy.init_node("listerner", anonymous=True)

    print("/vehicle" + str(master) + "/mavros/global_position/global")
    rospy.Subscriber("/vehicle" + str(master) + "/mavros/global_position/global", NavSatFix, get_position) 
    print("aa111111111111111111111111111aaaaaaaaaaaaaaaaaa")
    rospy.spin()

print("CAlled 1")
start(1)
print("CAlled 2")
setArm(1)
print("CAlled 3")
setArm(2)