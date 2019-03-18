#!/usr/bin/env python
from geometry_msgs.msg import Pose,Point,Vector3Stamped,PoseStamped
import task_manager
from nav_msgs.msg import Odometry
from mavros_msgs.msg import OverrideRCIn, VFR_HUD, WaypointList, RCOut, GlobalPositionTarget
import rospy
from sensor_msgs.msg import NavSatFix
import time
#home = [,]
#curr_x = 0
#curr_y = 0

vehicle_pos = [0,0]

#######   HAVERSINE START
'''
def getXY_waypt(x,y,home_x,home_y,rel_x,rel_y):
    if x==home_x:
        rel_x = 0 # relative position of vehicle w.r.t home
        rel_y = 0
    else:
        rel_x = x - origin_x
        rel_y = y - origin_y
    return rel_x,rel_y
'''

##########	Make home as (0,0) and localize the vehcile position respect to that
def getGPS(measurement):
    global vehicle_pos

    vehicle_lat=measurement.latitude
    vehicle_lon=measurement.longitude
    vehicle_pos = [vehicle_lat,vehicle_lon]

    print "UAV Pose", vehicle_lat, ", ", vehicle_lon
    #curr_x,curr_y = getXY_waypt(x,y,home[0],home[1],0,0)

def ros_connect():
	global wp_publisher, rate

	rospy.init_node('task_allocator', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	
	#subscribers
	rospy.Subscriber("/vehicle1/mavros/global_position/global", NavSatFix, getGPS)
	
	#publishers
	wp_publisher = rospy.Publisher('/vehicle1/mavros/setpoint_raw/global', GlobalPositionTarget, queue_size=1000)

	# Let the subscribers starte working
	time.sleep(2)
	print "Ros Services Connected\n"

def task_allocation():
	global wp_publisher, vehicle_pos, rate

	task_list = task_manager.get_tasks()	
	mission_complete = False
	task_in_progress = False
	print "Node Begins"
	while not mission_complete:
		if not task_in_progress:
			print "Task Allocation Begin\n"
			task = task_manager.get_optimal_task(task_list,vehicle_pos)

			target = GlobalPositionTarget()

			target.coordinate_frame = 6
			target.type_mask = 4088
			target.latitude = task[0]
			target.longitude = task[1]
			target.altitude = 5.0
			target.header.frame_id = '/base_link'

			wp_publisher.publish(target)
			task_in_progress = True
			print "Task Alloted\n"

		if task_in_progress and task_manager.task_achieved(task,vehicle_pos):
			print "Removing Task from List"
			task_in_progress = False
			task_list.remove(task)
			if (len(task_list) == 0):
				mission_complete = True

		rate.sleep()

if __name__ == '__main__' :

	ros_connect()

	task_allocation()


