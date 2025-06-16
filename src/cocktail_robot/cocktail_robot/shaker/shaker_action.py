# 예시 코드
from ..utils.base_action import BaseAction
from DR_common2 import posx

class ShakerAction(BaseAction):
    def __init__(self, arm, poses):
        self.arm = arm
        self.poses = poses

    def execute(self):
        pick_poses = self.poses['pick']
        pick_before_poses = self.poses['pick_before']
        shaking_poses = self.poses['shaking']
        place_before_poses = self.poses["place_before"]
        # 1. 잡는 위치로 이동
        self.arm.movel(pick_before_poses['task'])
        self.arm.movel(pick_poses['task'])
        self.arm.grasp()
        
        self.arm.movel(shaking_poses['task'])
        self.arm.amove_periodic(amp=[100,100,0,0,0,30], period=[1,1.5,0,0,0,0.5], atime=0.02, repeat=10, ref=DR_TOOL)
        # 2. 충돌 방지 경로
        self.arm.movel(shaking_poses['task'])
        self.arm.movel(place_before_poses['task'])
        # 3. 내려놓기
        self.arm.movel(pick_poses['task'])
        self.arm.release()
        self.arm.movel(pick_before_poses['task'])
        
        