# 예시 코드

from .base_action import BaseAction
from DR_common2 import posx

class PourAction(BaseAction):
    POSE_MAP = {
        "pour_tequila": posx([0, 0, 0, 0, 0, 0]),
        "pour_blue":    posx([0, 0, 0, 0, 0, 0]),
        "pour_red":     posx([0, 0, 0, 0, 0, 0]),
    }


    def __init__(self, arm, ingredient, amount, pose):
        self.arm = arm
        self.ingredient = ingredient
        self.amount = amount
        self.pose_name = pose

    def execute(self):
        pose = self.POSE_MAP.get(self.pose_name)

        if pose is None:
            print(f"[PourAction] 정의되지 않은 pose: {self.pose_name}")
            return
        
        self.arm.movel(pose)