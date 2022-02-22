import os
import rospy
from dynamixel_workbench_msgs.srv import *
from dynamixel_sdk import *
from my_dynamixel_workbench_tutorial.srv import *

class Command():
    def __init__(self):
        self.srv = rospy.ServiceProxy('/set_position', SetPosition)
        # str = "Start %s"%rospy.get_time()
        # rospy.loginfo(str)

    def __call__(self, id=1, value=4000):
        self.request = SetPositionRequest()
        self.request.id = id
        self.request.position = value
        self.srv(self.request)

if __name__ == "__main__":
    command = Command()
    command()
