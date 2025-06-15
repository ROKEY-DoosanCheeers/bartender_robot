# pick and place in 1 method. from pos1 to pos2 @20241104
import time
import rclpy
from DSR_ROBOT2 import DR_MV_MOD_REL, DR_BASE, DR_AXIS_Z, DR_QSTOP, DR_TOOL
from DR_common2 import posx, posj
from ..utils.base_action import BaseAction



### 힘 제어 : BASE 좌표계 기준
class StirAction(BaseAction):
    def __init__(self, arm, stir_pose):
        self.arm = arm
        self.stir_pose = stir_pose

    def execute(self):
        self.arm.movej(self.stir_pose["spoon_grasp_0"])
        self.arm.movej(self.stir_pose["spoon_grasp_1"])
        self.arm.grasp()
        self.arm.movel(pos=[0,0,160,0,0,0], mod=DR_MV_MOD_REL, ref=DR_BASE)
        self.arm.movej(self.stir_pose["stir"]) ##### pos before put in
        self.down_stir_up()
        self.arm.movej(self.stir_pose["spoon_grasp_1"])
        self.arm.movej(self.stir_pose["spoon_grasp_0"])



    def down_stir_up(self, target_pos, turning_radius=10, stir_repeat=10, return_posx=100, force_desired=20):
        k_d = [3000.0, 3000.0, 3000.0, 200.0, 200.0, 200.0] ## need to check
        f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
        f_dir = [0, 0, 1, 0, 0, 0]
        
        self.arm.task_compliance_ctrl(k_d)
        self.arm.set_desired_force(f_d, f_dir)

        while True:
            if self.arm.check_position_condition(axis=DR_AXIS_Z, max=target_pos, ref=DR_BASE):
                self.arm.stop(st_mode=DR_QSTOP)
                self.arm.release_force(time=0.5)
                self.arm.release_compliance_ctrl()
                break          
                
        self.arm.move_periodic(
            amp=[turning_radius, turning_radius, 0, 0, 0, 0],
            period=[1, 1, 0, 0, 0, 0],
            repeat=stir_repeat,
            ref=DR_TOOL
            )
        
        self.arm.movej(pos=posx(0,0,100,0,0,0), ref=DR_BASE, mod=DR_MV_MOD_REL)
        
