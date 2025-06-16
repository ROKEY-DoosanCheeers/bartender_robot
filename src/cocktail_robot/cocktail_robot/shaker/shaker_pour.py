# 예시 코드
from .base_action import BaseAction
from DR_common2 import posx

class PourAction(BaseAction):
    LOGATIONS = {
        'shaker': {'pick': posx(641.24, 1.38, 171.9, 60.98, 89.96, 90.34), 'before_pick': posx(605.59, -62.09, 171.29, 60.45, 89.97, 90.25)},
        'pour_pose': {'pour_before' : posx(737.32, -253.16, 288.69, 60.32, 115.48, 0.12),'pour' : posx(737.32, -253.16, 288.69, 6.32, 115.48, 0.12)},
    }

    def __init__(self, arm):
        self.arm = arm

    def execute(self):
        shaker_poses = self.LOGATIONS['shaker']
        pour_poses = self.LOGATIONS['pour_pose']

        # 1. 잡는 위치로 이동
        self.arm.movel(shaker_poses['before_pick'])
        self.arm.movel(shaker_poses['pick'])
        self.arm.grasp()
        
        self.arm.movel(pour_poses['pour_before'])
        # 2. 충돌 방지 경로
        self.arm.movel(pour_poses['pour'])
        self.arm.movel(pour_poses['pour_before'])

        drop_before = trans(shaker_poses['pick'],[0,0,100,0,0,0],DR_BASE,DR_BASE)
        # 3. 내려놓기
        self.arm.movel(drop_before)
        self.arm.release()
        self.arm.movel(shaker_poses['pick'])
        
        