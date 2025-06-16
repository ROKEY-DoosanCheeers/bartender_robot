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
    from DSR_ROBOT2 import (set_tool, set_tcp,
                            set_digital_output, # get_digital_input,
                            task_compliance_ctrl, set_desired_force, check_force_condition, check_position_condition,
                            amove_periodic,
                            release_force, release_compliance_ctrl,
                            move_periodic,
                            wait, movej, movel,DR_TOOL)
    from DR_common2 import posx, posj
except ImportError as e:
    print(f"Error importing DSR_ROBOT2: {e}")

# def wait_digital_input(sig_num):
#         while not get_digital_input(sig_num):
#             time.sleep(0.5)
#             print(f"Wait for digital input: {sig_num}")
#             pass


class RobotArm(Node):
    def __init__(self):
        super().__init__('robot_arm')
        # super().__init__('robot_arm', namespace=ROBOT_ID)
        DR_init.__dsr__node = self
        
        set_tool("Tool Weighttest")
        set_tcp("GripperDA_v2")

    def movej(self, pose, **kwargs):
        movej(pose, vel=VELOCITY, acc=ACC, **kwargs)

    def movel(self, pose, **kwargs):
        movel(pose, vel=VELOCITY, acc=ACC, **kwargs)


    def task_compliance_ctrl(self, stx):
        task_compliance_ctrl(stx)

    def set_desired_force(self, fd, f_dir):
        set_desired_force(fd, f_dir)

    def check_force_condition(self, axis, ref, **kwargs):
        check_force_condition(axis, ref, **kwargs)

    def check_position_condition(self, axis, **kwargs):
        check_position_condition(axis, **kwargs)

    def release_force(self, time):
        release_force(time)

    def release_compliance_ctrl(self):
        release_compliance_ctrl()

    def move_periodic(self, amp, period, repeat, ref, **kwargs):
        move_periodic(amp, period, repeat, ref, **kwargs)


    def grasp(self):
        set_digital_output(1, ON)
        wait(0.5)

    def release(self):
        set_digital_output(1, OFF)
        wait(0.5)

    def set_custom_grip(self, x):
        if x == 0:
            set_digital_output(2, OFF)
        elif x == 1:
            set_digital_output(2, ON)

    def stop(self):
        pass
        
    def emergency_stop(self):
        pass
    def amove_periodic(self,amp,period):
        amove_periodic(amp=amp, period=period, atime=0.02, repeat=10, ref=DR_TOOL)
