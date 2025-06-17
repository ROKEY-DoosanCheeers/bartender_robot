# pick and place in 1 method. from pos1 to pos2 @20241104
import time
import rclpy
import DR_init
from ..utils.base_action import BaseAction



### 힘 제어 : BASE 좌표계 기준
class GarnishAction(BaseAction):
    def __init__(self, node, garnish_pose, topping):
        DR_init.__dsr__node = node
        try:
            from DSR_ROBOT2 import (
                release_compliance_ctrl,
                check_force_condition,
                check_position_condition,
                task_compliance_ctrl,
                set_desired_force,
                release_force,
                release_compliance_ctrl,
                set_digital_output,
                move_periodic,
                movej,
                movel,
                DR_MV_MOD_REL,
                DR_AXIS_Z,
                DR_BASE,
            )
            from DR_common2 import posx

        except ImportError as e:
            print(f"Error importing DSR_ROBOT2 : {e}")
            return
        
        self.garnish_pose = garnish_pose
        self.grasp_option = 1

        self.posx = posx
        self.movej = movej
        self.movel = movel
        self.DR_MV_MOD_REL = DR_MV_MOD_REL
        self.DR_BASE = DR_BASE
        self.task_compliance_ctrl = task_compliance_ctrl
        self.set_desired_force = set_desired_force
        self.check_position_condition = check_position_condition
        self.DR_AXIS_Z = DR_AXIS_Z
        self.release_force = release_force
        self.release_compliance_ctrl = release_compliance_ctrl
        self.move_periodic = move_periodic
        self.set_digital_output = set_digital_output


    def execute(self):
        self.movej(self.garnish_pose[self.topping]["joint"]) #### pos before grasp
        self.movel(pos=[0,0,-40,0,0,0], mod=self.DR_MV_MOD_REL, ref=self.DR_BASE)
        self.grasp()
        self.movel(pos=[0,0,40,0,0,0], mod=self.DR_MV_MOD_REL, ref=self.DR_BASE)
        self.movej(self.garnish_pose["garnish_0"]["joint"])
        self.movej(self.garnish_pose["garnish_drop"]["joint"])

