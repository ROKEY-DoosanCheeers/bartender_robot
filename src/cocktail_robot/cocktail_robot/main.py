import rclpy
from rclpy.node import Node
import DR_init
import os, yaml
import numpy as np

from .pour.pour import PourAction
from .shaker.shaker import ShakerAction
from .stir_and_garnish.stir import StirAction
from .stir_and_garnish.garnish import GarnishAction
from .tumbler.tumbler import TumblerAction
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
            PourAction(node, poses=poses["pour"], ingredient="tequila", amount=50, target="shaker"), # tequila -> shaker
            PourAction(node, poses=poses["pour"], ingredient="blue_juice", amount=20, target="shaker"), # blue_juice -> shaker
            TumblerAction(node, poses=poses["tumbler"], move="close"), # close
            ShakerAction(node, poses=poses["shake"]), # shake
            TumblerAction(node, poses=poses["tumbler"], move="open"), # open
            PourAction(node, poses=poses["pour"], ingredient="shaker_", amount=80, target="glass"), # shaker -> glass
            GarnishAction(node, poses=poses["garnish"], topping="lime")
        ],
        'China Red': [
            PourAction(node, poses=poses["pour"], ingredient="tequila", amount=50, target="glass"),
            PourAction(node, poses=poses["pour"], ingredient="blue_juice", amount=30, target="glass"),
            StirAction(node, poses['stir']), # stir
            GarnishAction(node, poses=poses["garnish"], topping="cherry")
        ],
        'test': [
            # PourAction(node, ingredient="tequila", amount=50, target="shaker", pour_pose=poses["pour"]),
            # PourAction(node, ingredient="shaker_", amount=50, target="shaker_glass", pour_pose=poses["pour"])
            StirAction(node, poses['stir']), # stir
        ]
    }


def main():
    rclpy.init()
    node = rclpy.create_node("main", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            movej,
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
    recursive_check(poses)
    recipes = get_recipes(node, poses)
    print("가능한 칵테일:", list(recipes.keys()))

    cocktail = input("만들 칵테일을 입력하세요: ")
    if cocktail not in recipes:
        print("해당 레시피가 없습니다.")
        return

    print(f"\n[{cocktail}] 제조 시작!")
    
    movej(pos=[0,0,90,0,90,0], vel=VELOCITY*0.3, acc=ACC)
    for idx, action in enumerate(recipes[cocktail], 1):
        print(f'STEP {idx}. Started')
        action.execute()
    movej(pos=[0,0,90,0,90,0], vel=VELOCITY*0.3, acc=ACC)
    rclpy.shutdown()


def recursive_check(data_dict):
    if isinstance(data_dict, dict):
        for key, value in data_dict.items():
            recursive_check(value)
    elif isinstance(data_dict, list):
        if len(data_dict) == 6 and all(isinstance(v, (int, float)) for v in data_dict):
            arr = np.array(data_dict, dtype=np.float64)
            print(f"float64[6] OK: {arr}")
        elif len(data_dict) == 6:
            raise TypeError(f"6개인데 float/int 아님: {data_dict}")
        elif all(isinstance(v, (int, float)) for v in data_dict):
            raise IndexError(f"값 개수 오류 ({len(data_dict)}개): {data_dict}")
        else:
            raise TypeError(f"값 개수와 타입 모두 문제: {data_dict}")
            

if __name__ == "__main__":
    main()
