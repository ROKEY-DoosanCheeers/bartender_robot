import rclpy
from rclpy.node import Node
import DR_init
import os, yaml

from .shaker.shaker_action import ShakerAction
from .shaker.shaker_pour import PourAction    
from .stir_and_garnish.stir import StirAction
from .stir_and_garnish.garnish import GarnishAction
from ament_index_python.packages import get_package_share_directory
from .pour.pour import PourAction

POSE_PATH = os.path.join(
    get_package_share_directory("cocktail_robot"),
    "pose.yaml"
)

ROBOT_ID = "dsr01" # for rviz
# ROBOT_ID = "" # for moveit
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

def load_yaml(POSE_PATH):
    with open(POSE_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

def get_recipes(node, poses):
    return {
        'Margarita': [
            PourAction(node, ingredient="tequila", amount=50, target="shaker", pour_pose=poses["pour"]),
            PourAction(node, ingredient="blue_juice", amount=20, target="shaker", pour_pose=poses["pour"]),
            # ShakeAction(arm, pose="shake_zone", cycles=7),
            PourAction(node, ingredient="shaker_", amount=80, target="glass", pour_pose=poses["pour"])
            # GarnishAction(arm, poses["garnish"]),
            # PlateAction(arm),
        ],
        'China Red': [
            PourAction(node, ingredient="tequila", amount=50, target="glass", pour_pose=poses["pour"]),
            PourAction(node, ingredient="red_juice", amount=30, target="glass", pour_pose=poses["pour"]),
            # GarnishAction(arm, poses["garnish"]),
            # PlateAction(arm)
        ],
        'test': [
            TumblerAction(node, poses['tumbler'],'open'),
        ]
    }


def main():
    rclpy.init()
    node = rclpy.create_node("main", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            set_tool,
            set_tcp,
            set_ref_coord,
            DR_BASE
        )

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return
    
    set_tool("GripperDA_v2")
    set_tcp("Tool Weighttest")
    set_ref_coord(DR_BASE)

    try:
        from DSR_ROBOT2 import (
            set_tool,
            set_tcp,
            set_ref_coord,
            DR_BASE
        )

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    set_tool("GripperDA_v2")
    set_tcp("Tool Weighttest")
    set_ref_coord(DR_BASE)

    poses = load_yaml(POSE_PATH)
    recipes = get_recipes(node, poses)
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
