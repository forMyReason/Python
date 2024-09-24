# HEADER   :
#   File     :   folder_mat.py
#   Create   :   2024/09/07
#   Author   :   LiDanyang 
#   Branch   :   develop
#   Descript :   替换迁移材质引用


# UPDATE: 2024/9/12 16:24 -> 完成所有材质修改，包含所有工位/AO下SM的材质实例的迁移，以及材质实例的父级材质的迁移

# 我发现如果当前路径下static mesh 的 同名文件夹时，使用list_assets获取文件夹中的所有asset的路径时，会优先获取static mesh
# 所以我先删除AO，之后重新生成
# 1. 选中一堆文件夹，先将选中文件夹下面所有static mesh的材质迁移到指定文件夹下
# 2. 之后再将选中文件夹下面所有材质实例的父级材质迁移到指定文件夹下


import unreal

def get_assets_name_list(folder_path, asset_type):
    assets_list = []
    assets_name_list = []

    assets_path = unreal.EditorAssetLibrary().list_assets(folder_path, recursive=True, include_folder=False)
    for asset_path in assets_path:
        asset = unreal.EditorAssetLibrary.load_asset(asset_path.split('.')[0])
        if asset and isinstance(asset, asset_type):
            assets_list.append(asset)
    if assets_list:
        assets_name_list = [asset.get_name() for asset in assets_list]
    else:
        assets_name_list = []
    return assets_name_list

# TODO：目标材质文件夹，材质迁移的位置
# 上飞厂材质文件夹
mat_folder_path = r'/Game/ARJ_Model/_Materials/'
mat_parent_folder_path = r'/Game/ARJ_Model/_Materials/Reference/'

# 供应商材质文件夹
# mat_folder_path = r'/Game/ARJ_Model_GYS/_Materials/'
# mat_parent_folder_path = r'/Game/ARJ_Model_GYS/_Materials/Reference/'

# 测试材质文件夹
# mat_folder_path = r'/Game/Atesttset/_Materials/'
# mat_parent_folder_path = r'/Game/Atesttset/_Materials/Reference/'

# # 1. 选中一堆文件夹，先将选中文件夹下面所有static mesh的材质迁移到指定文件夹下
# selected_folder_paths = unreal.EditorUtilityLibrary.get_selected_folder_paths()
#
# for active_folder_path in selected_folder_paths:
#     assets_path = unreal.EditorAssetLibrary().list_assets(active_folder_path, recursive=True, include_folder=False)
#
#     # 迁移材质
#     for asset_path in assets_path:      # 文件夹下面每一个asset的path
#         # load asset into memory
#         asset = unreal.EditorAssetLibrary.load_asset(asset_path)
#
#         if asset and isinstance(asset, unreal.StaticMesh):
#             static_materials = asset.static_materials        # 获取当前资产使用到的所有材质[list]
#
#             # for item in static_materials:
#             #     print(item.material_slot_name)                                  # 2960641
#             #     print(item.material_interface)                                  # <Object '/Game/3dxml/ATA32-1/Materials/color_d2d2ffff.color_d2d2ffff' (0x0000053D20686200) Class 'MaterialInstanceConstant'>
#             #     print(item.material_interface.get_path_name())                  # /Game/3dxml/ATA32-1/Materials/color_d2d2ffff.color_d2d2ffff
#             #     print(item.material_interface.get_name())                       # color_d2d2ffff
#             #     print(item.material_interface.get_class())                      # <Object '/Script/Engine.MaterialInstanceConstant' (0x0000053C6B7B2800) Class 'Class'>
#             #     print(item.material_interface.get_class().get_name())           # MaterialInstanceConstant
#             #     print(item.material_interface.get_class().get_path_name())      # /Script/Engine.MaterialInstanceConstant
#             mat_instance_name_list = get_assets_name_list(mat_folder_path,unreal.MaterialInstance)
#
#             for i in range(len(static_materials)):
#                 current_name = static_materials[i].material_interface.get_name()
#                 current_path_name = static_materials[i].material_interface.get_path_name()
#                 current_slot_name = static_materials[i].material_slot_name
#                 if current_name in mat_instance_name_list:
#                     unreal.log(f"Already in Taget Folder : {asset.get_name()} : {current_slot_name} : {current_name}")
#                 else:
#                     unreal.log(f"Not in Taget Folder : {asset.get_name()} : {current_slot_name} : {current_name}")
#                     # BUG: 会报错，因为此时 mat_instance_name_list 没有更新
#                     duplicate_material = unreal.EditorAssetLibrary.duplicate_asset(current_path_name, mat_folder_path + current_name)
#                     unreal.log(f"{duplicate_material} is duplicated to {mat_folder_path + current_name}")
#
#                 new_material = unreal.EditorAssetLibrary.load_asset(mat_folder_path + current_name)
#                 asset.set_material(i, new_material)
#     unreal.SystemLibrary.collect_garbage()
#     unreal.EditorAssetSubsystem().save_directory('/Game/',only_if_is_dirty=True,recursive=True)

