#!/usr/bin/env python
import os
import rospy
from mavros_msgs.srv import *
from mavros_msgs.msg import Waypoint, WaypointList 

def waypoint_push_client():
	waypoint_clear_client()
	wl = WaypointList()
	path_to_way = dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(path_to_way + '/way.txt', 'r') as wps:
		lines = wps.readlines()
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
			wp.x_lat = float(values[8])
			wp.y_long = float(values[9])
			wp.z_alt = float(values[10])
			wp.autocontinue = bool(values[11])
			wl.waypoints.append(wp)
	# wp.frame = 3
	# wp.command = 22  # takeoff
	# wp.is_current = True
	# wp.autocontinue = True
	# wp.param1 = data[0]['altitude']  # takeoff altitude
	# wp.param2 = 0
	# wp.param3 = 0
	# wp.param4 = 0
	# wp.x_lat = data[0]['latitude']
	# wp.y_long = data[0]['longitude']
	# wp.z_alt = data[0]['altitude']
	#wl.waypoints.append(wp)

	# for point in data:
	# 	wp = Waypoint()
	# 	wp.frame = 3
	# 	wp.command = 16  # simple point
	# 	wp.is_current = False
	# 	wp.autocontinue = True
	# 	wp.param1 = 0  # takeoff altitude
	# 	wp.param2 = 0
	# 	wp.param3 = 0
	# 	wp.param4 = 0

	# 	wp.x_lat = point['latitude']
	# 	wp.y_long = point['longitude']
	# 	wp.z_alt = point['altitude']
	# 	wl.waypoints.append(wp)
	try:
		service = rospy.ServiceProxy('mavros/mission/push', WaypointPush)
		if service.call(0, wl.waypoints).success:
			print 'write mission success'
		else:
			print 'write mission error'
	except rospy.ServiceException, e:
		print "Service call failed: %s" % e

def waypoint_clear_client():
		try:
			response = rospy.ServiceProxy(
				'mavros/mission/clear', WaypointClear)
			return response.call().success
		except rospy.ServiceException, e:
			print "Service call failed: %s" % e
			return False

if __name__ == '__main__':
	waypoint_push_client()