#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, TwistStamped, Twist, Vector3, Pose
from mavros_msgs.msg import PositionTarget, AttitudeTarget, State
from mavros_msgs.srv import SetMode, SetModeRequest
from std_msgs.msg import Float64

def vel_callback(data):
	vel2_pub = rospy.Publisher('/vehicle2/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
	vel3_pub = rospy.Publisher('/vehicle3/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
	vel4_pub = rospy.Publisher('/vehicle4/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
	pub = TwistStamped()
	print(data.twist.linear.x, data.twist.linear.z)
	pub.twist.linear.x=data.twist.linear.x
	pub.twist.linear.z=data.twist.linear.z
	pub.twist.linear.y=data.twist.linear.y
	pub.twist.angular.x=data.twist.angular.x
	pub.twist.angular.y=data.twist.angular.y
	pub.twist.angular.z=data.twist.angular.z
	vel2_pub.publish(pub)
	vel3_pub.publish(pub)
	vel4_pub.publish(data)

def moveSame():
	rospy.Subscriber("/vehicle1/mavros/local_position/velocity_local", TwistStamped , vel_callback)
	
	
if __name__ == '__main__':
	rospy.init_node('circle', anonymous=True)
	rospy.Rate(10)
	moveSame()
	rospy.spin()