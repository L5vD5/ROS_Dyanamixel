import rospy
from dynamixel_workbench_msgs.srv import *

class Command():
    def __init__(self):
        self.srv = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        # str = "Start %s"%rospy.get_time()
        # rospy.loginfo(str)

    def __call__(self, id=0, addr_name="Goal_Position", value=1000):
        self.request = DynamixelCommandRequest()
        self.request.addr_name = addr_name
        self.request.id = id
        self.request.value = value
        self.srv(self.request)

if __name__ == "__main__":
    command = Command()
    command()
