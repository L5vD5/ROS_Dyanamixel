import rospy
from dynamixel_workbench_msgs.srv import *
if __name__ == "__main__":
    proxy = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
    # str = "Start %s"%rospy.get_time()
    rospy.loginfo(str)
    a = DynamixelCommandRequest()
    a.addr_name = 'Goal_Position'
    a.id = 1
    a.value = 3000
    proxy(a)
    

