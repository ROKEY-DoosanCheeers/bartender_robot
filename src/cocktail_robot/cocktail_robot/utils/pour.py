# 예시 코드

from .base_action import BaseAction
from DR_common2 import posx

class PourreadyAction(BaseAction):
    def __init__(self, arm, ingredient, amount, pose_dict):     # pose_dict로 location.yaml 파일을 불러옴
        self.arm = arm
        self.ingredient = ingredient
        self.amount = amount
        self.task_pose = pose_dict["task"]  # task 좌표
        self.joint_pose = pose_dict["joint"] # joint 좌표 선언

    def execute(self):
        self.arm.movel(self.task_pose)  # movel task 수행
        self.arm.movej(self.joint_pose) # movej joint 수행