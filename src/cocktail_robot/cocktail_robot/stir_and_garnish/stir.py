# pick and place in 1 method. from pos1 to pos2 @20241104
import DR_init
import time
from ..utils.base_action import BaseAction



ON, OFF = 1, 0
### 힘 제어 : BASE 좌표계 기준
class StirAction(BaseAction):
    def __init__(self, node, stir_pose):
        DR_init.__dsr__node = node
        try:
            from DSR_ROBOT2 import (
                release_compliance_ctrl,
                check_force_condition,
                task_compliance_ctrl,
                set_desired_force,
                set_tool,
                set_tcp,
                movej,
                movel,
                DR_FC_MOD_REL,
                DR_AXIS_Z,
                DR_BASE,
            )
            from DR_common2 import posx

        except ImportError as e:
            print(f"Error importing DSR_ROBOT2 : {e}")
            return
        
        self.stir_pose = stir_pose
        self.grasp_option = 1

    def execute(self):
        movej(self.stir_pose["spoon_grasp_0"]["joint"])
        movej(self.stir_pose["spoon_grasp_1"]["joint"])
        self.grasp(self.grasp_option)
        movel(pos=[0,0,160,0,0,0], mod=DR_MV_MOD_REL, ref=DR_BASE)
        movej(self.stir_pose["stir"]["joint"])
        self.down_stir_up()
        movej(self.stir_pose["spoon_grasp_1"]["joint"])
        movej(self.stir_pose["spoon_grasp_0"]["joint"])


    def down_stir_up(self, target_pos=336.4, turning_radius=10, stir_repeat=10, return_posx=100, force_desired=20):
        k_d = [3000.0, 3000.0, 3000.0, 200.0, 200.0, 200.0] ## need to check
        f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
        f_dir = [0, 0, 1, 0, 0, 0]
        
        task_compliance_ctrl(k_d)
        set_desired_force(f_d, f_dir)

        while True:
            if not check_position_condition(axis=DR_AXIS_Z, max=target_pos, ref=DR_BASE):
                time.sleep(0.5)
                release_force(time=0.5)
                release_compliance_ctrl()
                break       
            else:
                pass   
                
        move_periodic(
            amp=[turning_radius, turning_radius, 0, 0, 0, 0],
            period=[1, 1, 0, 0, 0, 0],
            repeat=stir_repeat,
            ref=DR_BASE
            )
        
        movej(pos=posx(0,0,100,0,0,0), ref=DR_BASE, mod=DR_MV_MOD_REL)

    def grasp(self, x):
        self._set_custom_grasp(x)
        set_digital_output(1, ON)
        wait(0.5)

    def release(self, x):
        self._set_custom_grasp(x)
        set_digital_output(1, OFF)
        wait(0.5)

    def _set_custom_grasp(self, x):
        if x == 0:
            set_digital_output(2, OFF)
        elif x == 1:
            set_digital_output(2, ON)
        
