#!/usr/bin/env python

import roslib
roslib.load_manifest('automow_navigation')

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

def movebase_client():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    rospy.loginfo('got server')
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "base_link"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 10.0
    goal.target_pose.pose.position.y = 0.0
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0
    client.send_goal(goal)
    rospy.loginfo('sent goal')
    rospy.loginfo(goal)
    client.wait_for_result()
    return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('simple_nav_goal')
        result = movebase_client()
        print result
    except rospy.ROSInterruptException:
        print "interrupted"
