# pick and place in 1 method. from pos1 to pos2 @20241104
import time
import rclpy
import DR_init
from DSR_ROBOT2 import (
    set_digital_output,
    get_digital_input,
    set_tool,
    set_tcp,
    movej,
    move_spiral
)

### 힘 제어 : BASE 좌표계 기준
def down_stir_up(target_pos, turning_radius=10, stir_repeat=10, return_posx=100, force_desired=20):
    k_d = [3000.0, 3000.0, 3000.0, 200.0, 200.0, 200.0] ## need to check
    f_d = [0.0, 0.0, -force_desired, 0.0, 0.0, 0.0]
    f_dir = [0, 0, 1, 0, 0, 0]
    
    task_compliance_ctrl(k_d)
    set_desired_force(f_d, f_dir)

    while True:
        if check_position_condition(axis=DR_AXIS_Z, max=target_pos, ref=DR_BASE):
            stop(st_mode=DR_QSTOP)
            release_force(time=0.5)
            release_compliance_ctrl()
            break          
            
    move_periodic(
        amp=[turning_radius, turning_radius, 0, 0, 0, 0],
        period=[1, 1, 0, 0, 0, 0],
        repeat=stir_repeat
        ref=DR_TOOL
        )
    
    movej(pos=posx(0,0,100,0,0,0), ref=DR_BASE, mod=DR_MV_MOD_REL)
    
