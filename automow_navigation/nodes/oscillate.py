#!/usr/bin/env python

import roslib
roslib.load_manifest('automow_navigation')

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion
import actionlib
import numpy as np


EAST = Quaternion(0,0,0,1)
NORTH = Quaternion(0,0,np.sqrt(2)/2,np.sqrt(2)/2)
WEST = Quaternion(0,0,1,0)
SOUTH = Quaternion(0,0,np.sqrt(2)/2,-np.sqrt(2)/2)


def movebase_client(northing, easting, heading):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "odom"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = easting
    goal.target_pose.pose.position.y = northing
    goal.target_pose.pose.position.z = 0.0

    goal.target_pose.pose.orientation = heading

    client.send_goal(goal)
    rospy.loginfo("Goal Sent: (%s , %s)"%(easting, northing))

    client.wait_for_result()
    client.get_result()

if __name__ == '__main__':
    rospy.init_node('simple_nav_goal')
    base_north = 15.0
    base_east = 5.0
    inc = 0.3
    movebase_client(base_north, base_east, NORTH)

    try:
        for x in np.arange(0,20,inc*2):
            movebase_client(base_north,
                            base_east + x,
                            NORTH)
            movebase_client(base_north + 10.0,
                            base_east + x,
                            NORTH)
            movebase_client(base_north + 10.0,
                            base_east + x + inc,
                            SOUTH)
            movebase_client(base_north,
                            base_east + x + inc,
                            SOUTH)
    except rospy.ROSInterruptException, KeyboardInterrupt:
        print "Interrupted!"

