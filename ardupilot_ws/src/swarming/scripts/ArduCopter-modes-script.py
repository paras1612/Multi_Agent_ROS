#!/usr/bin/env python
import rospy
import message_filters
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *

#global variable
latitude =0.0
longitude=0.0

global vehicle
def setGuidedMode(option = "1"):
    vehicle = '/vehicle' + option
    rospy.wait_for_service(vehicle +'/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy(vehicle + '/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='GUIDED') #return true or false
    except rospy.ServiceException, e:
        print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e
        
def setStabilizeMode(option = '1'):
    vehicle = '/vehicle' + option
    rospy.wait_for_service(vehicle +'/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy(vehicle + '/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
    except rospy.ServiceException, e:
        print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e

def setLandMode(option = '1'):
    vehicle = '/vehicle' + option
    rospy.wait_for_service(vehicle + '/mavros/cmd/land')
    try:
        landService = rospy.ServiceProxy(vehicle + '/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    except rospy.ServiceException, e:
        print "service land call failed: %s. The vehicle cannot land "%e
          
def setArm(option = '1'):
    vehicle = '/vehicle' + option
    rospy.wait_for_service(vehicle + '/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy(vehicle + '/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(True)
    except rospy.ServiceException, e:
        print "Service arm call failed: %s"%e
        
def setDisarm(option = '1'):
    vehicle = '/vehicle' + option
    rospy.wait_for_service(vehicle + '/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy(vehicle + '/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(False)
    except rospy.ServiceException, e:
        print "Service arm call failed: %s"%e


def setTakeoffMode(option = '1'):
    vehicle = '/vehicle' + option
    rospy.wait_for_service(vehicle + '/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy(vehicle + '/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
        takeoffService(altitude = 2, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    except rospy.ServiceException, e:
        print "Service takeoff call failed: %s"%e
    
    

def globalPositionCallback(globalPositionCallback):
    global latitude
    global longitude
    latitude = globalPositionCallback.latitude
    longitude = globalPositionCallback.longitude
    #print ("longitude: %.7f" %longitude)
    #print ("latitude: %.7f" %latitude)

def menu():
    print "Press"
    print "1: to set mode to GUIDED"
    print "2: to set mode to STABILIZE"
    print "3: to set mode to ARM the drone"
    print "4: to set mode to DISARM the drone"
    print "5: to set mode to TAKEOFF"
    print "6: to set mode to LAND"
    print "7: print GPS coordinates"
    
def myLoop():
    x='1'
    vehicle = '1'
    while ((not rospy.is_shutdown())and (x in ['1','2','3','4','5','6','7'])):
        menu()
        vehicle = raw_input("Enter vehicle number: ")
        x = raw_input("Enter your input: ");
        if (x=='1'):
            setGuidedMode(vehicle)
        elif(x=='2'):
            setStabilizeMode(vehicle)
        elif(x=='3'):
            setArm(vehicle)
        elif(x=='4'):
            setDisarm(vehicle)
        elif(x=='5'):
            setTakeoffMode(vehicle)
        elif(x=='6'):
            setLandMode(vehicle)
        elif(x=='7'):
            global latitude
            global longitude
            print ("longitude: %.7f" %longitude)
            print ("latitude: %.7f" %latitude)
        else: 
            print "Exit"
        
        
    

if __name__ == '__main__':
    rospy.init_node('dronemap_node', anonymous=True)
    rospy.Subscriber("/vehicle1/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)
    rospy.Subscriber("/vehicle2/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)
    # spin() simply keeps python from exiting until this node is stopped
    
    #listener()
    myLoop()
    #rospy.spin()

