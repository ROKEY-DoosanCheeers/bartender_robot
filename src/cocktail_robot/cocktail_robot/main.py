import threading
import time
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
from .bartender_gui import BartenderGUI

POSE_PATH = os.path.join(
    get_package_share_directory("cocktail_robot"),
    "pose.yaml"
)

ROBOT_ID = "dsr01"
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
            PourAction(node, ingredient="shaker_", amount=80, target="glass", pour_pose=poses["pour"]),
            GarnishAction(node, poses=poses["garnish"], topping="lime"),
            # PlateAction(arm),
        ],
        'China Red': [
            PourAction(node, ingredient="tequila", amount=50, target="glass", pour_pose=poses["pour"]),
            PourAction(node, ingredient="red_juice", amount=30, target="glass", pour_pose=poses["pour"]),
            # GarnishAction(arm, poses["garnish"]),
            # PlateAction(arm)
        ],
        'test': [
            PourAction(node, ingredient="tequila", amount=50, target="shaker", pour_pose=poses["pour"]),
            PourAction(node, ingredient="shaker_", amount=50, target="shaker_glass", pour_pose=poses["pour"])
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

    poses = load_yaml(POSE_PATH)
    recipes = get_recipes(node, poses)
    gui_recipes = ['표지'] + list(recipes.keys())

    # ================== 동작 관리 ==================
    stop_flag = threading.Event()
    action_thread = None

    def robot_action_callback(recipe_name):
        nonlocal action_thread
        if recipe_name == "STOP":
            app.set_status_msg("중단 요청!")
            stop_flag.set()
            return

        if action_thread and action_thread.is_alive():
            app.set_status_msg("이미 동작중! 중단 후 재실행하세요.")
            return

        def run_actions():
            app.set_status_msg(f"[{recipe_name}] 제조 시작!")
            stop_flag.clear()
            for idx, action in enumerate(recipes[recipe_name], 1):
                if stop_flag.is_set():
                    app.set_status_msg(f"[{recipe_name}] → 동작 중단됨!")
                    
                    break
                ing = getattr(action, 'ingredient', '-')
                stepname = action.__class__.__name__
                app.set_status_msg(f" - Step {idx}: [{ing}] [{stepname}] 실행 중.")
                action.execute()
                time.sleep(0.2)
            else:
                app.set_status_msg(f"[{recipe_name}] 제조 완료!")
        action_thread = threading.Thread(target=run_actions, daemon=True)
        action_thread.start()

    app = BartenderGUI(gui_recipes, recipes, robot_action_callback=robot_action_callback)
    app.mainloop()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
