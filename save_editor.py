# HEADER   :
#   File     :   BaseProcess.py
#   Create   :   2024/09/06
#   Author   :   LiDanyang 
#   Branch   :   develop
#   Descript :   unreal 基本的保存逻辑

import unreal

unreal.EditorAssetSubsystem().save_directory('/Game/3dxml/',only_if_is_dirty=True,recursive=True)

def toggle_actors_visibility(hide):
    world = unreal.EditorLevelLibrary.get_editor_world()
    all_actors = unreal.GameplayStatics.get_all_actors(world, unreal.Actor)
    for actor in all_actors:
        actor.set_actor_hidden_in_game(hide)
