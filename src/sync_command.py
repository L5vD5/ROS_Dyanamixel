import os
import rospy
from dynamixel_workbench_msgs.srv import *
from dynamixel_sdk import *
from my_dynamixel_workbench_tutorial.srv import *

ADDR_GOAL_POSITION          = 116
LEN_GOAL_POSITION           = 4         # Data Byte Length
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600

class Command():
    def __init__(self,DEVICENAME='/dev/ttyUSB0', PROTOCOL_VERSION=2.0):
        # self.srv = rospy.ServiceProxy('/bulkWrite', BulkSetItem)
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        try:
            self.portHandler.openPort()
            print("Succeeded to open the port")
        except Exception as e:
            print(e)
            print("Failed to open the port")
            print("Press any key to terminate...")
            quit()

        # Set port baudrate
        try:
            self.portHandler.setBaudRate(BAUDRATE)
            print("Succeeded to change the baudrate")
        except Exception as e:
            print(e)
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            quit()

        # str = "Start %s"%rospy.get_time()
        # rospy.loginfo(str)

    def __call__(self, id=1, value=0):
        self.request = GroupSyncWrite(self.portHandler, self.packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

        # Allocate goal position value into byte array
        param_goal_position = [DXL_LOBYTE(DXL_LOWORD(0)), DXL_HIBYTE(DXL_LOWORD(0)), DXL_LOBYTE(DXL_HIWORD(0)), DXL_HIBYTE(DXL_HIWORD(0))]

        # Add Dynamixel#1 goal position value to the Bulkwrite parameter storage
        dxl_addparam_result = self.request.addParam(1, param_goal_position)
        dxl_addparam_result = self.request.addParam(2, param_goal_position)
        print(dxl_addparam_result)

        dxl_comm_result = self.request.txPacket()
        print(dxl_comm_result)
        # ret = self.srv(self.request)
        # print(ret.flag)

if __name__ == "__main__":
    command = Command()
    command()
