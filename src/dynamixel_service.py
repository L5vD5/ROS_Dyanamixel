import os
import rospy
from dynamixel_workbench_msgs.srv import *
from dynamixel_sdk import *
from my_dynamixel_workbench_tutorial.srv import *
# from my_dynamixel_workbench_tutorial.msg import *

ADDR_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_GOAL_POSITION      = 116
ADDR_PRESENT_POSITION   = 132

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = 1                 # Dynamixel ID : 1
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class Service():
    def __init__(self, DEVICENAME='/dev/ttyUSB0', PROTOCOL_VERSION=2.0):
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

    def get_present_pos(self, req):
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, req.id, ADDR_PRESENT_POSITION)
        print("Present Position of ID %s = %s" % (req.id, dxl_present_position))
        return dxl_present_position

    def set_goal_pos_callback(self, data):
        print("Set Goal Position of ID %s = %s" % (data.id, data.position))
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, data.id, ADDR_GOAL_POSITION, data.position)
        print(dxl_comm_result, dxl_error)
        return True

    def read_write_py_node(self):
        rospy.init_node('read_write_py_node')
        rospy.Service('set_position', SetPosition, self.set_goal_pos_callback)
        rospy.Service('get_position', GetPosition, self.get_present_pos)
        rospy.spin()


def main():
    service = Service(DEVICENAME='/dev/ttyUSB0')
    try:
       service.portHandler.openPort()
       print("Succeeded to open the port")
    except Exception as e:
        print(e)
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    try:
        service.portHandler.setBaudRate(BAUDRATE)
        print("Succeeded to change the baudrate")
    except Exception as e:
        print(e)
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

    dxl_comm_result, dxl_error = service.packetHandler.write1ByteTxRx(service.portHandler, DXL_ID, ADDR_TORQUE_ENABLE, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % service.packetHandler.getTxRxResult(dxl_comm_result))
        print("Press any key to terminate...")
        getch()
        quit()
    elif dxl_error != 0:
        print("%s" % service.packetHandler.getRxPacketError(dxl_error))
        print("Press any key to terminate...")
        getch()
        quit()
    else:
        print("DYNAMIXEL has been successfully connected")

    service.read_write_py_node()

if __name__ == '__main__':
    main()