#!/usr/bin/env python

from math import sin, cos, sqrt, atan2, radians
import linecache

def get_tasks():

	task_list = []
	for i in range(1,13):
		data = linecache.getline('/home/mandeep/catkin_ws/src/swarm_pkg/src/swarm_sitl2.txt',i)
		data_list = data.split(',')
		data_list[0] = float(data_list[0])
		data_list[1] = float(data_list[1].rstrip())
		print data_list
		task_list.append(data_list)

	return task_list

def get_distance(task, vehicle_pos):

	#cost = math.sqrt((task[0] - vehicle_pose[0])**2 + (task[1] - vehicle_pose[1])**2) # euler_distance

	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(task[0])
	lon1 = radians(task[1])
	lat2 = radians(vehicle_pos[0])
	lon2 = radians(vehicle_pos[1])

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	#print("Result:", distance)
	#print("Should be:", 278.546, "km")

	return distance

def get_optimal_task(task_list,vehicle_pos):

	print "Number of tasks remaining :", len(task_list)
	for i in range(0,len(task_list)):
		task = task_list[i]
		cost = get_distance(task,vehicle_pos)
		print "Task Cost: ", cost
		if i == 0:
			min_cost = cost
			optimal_task = task
		else:
			if(cost < min_cost):
				min_cost = cost
				optimal_task = task

	print "Returning Optimal Task :", optimal_task
	return optimal_task

def task_achieved(task,vehicle_pos):

	dist = get_distance(task,vehicle_pos)*1000 # to convert in meters
	#print "Task Distance :", dist
	if dist > 5: 
		#print "Task Not Achieved"
		return False
	else:
		#print "Task Achieved"
		return True





