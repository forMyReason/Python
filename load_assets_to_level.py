##################################################
# HEADER   :
#   File     :   load_assets_to_level.py
#   Create   :   2024/09/02
#   Author   :   LiDanyang 
#   Branch   :   lession
#   Descript :   将指定模型加载到场景中

# UPDATE  :
#   Last Edit  :   2024/09/02 15:23:18
#   Status     :   Need Review
##################################################

import unreal

## 1. 通过指定路径加载模型
# asset_path = "/Game/ARJ_Model/140/140A104BB0300_01/S4648A050_1_1__body1_4"

## 2. 加载所有选中模型
# selectionAssets = unreal.EditorUtilityLibrary().get_selected_assets()
# asset_paths = [item.get_path_name() for item in selectionAssets]

# # 3. 加载指定文件夹下所有模型
# path = "/Game/ARJ_Model/140/140A104BB0300_01/"
# asset_paths = unreal.EditorAssetLibrary.list_assets(path, recursive=True, include_folder=False)

# for asset_path in asset_paths:
#     print(asset_path)

for asset_path in asset_paths:
    # load asset into memory
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)

    if asset:
        if isinstance(asset, unreal.StaticMesh):
            actor = unreal.EditorActorSubsystem().spawn_actor_from_object(asset, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
        elif isinstance(asset, unreal.Blueprint):
            actor = unreal.EditorActorSubsystem.spawn_actor_from_class(asset.GeneratedClass, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
        else:
            # Handle other asset types if needed
            actor = None
        
        if actor:
            unreal.log("Asset successfully placed in the scene.")
        else:
            unreal.log_warning("Asset type is not supported for direct placement in the scene.")
    else:
        unreal.log_error("Failed to load asset. Please check the asset path.")