# 2. 之后再将选中文件夹下面所有材质实例的父级材质迁移到指定文件夹下
# 当前文件夹下所有的材质实例 asset path
mat_instance_path_list = unreal.EditorAssetLibrary.list_assets(mat_folder_path, recursive=True, include_folder=False)       # /Game/ARJ_Model_GYS/_Materials/color_f3feb1ff.color_f3feb1ff
mat_instace_name_list = get_assets_name_list(mat_folder_path, unreal.MaterialInstance)      # color_0000ffff

mat_parent_path_list = unreal.EditorAssetLibrary.list_assets(mat_parent_folder_path, recursive=True, include_folder=False)

for item in mat_instance_path_list:
    mat_parent_name_list = get_assets_name_list(mat_parent_folder_path , unreal.Material)           # M_DatasmithCAD，M_DatasmithCADTransparent

    mat = unreal.EditorAssetLibrary.load_asset(item.split('.')[0])          # mat_instance
    assetData_matIns = unreal.EditorAssetLibrary.find_asset_data(mat.get_path_name()).get_asset()
    # print(mat.get_name())
    # print(mat.get_path_name())
    if isinstance(mat, unreal.MaterialInstance):
        mat_parent = mat.parent
        if isinstance(mat_parent, unreal.Material):                         # M_DatasmithCAD，M_DatasmithCADTransparent
            if mat_parent.get_name() not in mat_parent_name_list:
                # 如果父材质不在目标文件夹中，则复制
                duplicate_material = unreal.EditorAssetLibrary().duplicate_asset(mat_parent.get_path_name(), mat_parent_folder_path + str(mat_parent.get_name()))
                assetData_matParent = unreal.EditorAssetLibrary.find_asset_data(duplicate_material.get_path_name())
                _MatInstance = assetData_matParent.get_asset()
                # _MatInstance = unreal.MaterialInstance.cast(assetData_matParent.get_asset())
                unreal.MaterialEditingLibrary().set_material_instance_parent(assetData_matIns, _MatInstance)
            else:
                unreal.log(f"Already in {mat_parent_folder_path} : {mat_parent.get_name()}")
                existing_material = unreal.EditorAssetLibrary.load_asset(mat_parent_folder_path + str(mat_parent.get_name()))
                assetData_matParent = unreal.EditorAssetLibrary.find_asset_data(existing_material.get_path_name())
                # _MatInstance = unreal.MaterialInstance.cast(assetData_matParent.get_asset())
                _MatInstance = assetData_matParent.get_asset()
                unreal.MaterialEditingLibrary().set_material_instance_parent(assetData_matIns, _MatInstance)
        else:
            unreal.log_warning(f"{mat.get_name()} has no parent material.")
unreal.get_editor_subsystem(unreal.EditorAssetSubsystem).save_directory(mat_folder_path , only_if_is_dirty=False , recursive=True)
