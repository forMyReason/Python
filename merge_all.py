import unreal
import os

# 合并某路径下的所有actor
# folder_path = "/Game/Python"
folder_path = "/Game/Temp_Fbx_Export"

output_path = "/Game/Temp_Fbx_Export/MergedMesh"
output_name = "MergedStaticMesh"

# TODO:Asset Registry
# Get the Asset Registry to find all assets in  the folder
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
# 获取asset data
assets = asset_registry.get_assets_by_path(folder_path, recursive=False)        # 是否迭代文件夹 assetData

static_mesh_assets = []

# asset.is_asset_loaded() 确保资产已经被load进内存中，才能执行操作

for asset in assets:
    if asset.get_class() == unreal.StaticMesh.static_class():
        if not asset.is_asset_loaded():
            unreal.load_asset(asset.get_full_name())        # get_name() 和 get_full_name()
        static_mesh_assets.append(asset)

if not static_mesh_assets:
    print(f"No static meshes found in folder: {folder_path}")
else:
    # for i in static_mesh_assets:
    #     print(i.asset_class)                # None
    #     print(i.asset_class_path)           # <Struct 'TopLevelAssetPath' (0x000008E80B50111C) {package_name: "/Script/Engine", asset_name: "StaticMesh"}>
    
    # Setup the mesh merging options
    merge_options = unreal.MeshMergingSettings()
    merge_options.pivot_point_at_zero=True

    # Specify where to save the merged static mesh
    merge_tool = unreal.MeshMergingTool()
    package_path = f"{output_path}/{output_name}"

    # Perform the mesh merge operation
    merged_asset = merge_tool.merge_static_mesh_actors(
        static_mesh_actors=static_meshes,
        mesh_merging_settings=merge_options,
        package_name=package_path,
        merge_mesh_data=None,
    )

    if merged_asset:
        print(f"Merged Static Mesh created at: {package_path}")
    else:
        print("Failed to merge static meshes.")