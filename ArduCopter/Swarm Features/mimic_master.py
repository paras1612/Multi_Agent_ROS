#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, TwistStamped, Twist, Vector3, Pose
from mavros_msgs.msg import PositionTarget, AttitudeTarget, State
from mavros_msgs.srv import SetMode, SetModeRequest
from std_msgs.msg import Float64
import argparse

def vel_callback(data, args):
	drone_count = args[0]
	curr_leader = args[1]
	for i in range(1, drone_count+1):
		if i != curr_leader:
			rospy.Publisher('/vehicle'+str(i)+'/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10).publish(data)

def orient_callback(data, args):
	drone_count = args[0]
	curr_leader = args[1]
	for i in range(1, drone_count+1):
		if i != curr_leader:
			rospy.Publisher('/vehicle'+str(i)+'/mavros/global_position/compass_hdg', Float64, queue_size=10).publish(data)

def moveSame(drone_count, curr_leader=1):
	rospy.Subscriber("/vehicle"+str(curr_leader)+"/mavros/local_position/velocity_local", TwistStamped , vel_callback, (drone_count, curr_leader))
	rospy.Subscriber("/vehicle"+str(curr_leader)+"/mavros/global_position/compass_hdg", Float64, orient_callback, (drone_count, curr_leader))
	
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--n', dest='drone_count', type=int, default=1)
	parser.add_argument('--leader', dest='curr_leader', type=int, default=1)
	args = parser.parse_args()
	rospy.init_node('circle', anonymous=True)
	rospy.Rate(10)
	print()
	moveSame(args.drone_count, args.curr_leader)
	rospy.spin()
