#!/usr/bin/env python

import roslib
roslib.load_manifest('automow_navigation')

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion
import actionlib
import numpy as np

from optparse import OptionParser

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
    rospy.init_node('send_goal')

    parser = OptionParser(usage = "usage: %prog East North Heading")
    (options, args) = parser.parse_args()

    if args[2] == 'N':
        heading = NORTH
    elif args[2] == 'E':
        heading = EAST
    elif args[2] == 'S':
        heading = SOUTH
    elif args[2] == 'W':
        heading = WEST
    else:
        print "Invalid heading!"
        sys.exit(-1)

    try:
        movebase_client(float(args[1]),
                        float(args[0]),
                        heading)
    except rospy.ROSInterruptException, KeyboardInterrupt:
        print "Interrupted!"

