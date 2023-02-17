import rospy
from dynamixel_workbench_msgs.srv import *
from naive_dynamixel_command import Command

if __name__ == "__main__":
    command = Command()
    command(value=0, id=1)

