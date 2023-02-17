import rospy
import time
# from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Int32MultiArray
from model.class_xc330 import xc330
import numpy as np

class DynamixelBase(object):
    def __init__(self):
        self.transform_data = None 
        self.markers = None
        # self.tick = 0
        self.transform_data_sub = rospy.Subscriber('/dynamixel/control', Int32MultiArray, self.callback)
        self.snapbot = xc330('SNAPBOT', _USB_NUM=1)
        self.snapbot.connect()
        self.snapbot.set_torque([1])
        self.snapbot.set_operatingmode([4])

        # tic_temp = 0
        # while self.tick<2:
        #     time.sleep(1e-3)
        #     tic_temp = tic_temp + 1
        #     if tic_temp > 5000:
        #         print ("[ERROR] Vicon Base")
        #         break
      
    def callback(self, data):
        # rospy.loginfo(rospy.get_name())
        # for marker in data.markers:
        #     rospy.loginfo(marker.translation)
        currpos = self.snapbot.get_currpos()
        print(currpos)
        print(data.data)
        minmaxInterval = 5000
        self.snapbot.set_minmaxpos(currpos-np.ones_like(currpos)*minmaxInterval,currpos+np.ones_like(currpos)*minmaxInterval)
        initpos = [data.data[0]] #  np.array([15,-15,30,-15]
        self.snapbot.set_goalposcluster(initpos,1)

        


if __name__ == "__main__":
    rospy.init_node("Test")
    D = DynamixelBase()
    # V.listener()
    rospy.spin()
