# 예시 코드
from ..utils.base_action import BaseAction
import DR_init
import time
ON, OFF = 1, 0
DR = None
VEL, ACC = 100, 30
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
        pick_poses = self.poses['pick']
        pick_before_poses = self.poses['pick_before']
        shaking_poses = self.poses['shaking']
        place_before_poses = self.poses["place_before"]
        # 1. 잡는 위치로 이동
        DR.movej([0,0,90,0,90,0],vel=VEL,acc=ACC)
        DR.movel(pick_before_poses['task'],vel=VEL,acc=ACC)
        DR.movel(pick_poses['task'],vel=VEL,acc=ACC)
        self.grasp()

        DR.movel(place_before_poses['task'],vel=VEL,acc=ACC)
        DR.movel(shaking_poses['task'],vel=VEL,acc=ACC,ref=DR.DR_BASE)

        DR.move_periodic([50, 50, 0, 0, 0, 45], [1.25,0.75, 0, 0, 0, 2],repeat=10,atime=0.1,ref=DR.DR_TOOL)
        # 2. 충돌 방지 경로
        DR.movel(shaking_poses['task'],vel=VEL,acc=ACC)
        DR.movel(place_before_poses['task'],vel=VEL,acc=ACC)
        # 3. 내려놓기
        DR.movel(pick_poses['task'],vel=VEL,acc=ACC)
        self.release()
        DR.movel(pick_before_poses['task'],vel=VEL,acc=ACC)
        DR.movel(place_before_poses['task'],vel=VEL,acc=ACC)
        home_pose = place_before_poses['task'].copy()
        home_pose[3:] = [0,-180,0]
        DR.movel(home_pose,vel=VEL,acc=ACC)
        DR.movej([0,0,90,0,90,0],vel=VEL,acc=ACC)
        
        
    def grasp(self):
        DR.set_digital_output(1,ON)
        DR.set_digital_output(2,OFF)
        DR.wait(1)

    def release(self):
        DR.set_digital_output(1,OFF)
        DR.set_digital_output(2,OFF)
        DR.wait(1)

        