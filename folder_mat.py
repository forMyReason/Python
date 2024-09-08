# HEADER   :
#   File     :   folder_mat.py
#   Create   :   2024/09/07
#   Author   :   LiDanyang 
#   Branch   :   develop
#   Descript :   替换迁移材质引用

import unreal

# 放asset的文件夹路径
selected_folder_paths = unreal.EditorUtilityLibrary.get_selected_folder_paths()
active_folder_path = selected_folder_paths[0]

# 文件夹下面所有asset
assets_path = unreal.EditorAssetLibrary.list_assets(active_folder_path, recursive=True, include_folder=False)

# 目标材质文件夹
mat_folder_path = "/Game/Temp_Material/"
mat_instance_list = unreal.EditorAssetLibrary.list_assets(mat_folder_path, recursive=True, include_folder=False)

if mat_instance_list:
    mat_instance_name_list = [mat.split('.')[-1] for mat in mat_instance_list]
else:
    mat_instance_name_list = []

# 是否在当前路径下
# 两种方式：
# 比较命名
# 比较路径


# 迁移材质
for asset_path in assets_path:
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    # print(f"Loaded asset: {asset_path}")

    if asset:
        # 获取当前资产的材质
        static_materials = asset.static_materials
        # print(f"The {asset.get_name()} has {len(static_materials)} meterials")
        # for material in static_materials:
        #     print(f'-{material.material_slot_name}')

        for i in range(len(static_materials)):
            if static_materials[i].material_slot_name in mat_instance_name_list:          # 判断材质是否在指定路径
                # unreal.log(f"Already in Taget Folder : {asset.get_name()} : {static_materials[i].material_slot_name}")
                continue
            else:
                # print(static_materials[i].material_slot_name)                         # 材质名称
                # print(static_materials[i].material_interface)                         # 材质接口，返回Object
                # print(static_materials[i].material_interface.get_path_name())         # 获取当前材质路径
                # print(mat_folder_path + str(static_materials[i].material_slot_name))         # 目标路径

                unreal.log_warning(f"Not in Taget Folder : {static_materials[i].material_slot_name}")
                duplicate_material = unreal.EditorAssetLibrary.duplicate_asset(static_materials[i].material_interface.get_path_name(), mat_folder_path + str(static_materials[i].material_slot_name))
                unreal.log_warning(f"{duplicate_material} is duplicated to {mat_folder_path + str(static_materials[i].material_slot_name)}")

        unreal.SystemLibrary.collect_garbage()

# 迁移所有材质的父级材质
mat_parent_folder_path = "/Game/Temp_Material/Master/"
mat_parent_path_list = unreal.EditorAssetLibrary.list_assets(mat_parent_folder_path, recursive=True, include_folder=False)

for target_mat in mat_instance_list:
    mat = unreal.EditorAssetLibrary.load_asset(target_mat)
    # print(mat)                              # 返回object
    # print(mat.get_class().get_name())       # 返回材质类型
    
    # 继承关系如下
    # Material-> 
    # MaterialInstance -> 
    # MaterialInstanceConstant / MaterialInstanceDynamic
    # 所有这几个都是继承自MaterialInstance

    if mat.get_class().get_name() == "MaterialInstanceConstant":
        mat_parent = mat.parent                 # 获取父级材质
        # print(mat_parent.get_path_name())     # 获取父级材质路径：/Game/LevelPrototyping/Materials/M_Solid.M_Solid
        # print(mat_parent.get_name())          # 获取父级材质名称：M_Solid

        if mat_parent:
            if mat_parent.get_path_name() not in mat_parent_path_list:
                duplicate_material = unreal.EditorAssetLibrary.duplicate_asset(mat_parent.get_path_name(), mat_parent_folder_path + str(mat_parent.get_name()))
                unreal.log_warning(f"{duplicate_material} is duplicated to {mat_folder_path + str(mat_parent.get_name())}")
unreal.SystemLibrary.collect_garbage()

# material_slot_names = unreal.StaticMeshComponent.get_material_slot_names (static_mesh_component)

unreal.EditorAssetSubsystem().save_directory('/Game/',only_if_is_dirty=True,recursive=True)