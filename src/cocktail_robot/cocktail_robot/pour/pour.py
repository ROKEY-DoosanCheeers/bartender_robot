import time
import rclpy
import DR_init
from ..utils.base_action import BaseAction


VELOCITY, ACCURACY = 70, 60
ON, OFF = 1, 0
DR = None

# PourAction(arm, "tequila", 50, shaker, poses["pour_tequila"])

class PourAction:
    def __init__(self, node, ingredient, amount, target, pour_pose):
        DR_init.__dsr__node = node

        try:
            import DSR_ROBOT2

        except ImportError as e:
            print(f"Error importing DSR_ROBOT2 : {e}")
            return

        global DR
        DR = DSR_ROBOT2
        
        self.grasp_option = 0
        self.ingredient = ingredient
        self.target = target
        self.pour_pose = pour_pose


    def execute(self):
        # set position
        DR.movej(self.pour_pose["pour_ready"]["joint"], vel=VELOCITY, acc = ACCURACY)
        self.release(self.grasp_option)

        # pick
        DR.movel(self.pour_pose["pick_before"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movej(self.pour_pose["pick_before"]["joint"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(self.pour_pose[self.ingredient]["task"], vel=VELOCITY, acc = ACCURACY)
        self.grasp(self.grasp_option)
        DR.movel(self.pour_pose["pick_up"]["task"], vel=VELOCITY, acc = ACCURACY)

        # pour
        DR.movel(self.pour_pose[self.target]["ready"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movej(self.pour_pose[self.target]["ready"]["joint"], vel=VELOCITY, acc = ACCURACY)
        DR.movej(self.pour_pose[self.target]["start"]["joint"], vel=VELOCITY, acc = ACCURACY)
        time.sleep(1)
        DR.movej(self.pour_pose[self.target]["ready"]["joint"])

        # go to place
        DR.movel(self.pour_pose["pick_up"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(self.pour_pose["pick_before"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movej(self.pour_pose["pick_before"]["joint"], vel=VELOCITY, acc = ACCURACY)
        DR.movel(self.pour_pose[self.ingredient]["task"], vel=VELOCITY, acc = ACCURACY)
        self.release(self.grasp_option)

        # end
        DR.movel(self.pour_pose["pick_before"]["task"], vel=VELOCITY, acc = ACCURACY)
        DR.movej(self.pour_pose["pour_ready"]["joint"], vel=VELOCITY, acc = ACCURACY)


        # self.grasp(self.grasp_option)
        # self.release(self.grasp_option)


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




