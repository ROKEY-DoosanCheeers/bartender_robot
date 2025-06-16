import rclpy
from rclpy.node import Node
import DR_init
import os, yaml
from src.cocktail_robot.cocktail_robot.utils.robot_arm import RobotArm
from utils.garnish import GarnishAction

from DR_common2 import posx, posj
# 여기에 import할 각 모듈 파일과 클래스명 추가. 동작별 import

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSE_PATH = os.path.join(BASE_DIR, "../locations/pose.yaml")

def load_yaml(POSE_PATH):
    with open(POSE_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    for v in data.values():
        if "task" in v:
            v["task"] = posx(v["task"])
        if "joint" in v:
            v["joint"] = posj(v["joint"])
    return data

def get_recipes(arm, poses):
    return {
        'Margarita': [
            # PourAction(arm, "tequila", 50, poses["pour_tequila"]),
            # PourAction(arm, "blue_juice", 20, poses["pour_tequila"]),
            # ShakeAction(arm, pose="shake_zone", cycles=7),
            GarnishAction(arm, poses["garnish"]),
            # PlateAction(arm)
        ],
        'China Red': [
            # PourAction(arm, "tequila", 50, pose="pour_tequila"),
            # PourAction(arm, "red_juice", 30, pose="pour_red"),
            # ShakeAction(arm, pose="shake_zone", cycles=5),
            GarnishAction(arm, poses["garnish"]),
            # PlateAction(arm)
        ]
    }


def main():
    rclpy.init()
    arm = RobotArm()
    poses = load_yaml(POSE_PATH)
    recipes = get_recipes(arm, poses)
    print("가능한 칵테일:", list(recipes.keys()))

    cocktail = input("만들 칵테일을 입력하세요: ")
    if cocktail not in recipes:
        print("해당 레시피가 없습니다.")
        return

    print(f"\n[{cocktail}] 제조 시작!")
    for idx, action in enumerate(recipes[cocktail], 1):
        action.execute()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
