import rclpy
from rclpy.node import Node
import DR_init
import time
from DR_common2 import posx,posj

ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 30, 30

# DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL
ON, OFF = 1, 0


# def wait_digital_input(sig_num):
#         while not get_digital_input(sig_num):
#             time.sleep(0.5)
#             print(f"Wait for digital input: {sig_num}")
#             pass


class RobotArm(Node):
    def __init__(self,DR):
        super().__init__('robot_arm')
        # super().__init__('robot_arm', namespace=ROBOT_ID

        self.DR = DR
    def movej(self, pose):
        self.DR.movej(posj(pose), vel=VELOCITY, acc=ACC)

    def movel(self, pose):
        self.DR.movel(posx(pose), vel=VELOCITY, acc=ACC)


    def task_compliance_ctrl(self, stx):
        self.DR.task_compliance_ctrl(stx)

    def set_desired_force(self, fd, f_dir):
        self.DR.set_desired_force(fd, f_dir)

    def check_force_condition(self, axis, ref, **kwargs):
        self.DR.check_force_condition(axis, ref, **kwargs)

    def check_position_condition(self, axis, **kwargs):
        self.DR.check_position_condition(axis, **kwargs)

    def release_force(self, time):
        self.DR.release_force(time)

    def release_compliance_ctrl(self):
        self.DR.release_compliance_ctrl()

    def move_periodic(self, amp, period):
        self.DR.move_periodic(amp, period, repeat=10)


    def grasp(self):
        self.DR.set_digital_output(1, ON)
        self.DR.wait(0.5)

    def release(self):
        self.DR.set_digital_output(1, OFF)
        self.DR.wait(0.5)

    def set_custom_grip(self, x):
        if x == 0:
            self.DR.set_digital_output(2, OFF)
        elif x == 1:
            self.DR.set_digital_output(2, ON)

    def stop(self):
        pass
        
    def emergency_stop(self):
        pass
    def amove_periodic(self,amp,period):
        self.DR.amove_periodic(amp=amp, period=period, atime=0.02, repeat=10, ref=self.DR.DR_TOOL)
