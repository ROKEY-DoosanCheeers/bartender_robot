# 예시 코드
from ..utils.base_action import BaseAction
import DR_init
import time

DR = None

class ShakerAction(BaseAction):
    def __init__(self, node, poses):
        DR_init.__dsr__node = node
        self.poses = poses
        global DR
        try:
            import DSR_ROBOT2 as DR
        except ImportError as e:
            print(f"Error importing DSR_ROBOT2 : {e}")
            return

    def execute(self):
        DR.set_velx(vel1=100,vel2=50)
        DR.set_accx(30, 30)
        pick_poses = self.poses['pick']
        pick_before_poses = self.poses['pick_before']
        shaking_poses = self.poses['shaking']
        place_before_poses = self.poses["place_before"]
        # 1. 잡는 위치로 이동
        DR.movej([0,0,90,0,90,0])
        DR.movel(pick_before_poses['task'])
        DR.movel(pick_poses['task'])
        self.grasp()
        
        DR.movel(shaking_poses['task'])
        # DR.movej([0, -30, 90, 0, 60, 0])
        # DR.movej([10, -20, 100, 0, 70, 10])
        # DR.movej([-10, -40, 110, 0, 50, -10])
        DR.amove_periodic([50,50,0,0,0,15],[1,1.5,0,0,0,1])
        # 2. 충돌 방지 경로
        DR.movel(shaking_poses['task'])
        DR.movel(place_before_poses['task'])
        # 3. 내려놓기
        DR.movel(pick_poses['task'])
        self.release()
        DR.movel(pick_before_poses['task'])
        
        
    def grasp():
        pass

    def release():
        pass