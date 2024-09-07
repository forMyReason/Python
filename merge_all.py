##################################################
# HEADER   :
#   File     :   merge_all.py
#   Create   :   2024/09/02
#   Author   :   LiDanyang 
#   Branch   :   lession
#   Descript :   合并某路径下的所有asset

# UPDATE  :
#   Last Edit  :   2024/09/02 14:34:03
#   Status     :   GiveUp
##################################################

import unreal
import os

folder_path = r"/Game/ARJ_Model/221/221A403AD0120/"

merge_path = r"/Game/ARJ_Model/221/"
merge_name = folder_path.split('/')[-2]
print(merge_path)
print(merge_name)

static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets_data = asset_registry.get_assets_by_path(folder_path, recursive=False)        # 返回struct，assetdata
# assets_path = unreal.EditorAssetLibrary.list_assets(folder_path, recursive=True, include_folder=False)       # 返回str，所有asset的相对路径

static_mesh_assets = []

for asset in assets_data:
    print(asset.get_asset())
    if isinstance(asset.get_asset(),unreal.StaticMesh):
        static_mesh_assets.append(asset)
        unreal.load_asset(asset.package_path)

# load进内存之后，是不是就相当于已经是actor了？就可以考虑merge了？

if not static_mesh_assets:
    print(f"No static meshes found in folder: {folder_path}")
else:
    merge_setting = unreal.MeshMergingSettings()
    merge_setting.pivot_point_at_zero = True

    asset_path = os.path.join(merge_path , merge_name)
    merge_options = unreal.MergeStaticMeshActorsOptions(
        base_package_name = asset_path,
        mesh_merging_settings = merge_setting
    )
    merged_asset = static_mesh_lib.merge_static_mesh_actors(static_mesh_assets , merge_options)

    if merged_asset:
        print(f"Merged Static Mesh created at: {package_path}")
    else:
        print("Failed to merge static meshes.")