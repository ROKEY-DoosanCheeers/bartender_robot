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
)

from DR_common2 import posj

def vertical_grasp(height, grasp_num, release_num):
    posx_down = [0,0,-height,0,0,0]
    posx_up = [0,0,height,0,0,0]
    movel(pos=posx_down, ref=DR_BASE, mod=DR_MV_MOD_REL)
    grasp(grasp_num, release_num)
    movel(pos=posx_up, ref=DR_BASE, mod=DR_MV_MOD_REL)

def vertical_release(height, grasp_num, release_num):
    posx_down = [0,0,-height,0,0,0]
    posx_up = [0,0,height,0,0,0]
    movel(pos=posx_down, ref=DR_BASE, mod=DR_MV_MOD_REL)
    release(grasp_num, release_num)
    movel(pos=posx_up, ref=DR_BASE, mod=DR_MV_MOD_REL)

def grasp(grasp_num, release_num):
    set_digital_output(grasp_num, ON)
    set_digital_output(release_num, OFF)
    wait_digital_input(grasp_num)

def release(grasp_num, release_num):
    print("set for digital output 0 1 for release")
    set_digital_output(release_num, ON)
    set_digital_output(grasp_num, OFF)
    wait_digital_input(release_num)

def wait_digital_input(sig_num):
    while not get_digital_input(sig_num):
        time.sleep(0.5)
        print(f"Wait for digital input: {sig_num}")
        pass