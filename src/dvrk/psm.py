#  Author(s):  Anton Deguet
#  Created on: 2016-05

#   (C) Copyright 2016-2023 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---

from dvrk.arm import *

import numpy

class psm(arm):
    """Simple robot API wrapping around ROS messages
    """

    # class to contain jaw methods
    class __Jaw:
        def __init__(self, ros_node, ros_sub_namespace, expected_interval, operating_state_instance):
            self.__crtk_utils = crtk.utils(self, ros_node, expected_interval, operating_state_instance)
            self.__crtk_utils.add_measured_js(ros_sub_namespace)
            self.__crtk_utils.add_setpoint_js(ros_sub_namespace)
            self.__crtk_utils.add_servo_jp(ros_sub_namespace)
            self.__crtk_utils.add_move_jp(ros_sub_namespace)
            self.__crtk_utils.add_servo_jf(ros_sub_namespace)

        def close(self):
            "Close the tool jaw"
            return self.move_jp(numpy.array([math.radians(-20.0)]))

        def open(self, angle = math.radians(60.0)):
            "Close the tool jaw"
            return self.move_jp(numpy.array([angle]))


    # initialize the robot
    def __init__(self, arm_name, ros_node,
                 expected_interval = 0.01):
        # first call base class constructor
        self._arm__init_arm(arm_name, ros_node, expected_interval)
        self.jaw = self.__Jaw(self._arm__ros_node, 'jaw/', expected_interval,
                              operating_state_instance = self)

        # publishers
        self.__set_tool_present_publisher = self._arm__ros_node.create_publisher(std_msgs.msg.Bool,
                                                                                 'jaw/set_tool_present',
                                                                                 10) # latch = True
        self._arm__pub_list.extend([self.__set_tool_present_publisher])

    def insert_jp(self, depth):
        "insert the tool, by moving it to an absolute depth"
        goal = numpy.copy(self.setpoint_jp())
        goal[2] = depth
        return self.move_jp(goal)

    def set_tool_present(self, tool_present):
        "Set tool inserted.  To be used only for custom tools that can't be detected automatically"
        tp = std_msgs.msg.Bool()
        tp.data = tool_present
        self.__set_tool_present_publisher.publish(tp)
