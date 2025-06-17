# pick and place in 1 method. from pos1 to pos2 @20241104
import DR_init
import time
from ..utils.base_action import BaseAction


VELOCITY, ACCURACY = 70, 60
ON, OFF = 1, 0
### 힘 제어 : BASE 좌표계 기준
class StirAction(BaseAction):
    def __init__(self, node, stir_pose):
        DR_init.__dsr__node = node
        print('initialized')
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
        
        self.stir_pose = stir_pose
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
        self.movel(pos=self.stir_pose["spoon_grasp_0"]["task"], vel=VELOCITY, acc = ACCURACY)
        self.movel(self.stir_pose["spoon_grasp_1"]["task"], vel=VELOCITY, acc = ACCURACY)
        self.grasp(self.grasp_option)
        self.movel(pos=[0,0,160,0,0,0], vel=VELOCITY, acc = ACCURACY, mod=self.DR_MV_MOD_REL, ref=self.DR_BASE)
        self.movel(pos=self.stir_pose["spoon_grasp_0"]["task"], vel=VELOCITY, acc = ACCURACY)
        self.movel(self.stir_pose["stir"]["task"], vel=VELOCITY, acc = ACCURACY)
        self.down_stir_up()
        self.movel(self.stir_pose["stir"]["task"], vel=VELOCITY, acc = ACCURACY)
        self.movel(self.stir_pose["spoon_grasp_0"]["task"], vel=VELOCITY, acc = ACCURACY)


    def down_stir_up(self, target_pos=336.4, turning_radius=10, stir_repeat=10, return_posx=100, force_desired=20):
        k_d = [3000.0, 3000.0, 3000.0, 200.0, 200.0, 200.0] ## need to check
        f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
        f_dir = [0, 0, 1, 0, 0, 0]
        
        self.task_compliance_ctrl(k_d)
        self.set_desired_force(f_d, f_dir)

        while True:
            if not self.check_position_condition(axis=self.DR_AXIS_Z, max=target_pos, ref=self.DR_BASE):
                time.sleep(0.5)
                self.release_force(time=0.5)
                self.release_compliance_ctrl()
                break       
            else:
                pass   
                
        self.move_periodic(
            amp=[turning_radius, turning_radius, 0, 0, 0, 0],
            period=[1, 1, 0, 0, 0, 0],
            repeat=stir_repeat,
            ref=self.DR_BASE
            )
        
        # self.movej(pos=[0,0,100,0,0,0], vel=VELOCITY, acc=ACCURACY, mod=self.DR_MV_MOD_REL)

    def grasp(self, x):
        self._set_custom_grasp(x)
        self.set_digital_output(1, ON)
        time.sleep(0.5)

    def release(self, x):
        self._set_custom_grasp(x)
        self.set_digital_output(1, OFF)
        time.sleep(0.5)

    def _set_custom_grasp(self, x):
        if x == 0:
            self.set_digital_output(2, OFF)
        elif x == 1:
            self.set_digital_output(2, ON)
        
