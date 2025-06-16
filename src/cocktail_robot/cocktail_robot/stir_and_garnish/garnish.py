# pick and place in 1 method. from pos1 to pos2 @20241104
import time
import rclpy
from DSR_ROBOT2 import DR_MV_MOD_REL, DR_BASE, DR_AXIS_Z, DR_QSTOP, DR_TOOL
from DR_common2 import posx, posj
from ..utils.base_action import BaseAction



### 힘 제어 : BASE 좌표계 기준
class GarnishAction(BaseAction):
    def __init__(self, arm, garnish_pose, topping):
        self.arm = arm
        self.garnish_pose = garnish_pose
        self.topping = topping

    def execute(self):
        self.arm.movej(self.garnish_pose[self.topping]["joint"]) #### pos before grasp
        self.arm.movel(pos=[0,0,-40,0,0,0], mod=DR_MV_MOD_REL, ref=DR_BASE)
        self.arm.grasp()
        self.arm.movel(pos=[0,0,40,0,0,0], mod=DR_MV_MOD_REL, ref=DR_BASE)
        self.arm.movej(self.garnish_pose["garnish_0"]["joint"])
        self.arm.movej(self.garnish_pose["garnish_drop"]["joint"])

