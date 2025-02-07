#  Author(s):  Anton Deguet
#  Created on: 2016-08

# (C) Copyright 2016-2023 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---

import rclpy

from std_msgs.msg import Bool, Float64, Empty, String
from geometry_msgs.msg import Quaternion

class teleop_psm(object):
    """Simple dVRK teleop PSM API wrapping around ROS messages
    """

    # initialize the teleop
    def __init__(self, teleop_name, ros_namespace = ''):
        # base class constructor in separate method so it can be called in derived classes
        self.__init_teleop_psm(teleop_name, ros_namespace)


    def __init_teleop_psm(self, teleop_name, ros_namespace = ''):
        """Constructor.  This initializes a few data members. It
        requires a teleop name, this will be used to find the ROS topics
        for the console being controlled."""
        # data members
        self.__teleop_name = teleop_name
        self.__ros_namespace = ros_namespace
        self.__full_ros_namespace = self.__ros_namespace + self.__teleop_name
        self.__scale = 0.0

        # publishers
        self.__set_scale_pub = rospy.Publisher(self.__full_ros_namespace
                                               + '/set_scale',
                                               Float64, latch = True, queue_size = 1)
        self.__set_desired_state_pub = rospy.Publisher(self.__full_ros_namespace
                                                       + '/set_desired_state',
                                                       String, latch = True, queue_size = 1)

        # subscribers
        rospy.Subscriber(self.__full_ros_namespace
                         + '/scale',
                         Float64, self.__scale_cb)

        # create node
        if not rospy.get_node_uri():
            rospy.init_node('teleop_api', anonymous = True, log_level = rospy.WARN)
        else:
            rospy.logdebug(rospy.get_caller_id() + ' -> ROS already initialized')


    def __scale_cb(self, data):
        """Callback for teleop scale.

        :param data: the latest scale requested for the teleop"""
        self.__scale = data.data

    def set_scale(self, scale):
        self.__set_scale_pub.publish(scale)

    def get_scale(self):
        return self.__scale

    def enable(self):
        self.__set_desired_state_pub.publish('ENABLED')

    def disable(self):
        self.__set_desired_state_pub.publish('DISABLED')
