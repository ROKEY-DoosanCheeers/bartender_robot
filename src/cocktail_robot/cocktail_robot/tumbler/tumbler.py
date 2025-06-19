from ..utils.base_action import BaseAction
import DR_init
import time
#from ..utils.base_action import BaseAction
VELOCITY, ACCURACY = 100,60
ON, OFF = 1, 0
DR = None
class TumblerAction(BaseAction):
    def __init__(self,node, tumbler_pose, move):     # pose_dict로 location.yaml 파일을 불러옴
        self.move = move
        DR_init.__dsr__node = node
        print('initialized')
        global DR
        try:
            import DSR_ROBOT2 as DR 

        except ImportError as e:
            print(f"Error importing DSR_ROBOT2 : {e}")
            return
        self.tumbler_pose = tumbler_pose
        self.grasp_option = 0
        

    def execute(self):
        tumbler_cover_up = self.tumbler_pose["cover_top"]["task"].copy()
        tumbler_mouth_up = self.tumbler_pose["mouth_close"]["task"].copy()
        tumbler_mouth_up_open = self.tumbler_pose["mouth_open"]["task"].copy()
        
        tumbler_cover_up[2] = 250
        tumbler_mouth_up[2] = 250
        tumbler_mouth_up_open[2] = 250
        if self.move == 'close':
            DR.movej(pos=self.tumbler_pose["origin"]["joint"],vel = VELOCITY, acc = ACCURACY)
            self.release(self.grasp_option)
            print(tumbler_cover_up)
            DR.movel(pos=tumbler_cover_up,vel=VELOCITY, acc = ACCURACY) #pos
            DR.movel(pos=self.tumbler_pose["cover_top"]["task"],vel=VELOCITY, acc = ACCURACY) #pos
            self.grasp(self.grasp_option)
            DR.movel(pos=tumbler_cover_up,vel=VELOCITY, acc = ACCURACY) #pos
            DR.movel(pos=tumbler_mouth_up,vel=VELOCITY,acc=ACCURACY)
            DR.movel(pos=self.tumbler_pose["mouth_close"]["task"],vel = VELOCITY,acc = ACCURACY) #pos
            print('spin')
            self.spin()
            print('stop spin')
            self.release(self.grasp_option)
            DR.movel(pos=tumbler_mouth_up,vel=VELOCITY,acc=ACCURACY)
            DR.movej(pos=self.tumbler_pose["origin"]["joint"],vel = VELOCITY, acc = ACCURACY)
        elif self.move == 'open':
            DR.movej(pos=self.tumbler_pose["origin"]["joint"],vel = VELOCITY, acc = ACCURACY)
            self.release(self.grasp_option)
            DR.movel(pos=tumbler_mouth_up_open,vel=VELOCITY,acc=ACCURACY)
            DR.movel(pos=self.tumbler_pose["mouth_before_open"]["task"],vel = VELOCITY,acc = ACCURACY) #poss
            DR.movel(pos=self.tumbler_pose["mouth_open"]["task"],vel = VELOCITY,acc = ACCURACY) #poss
            self.grasp(self.grasp_option)
            print('start respin')
            self.respin()
            print('stop respin')
            DR.movel(pos=tumbler_mouth_up_open,vel=VELOCITY,acc=ACCURACY)
            DR.movel(pos=tumbler_cover_up,vel=VELOCITY, acc = ACCURACY) #pos
            DR.movel(pos=self.tumbler_pose["cover_top"]["task"],vel=VELOCITY, acc = ACCURACY) #pos
            self.release(self.grasp_option)
            DR.movej(pos=self.tumbler_pose["origin"]["joint"],vel = VELOCITY, acc = ACCURACY)
            self.release(self.grasp_option)

        else:
            raise KeyError("이 키는 존재하지 않습니다!")
        
    
    def grasp(self, x):
        self._set_custom_grasp(x)
        DR.set_digital_output(1, ON)
        time.sleep(0.5)

    def spin(self):
        DR.task_compliance_ctrl([5,5,500,100,100,100])
        time.sleep(0.1)
        DR.set_desired_force([0,0,-15,0,0,0],dir=[0,0,1,0,0,0])
        while True: # first
            if DR.check_force_condition(DR.DR_AXIS_Z,max=10):
                break
            time.sleep(0.1)
            
        current_joint = DR.get_current_posj()
        for i in range(12):
            current_joint[5] += 30
            DR.movej(current_joint , vel = 30, acc =30)
            print(i)
        DR.release_force()
        time.sleep(0.1)
        DR.release_compliance_ctrl()
        time.sleep(0.1)

    def respin(self):
        DR.task_compliance_ctrl([5,5,500,100,100,100])
        time.sleep(0.1)
        DR.set_desired_force([0,0,15,0,0,0],dir=[0,0,1,0,0,0])
        current_joint = DR.get_current_posj()
        for i in range(11):
            current_joint[5] -= 30
            DR.movej(current_joint , vel = 30, acc =30)
            print(i)
        DR.release_force()
        time.sleep(0.1)
        DR.release_compliance_ctrl()
        time.sleep(0.1)

    def release(self, x):
        self._set_custom_grasp(x)
        DR.set_digital_output(1, OFF)
        time.sleep(0.5)

    def _set_custom_grasp(self, x):
        if x == 0:
            DR.set_digital_output(2, OFF)
        elif x == 1:
            DR.set_digital_output(2, ON)
