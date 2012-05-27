import roslib
roslib.load_manifest('automow_handler')

import rospy

from txosc import osc

from touchosc_bridge.abstracttabpage import AbstractTabpageHandler
from automow_node.msg import Automow_PCB
from automow_node.srv import Cutters


class CutterTabpageHandler(AbstractTabpageHandler):
    def __init__(self, touchosc_interface, handler_name, tabpage_names):
        super(CutterTabpageHandler, self).__init__(touchosc_interface,
                                                    handler_name,
                                                    tabpage_names)

        self.add_osc_callback('left', self.control_callback)
        self.add_osc_callback('right', self.control_callback)
        self.add_osc_callback('both', self.both_callback)

        self.cutter_control = rospy.ServiceProxy('/cutters', Cutters)

        self.cutter_1 = False
        self.cutter_2 = False

    def update_display(self):
        to_send = []
        to_send.append(osc.Message('both', self.cutter_1 or self.cutter_2))
        to_send.append(osc.Message('left', self.cutter_1))
        to_send.append(osc.Message('right', self.cutter_2))
        self.send(osc.Bundle(to_send))

    def control_callback(self, address_list, value_list, send_address):
        if len(address_list) <= 2:
            if address_list[1] == 'left':
                self.cutter_1 = bool(value_list[0])
            elif address_list[1] == 'right':
                self.cutter_2 = bool(value_list[0])

        resp = self.cutter_control(self.cutter_1, self.cutter_2)
        self.cutter_1 = resp.cutter_1
        self.cutter_2 = resp.cutter_2
        self.update_display()

    def both_callback(self, address_list, value_list, send_address):
        if len(address_list) <= 2:
            self.cutter_1 = bool(value_list[0])
            self.cutter_2 = bool(value_list[0])

            resp = self.cutter_control(self.cutter_1, self.cutter_2)
            self.cutter_1 = resp.cutter_1
            self.cutter_2 = resp.cutter_2
            self.update_display()
