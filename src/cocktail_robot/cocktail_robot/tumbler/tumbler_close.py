from ..utils.base_action import BaseAction
import DR_init
import time
#from ..utils.base_action import BaseAction
VELOCITY, ACCURACY = 100,60
ON, OFF = 1, 0
DR = None
class TumblerAction(BaseAction):
    def __init__(self,node, tumbler_pose):     # pose_dict로 location.yaml 파일을 불러옴
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
        DR.movej(pos=self.tumbler_pose["origin"]["joint"],vel = VELOCITY, acc = ACCURACY)
        self.release(self.grasp_option)
        DR.movej(pos=self.tumbler_pose["cover_top"]["joint"],vel=VELOCITY, acc = ACCURACY)
        self.grasp(self.grasp_option)
        DR.movej(pos=self.tumbler_pose["mouth_top"]["joint"],vel = VELOCITY,acc = ACCURACY)
        self.spin()
        DR.movej(pos=self.tumbler_pose["origin"]["joint"],vel = VELOCITY, acc = ACCURACY)
        
    
    def grasp(self, x):
        self._set_custom_grasp(x)
        self.set_digital_output(1, ON)
        time.sleep(0.5)

    def spin(self,force = 5, angle =270, period = 2.0, atime =1.0, force_check = 10):
        # center = DR.get_current_pose()
        fd = [0,0,force,0,0,0]
        fdir = [0,0,1,0,0,0]
        DR.task_compliance_ctrl([5,5,3000,200,200,200])
        DR.set_desired_force(fd,dir =fdir, mod=DR.DR_FC_MOD_REL)
        amp = [0.0, 0.0, 0.0, 0.0, 0.0, angle]  # Z회전r
        period_vals = [0.0, 0.0, 0.0, 0.0, 0.0, period]
        repeat = 1
        reference = self.DR_BASE
        DR.amove_periodic(amp, period_vals, atime, repeat, ref=reference)
        try:
            while True:
                # current_force = DR.check_force_condition()
                # z_force = current_force[5]
                if DR.check_force_condition(DR.DR_AXIS_Z,max = force_check):
                    print(f"force ")
                    break
                time.sleep(0.5)
        finally:
            DR.amove_periodic_stop()
            DR.release_force
            DR.release_compliance_ctrl()
            DR.release()
        # DR.set_desired_force([0,0,-10,0,0,10],[0,0,1,0,0,1],time=0.5,mod=DR.DR_FC_MOD_REL)
        # while not DR.check_force_condition(DR.DR_AXIS_Z,max=force_check):
        #     # DR.amovel(pos=[0,0,0,0,0,10],vel=VELOCITY,acc=ACCURACY,ref=DR.DR_MV_MOD_REL)
        #     DR.wait(0.5)

    def release(self, x):
        self._set_custom_grasp(x)
        self.set_digital_output(1, OFF)
        time.sleep(0.5)

    def _set_custom_grasp(self, x):
        if x == 0:
            self.set_digital_output(2, OFF)
        elif x == 1:
            self.set_digital_output(2, ON)
