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

vehicle1_pos = [0,0]
vehicle2_pos = [0,0]

def getGPS_vehicle1(measurement):
    global vehicle1_pos

    vehicle_lat=measurement.latitude
    vehicle_lon=measurement.longitude
    vehicle1_pos = [vehicle_lat,vehicle_lon]

    #print "UAV1 : ", vehicle1_pos


def getGPS_vehicle2(measurement):
    global vehicle2_pos

    vehicle_lat=measurement.latitude
    vehicle_lon=measurement.longitude
    vehicle2_pos = [vehicle_lat,vehicle_lon]

    #V2 : ", vehicle2_pos

def ros_connect():
	global wp_publisher1,wp_publisher2, rate

	rospy.init_node('task_allocator', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	
	#subscribers
	rospy.Subscriber("/vehicle1/mavros/global_position/global", NavSatFix, getGPS_vehicle1)
	rospy.Subscriber("/vehicle2/mavros/global_position/global", NavSatFix, getGPS_vehicle2)
	
	#publishers
	wp_publisher1 = rospy.Publisher('/vehicle1/mavros/setpoint_raw/global', GlobalPositionTarget, queue_size=1000)
	wp_publisher2 = rospy.Publisher('/vehicle2/mavros/setpoint_raw/global', GlobalPositionTarget, queue_size=1000)

	# Let the subscribers starte working
	time.sleep(2)
	print "Ros Services Connected\n"

def task_allocation():
	global wp_publisher1, wp_publisher2, vehicle1_pos, vehicle2_pos, rate

	task_list = task_manager.get_tasks()	
	tasks_finished = False
	vehicle1_in_progress = False
	vehicle2_in_progress = False
	vehicle1_task_complete = False
	vehicle2_task_complete = False

	print "Node Begins"
	while (not vehicle1_task_complete) or (not vehicle2_task_complete) or (not tasks_finished) :

		if not vehicle1_in_progress and not tasks_finished:
			print "Task Allocation Begin\n"
			vehicle1_task = task_manager.get_optimal_task(task_list,vehicle1_pos)

			target = GlobalPositionTarget()

			target.coordinate_frame = 6
			target.type_mask = 4088
			target.latitude = vehicle1_task[0]
			target.longitude = vehicle1_task[1]
			target.altitude = 5.0
			target.header.frame_id = ''

			wp_publisher1.publish(target)
			vehicle1_in_progress = True
			vehicle1_task_complete = False

			task_list.remove(vehicle1_task)
			if (len(task_list) == 0):
				tasks_finished = True

			print "Task Alloted to Vehicle 1\n"

		if not vehicle2_in_progress and not tasks_finished:
			print "Task Allocation Begin\n"
			vehicle2_task = task_manager.get_optimal_task(task_list,vehicle2_pos)

			target = GlobalPositionTarget()

			target.coordinate_frame = 6
			target.type_mask = 4088
			target.latitude = vehicle2_task[0]
			target.longitude = vehicle2_task[1]
			target.altitude = 5.0
			target.header.frame_id = ''

			wp_publisher2.publish(target)
			vehicle2_in_progress = True
			vehicle2_task_complete = False

			task_list.remove(vehicle2_task)
			if (len(task_list) == 0):
				tasks_finished = True

			print "Task Alloted to Vehicle 2\n"

		if vehicle1_in_progress and task_manager.task_achieved(vehicle1_task,vehicle1_pos):
			print "Vehicle1 achieved task"
			vehicle1_in_progress = False
			vehicle1_task_complete = True

		if vehicle2_in_progress and task_manager.task_achieved(vehicle2_task,vehicle2_pos):
			print "Vehicle2 achieved task"			
			vehicle2_in_progress = False
			vehicle2_task_complete = True

		#print "Vehicle 1 task comlpete", vehicle1_task_complete
		#print "Vehicle 2 task comlpete", vehicle2_task_complete
		#print "task comlpete", tasks_finished


		rate.sleep()

	print "All tasks finished" 

if __name__ == '__main__' :

	ros_connect()

	task_allocation()


