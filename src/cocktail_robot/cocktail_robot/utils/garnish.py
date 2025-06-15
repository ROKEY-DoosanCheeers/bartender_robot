# 예시 코드

from .base_action import BaseAction
from DR_common2 import posx

class GarnishAction(BaseAction):
    GARNISH_LOGATIONS = {
        'lime': {'pick': posx([0, 0, 0, 0, 0, 0]), 'place': posx([0, 0, 0, 0, 0, 0])},
        'cherry': {'pick': posx([0, 0, 0, 0, 0, 0]), 'place': posx([0, 0, 0, 0, 0, 0])},
    }

    def __init__(self, arm, topping):
        self.arm = arm
        self.topping = topping

    def execute(self):
        poses = self.GARNISH_POSES[self.topping]

        # 1. 잡는 위치로 이동
        self.arm.movel(poses['pick'])
        self.arm.grasp()
        
        # 2. 충돌 방지 경로
        self.arm.movej(poses['pick'])

        # 3. 내려놓기
        self.arm.movel(poses['place'])
        self.arm.release()