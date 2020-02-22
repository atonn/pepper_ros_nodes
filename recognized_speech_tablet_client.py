#!/usr/bin/env python

import rospy
import socket
from std_msgs.msg import String

class TabletClient:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), 1620))

    def __del__(self):
        self.s.close()

    def recognized_speech_cb(self, data):
        msg = data.data + "<br>"
        print("Sending via socket:", msg)
        self.s.send(msg)
        rospy.loginfo(rospy.get_caller_id() + 'recognized speech: %s', msg)

    def run(self):
        rospy.init_node('tablet_string_display_client', anonymous=True)
        rospy.Subscriber('recognized_speech', String, self.recognized_speech_cb)
        rospy.spin()

if __name__ == '__main__':
    TabletClient().run()
