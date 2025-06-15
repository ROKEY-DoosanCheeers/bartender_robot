import rclpy
from rclpy.node import Node
import DR_init
from robot_arm import RobotArm
from robot_actions.garnish import GarnishAction
# 여기에 import할 각 모듈 파일과 클래스명 추가. 동작별 import

def get_recipes(arm):
    return {
        'Margarita': [
            # PourAction(arm, "tequila", 50, pose="pour_tequila"),
            # PourAction(arm, "blue_juice", 20, pose="pour_blue"),
            # ShakeAction(arm, pose="shake_zone", cycles=7),
            GarnishAction(arm, "lime"),
            # PlateAction(arm)
        ],
        'China Red': [
            # PourAction(arm, "tequila", 50, pose="pour_tequila"),
            # PourAction(arm, "red_juice", 30, pose="pour_red"),
            # ShakeAction(arm, pose="shake_zone", cycles=5),
            GarnishAction(arm, "cherry"),
            # PlateAction(arm)
        ]
    }

def main():
    rclpy.init()
    arm = RobotArm()  
    recipes = get_recipes(arm)
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
