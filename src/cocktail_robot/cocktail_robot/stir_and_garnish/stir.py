# pick and place in 1 method. from pos1 to pos2 @20241104
import DR_init
import time
from ..utils.base_action import BaseAction


VELOCITY, ACCURACY = 60, 60
ON, OFF = 1, 0
### 힘 제어 : BASE 좌표계 기준
class StirAction(BaseAction):
    def __init__(self, node, stir_pose):
        DR_init.__dsr__node = node

        try:
            import DSR_ROBOT2

        except ImportError as e:
            print(f"Error importing DSR_ROBOT2 : {e}")
            return
        
        global DR
        DR = DSR_ROBOT2

        self.stir_pose = stir_pose
        self.grasp_option = 1

        
    def execute(self):
        # print('task ready')
        DR.movel(pos=self.stir_pose["task_ready"]["task"], vel=VELOCITY, acc = ACCURACY)

        # print('grasp position')
        DR.movel(self.stir_pose["spoon_grasp_ready"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(self.stir_pose["spoon_grasp"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(pos=[0,-30,0,0,0,0], vel=VELOCITY, acc = ACCURACY, mod=DR.DR_MV_MOD_REL, ref=DR.DR_BASE)
        
        # print('grasp')
        self.grasp(self.grasp_option)

        # print('grasp up')
        DR.movel(pos=[0,0,200,0,0,0], vel=VELOCITY, acc = ACCURACY, mod=DR.DR_MV_MOD_REL, ref=DR.DR_BASE)
       
        # print('stir position')
        DR.movel(pos=self.stir_pose["task_ready"]["task"], vel=VELOCITY, acc = ACCURACY)        
        DR.movel(self.stir_pose["stir"]["task"], vel=VELOCITY, acc = ACCURACY)
        # print('stir')
        self.down_stir()
        
        # print('stir up')
        DR.movel(self.stir_pose["stir"]["task"], vel=VELOCITY, acc = ACCURACY)
        
        # print('go back and release')
        DR.movel(self.stir_pose["task_ready"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(self.stir_pose["spoon_drop"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(pos=[0,0,-200,0,0,0], vel=VELOCITY, acc = ACCURACY, mod=DR.DR_MV_MOD_REL, ref=DR.DR_BASE)
        self.release(self.grasp_option)
        DR.movel(self.stir_pose["spoon_grasp"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(self.stir_pose["spoon_grasp_ready"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(pos=self.stir_pose["task_ready"]["task"], vel=VELOCITY, acc = ACCURACY)


    def down_stir(self, target_pos=336.4, turning_radius=10, stir_repeat=4, force_desired=55):
        DR.set_ref_coord(DR.DR_BASE)
        k_d = [5, 5, 50, 100, 100, 100] ## need to check
        f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
        f_dir = [0, 0, 1, 0, 0, 0]
        
        DR.task_compliance_ctrl(k_d)
        DR.set_desired_force(f_d, f_dir)

        while not DR.check_position_condition(axis=DR.DR_AXIS_Z, max=target_pos, ref=DR.DR_BASE):
            time.sleep(0.5)
            pass

        DR.release_force(time=0.5)
        DR.release_compliance_ctrl()

        DR.move_periodic(
            amp=[turning_radius, turning_radius, 0, 0, 0, 0],
            period=[1, 1, 0, 0, 0, 0],
            repeat=stir_repeat,
            ref=DR.DR_BASE
            )
        
        # self.movej(pos=[0,0,100,0,0,0], vel=VELOCITY, acc=ACCURACY, mod=self.DR_MV_MOD_REL)

    def grasp(self, x):
        self._set_custom_grasp(x)
        DR.set_digital_output(1, ON)
        time.sleep(0.5)

    def release(self, x):
        self._set_custom_grasp(x)
        DR.set_digital_output(1, OFF)
        time.sleep(0.5)

    def _set_custom_grasp(self, x):
        if x == 0:
            DR.set_digital_output(2, OFF)
        elif x == 1:
            DR.set_digital_output(2, ON)
        
