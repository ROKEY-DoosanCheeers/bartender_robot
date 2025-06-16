# 예시 코드
from .base_action import BaseAction
from DR_common2 import posx

class ShakerAction(BaseAction):
    LOGATIONS = {
        'shaker': {'pick': posx(641.24, 1.38, 171.9, 60.98, 89.96, 90.34), 'before_pick': posx(605.59, -62.09, 171.29, 60.45, 89.97, 90.25)},
        'shaking_pose': {'pick_up': posx(545.48, -6.88, 658.82, 178.42, -78.39, -93.5), 'place_up': posx(641.24, 1.38, 271.9, 60.98, 89.96, 90.34)},
    }

    def __init__(self, arm):
        self.arm = arm

    def execute(self):
        shaker_poses = self.LOGATIONS['shaker']
        shaking_poses = self.LOGATIONS['shaking_pose']

        # 1. 잡는 위치로 이동
        self.arm.movel(shaker_poses['before_pick'])
        self.arm.movel(shaker_poses['pick'])
        self.arm.grasp()
        
        self.arm.movel(shaking_poses['pick_up'])
        self.arm.amove_periodic(amp=[50,50,0,0,0,45], period=[2,3,0,0,0,1], atime=0.02, repeat=10, ref=DR_TOOL)
        # 2. 충돌 방지 경로
        self.arm.movel(shaking_poses['place_up'])

        # 3. 내려놓기
        self.arm.movel(shaker_poses['pick'])
        self.arm.release()
        self.arm.movel(shaker_poses['before_pick'])
        
        