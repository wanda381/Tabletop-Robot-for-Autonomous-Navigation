#!/usr/bin/env python3

#This is the program that sets the autonomous navigation of the robot. Three different points on the map is given. The robot autonomously moves there.

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry

# Callbacks definition

def active_cb():
    rospy.loginfo("Goal pose being processed")

def feedback_cb(feedback):
    rospy.loginfo("Current location: "+str(feedback))

def done_cb(status, result):
    if status == 3:
        rospy.loginfo("Goal reached")
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")
    

rospy.init_node('goal_pose')

navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
navclient.wait_for_server()

odom_msg = rospy.wait_for_message('/odom', Odometry)


goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now()
#The z pose is set to the initial z pose as it is on a table

# Point A

goal.target_pose.pose.position.x = 0.418
goal.target_pose.pose.position.y = 0.377
goal.target_pose.pose.position.z = odom_msg.pose.pose.position.z
goal.target_pose.pose.orientation.x = -0.015
goal.target_pose.pose.orientation.y = 0.0010
goal.target_pose.pose.orientation.z = odom_msg.pose.pose.orientation.z
goal.target_pose.pose.orientation.w = 0.6488
navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
finished = navclient.wait_for_result()

# Point B
goal.target_pose.pose.position.x = 0.685
goal.target_pose.pose.position.y = -0.3143
goal.target_pose.pose.position.z = odom_msg.pose.pose.position.z
goal.target_pose.pose.orientation.x = -0.00032
goal.target_pose.pose.orientation.y = 0.0015
goal.target_pose.pose.orientation.z = odom_msg.pose.pose.orientation.z
goal.target_pose.pose.orientation.w = 0.9799
navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
finished = navclient.wait_for_result()

# Point C
goal.target_pose.pose.position.x = -0.972
goal.target_pose.pose.position.y = -0.173
goal.target_pose.pose.position.z = odom_msg.pose.pose.position.z
goal.target_pose.pose.orientation.x = 0.0095
goal.target_pose.pose.orientation.y = 0.00218
goal.target_pose.pose.orientation.z = odom_msg.pose.pose.orientation.z
goal.target_pose.pose.orientation.w = 0.7990
navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
finished = navclient.wait_for_result()

if not finished:
    rospy.logerr("Action server not available!")
else:
    rospy.loginfo ( navclient.get_result())
