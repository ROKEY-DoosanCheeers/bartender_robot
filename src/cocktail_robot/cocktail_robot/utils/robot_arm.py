import rclpy
from rclpy.node import Node
import DR_init
import time

# ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 30, 30

# DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL
ON, OFF = 1, 0


try:
    from DSR_ROBOT2 import set_tool, set_tcp, set_digital_output, get_digital_input, movej, movel
    from DR_common2 import posx, posj
except ImportError as e:
    print(f"Error importing DSR_ROBOT2: {e}")

def wait_digital_input(sig_num):
        while not get_digital_input(sig_num):
            time.sleep(0.5)
            print(f"Wait for digital input: {sig_num}")
            pass


class RobotArm(Node):
    def __init__(self):
        super().__init__('robot_arm')
        # super().__init__('robot_arm', namespace=ROBOT_ID)
        DR_init.__dsr__node = self
        
        set_tool("Tool Weighttest")
        set_tcp("GripperDA_v2")


    def movej(self, pose):
        movej(pose, vel=VELOCITY, acc=ACC)

    def movel(self, pose):
        movel(pose, vel=VELOCITY, acc=ACC)

    def grasp(self):
        set_digital_output(1, ON)
        set_digital_output(2, OFF)
        wait_digital_input(1)

    def release(self):
        set_digital_output(2, ON)
        set_digital_output(1, OFF)
        wait_digital_input(2)

    def set_custom_grip(self, x):
        if x == 0:
            set_digital_output(3, OFF)
            set_digital_output(4, OFF)
        elif x == 1:
            set_digital_output(3, OFF)
            set_digital_output(4, ON)
        elif x == 2:
            set_digital_output(3, ON)
            set_digital_output(4, OFF)
        elif x == 3:
            set_digital_output(3, ON)
            set_digital_output(4, ON)

        
    def emergency_stop(self):
        pass
