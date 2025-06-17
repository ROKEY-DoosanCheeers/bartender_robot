import rclpy
from rclpy.node import Node
import DR_init
import os, yaml
from src.cocktail_robot.cocktail_robot.utils.robot_arm import RobotArm
from .utils.garnish import GarnishAction
from .shaker.shaker_action import ShakerAction
from .shaker.shaker_pour import PourAction    

ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 30, 30

# DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL
ON, OFF = 1, 0
# 여기에 import할 각 모듈 파일과 클래스명 추가. 동작별 import

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSE_PATH = os.path.join(BASE_DIR, "locations/pose.yaml")

def load_yaml(POSE_PATH):
    with open(POSE_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

def get_recipes(arm, poses):
    return {
        'Margarita': [
            ShakerAction(arm,poses["shake"])
            # PourAction(arm, "tequila", 50, pose="pour_tequila"),
            # PourAction(arm, "blue_juice", 20, pose="pour_blue"),
            # ShakeAction(arm, pose="shake_zone", cycles=7),
            # GarnishAction(arm, "lime"),
            # PlateAction(arm)
        ],
        'China Red': [
            # PourAction(arm, "tequila", 50, pose="pour_tequila"),
            # PourAction(arm, "red_juice", 30, pose="pour_red"),
            # ShakeAction(arm, pose="shake_zone", cycles=5),
            # GarnishAction(arm, poses["garnish"]),
            # PlateAction(arm)
        ]
    }


def main(args=None):    
    rclpy.init(args=args)
    node = rclpy.create_node("force_control", namespace=ROBOT_ID)
    DR_init.__dsr__node = node
    try:
        import DSR_ROBOT2 as DR
    except ImportError as e:    
        print(f"Error importing DSR_ROBOT2: {e}")
    arm = RobotArm(DR)
    poses = load_yaml(POSE_PATH)
    recipes = get_recipes(arm, poses)
    print("가능한 칵테일:", list(recipes.keys()))

    cocktail = 'Margarita'
    if cocktail not in recipes:
        print("해당 레시피가 없습니다.")
        return

    print(f"\n[{cocktail}] 제조 시작!")
    for idx, action in enumerate(recipes[cocktail], 1):
        action.execute()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
