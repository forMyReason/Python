# HEADER   :
#   File     :   folder_mat.py
#   Create   :   2024/09/07
#   Author   :   LiDanyang 
#   Branch   :   develop
#   Descript :   替换迁移材质引用

import unreal

# 我发现如果当前路径下static mesh 的 同名文件夹时，使用list_assets获取文件夹中的所有asset的路径时，会优先获取static mesh
# 所以我先删除AO，之后重新生成

# 放asset的文件夹路径
selected_folder_paths = unreal.EditorUtilityLibrary.get_selected_folder_paths()
# for selected_folder_path in selected_folder_paths:
#     print(selected_folder_path)


for active_folder_path in selected_folder_paths:

    # active_folder_path = selected_folder_paths[0]       # /Game/ARJ_Model/212/212A103HA0040
    # print(active_folder_path)

    # 文件夹下面所有asset
    # 在使用之前需要 convert_relative_path_to_full
    # asset_path = unreal.EditorAssetLibrary().list_assets(active_folder_path, recursive=True, include_folder=False)
    assets_path = unreal.EditorAssetLibrary().list_assets(active_folder_path, recursive=True, include_folder=False)
    # for asset_path in assets_path:
    #     print(asset_path)

    # 目标材质文件夹，材质迁移的位置
    mat_folder_path = "/Game/ARJ_Model/_Materials/"


    def get_material_instance_name_list(mat_folder_path):
        # 获取文件夹下的所有材质路径，string 类型
        mat_instance_list = unreal.EditorAssetLibrary().list_assets(mat_folder_path, recursive=True, include_folder=False)
        if mat_instance_list:
            mat_instance_name_list = [mat.split('.')[-1] for mat in mat_instance_list]
        else:
            mat_instance_name_list = []

        # for item in mat_instance_name_list:
        #     print(item)
        return mat_instance_name_list


    # 是否在当前路径下
    # 两种方式：
    # 比较命名
    # 比较slot name
    # 比较路径

    ####### 迁移材质

    # print 当前路径下所有asset 的每个材质信息
    for asset_path in assets_path:      # 文件夹下面每一个asset的path
        # load asset into memory
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)

        if asset and isinstance(asset, unreal.StaticMesh):
            static_materials = asset.static_materials        # 获取当前资产使用到的所有材质[list]
            # print(f"The {asset.get_name()} has {len(static_materials)} meterials")
            # for material in static_materials:
            #     print(f'{material.material_slot_name}')

            # for item in static_materials:
            #     print(item.material_slot_name)                                  # 2960641
            #     print(item.material_interface)                                  # <Object '/Game/3dxml/ATA32-1/Materials/color_d2d2ffff.color_d2d2ffff' (0x0000053D20686200) Class 'MaterialInstanceConstant'>
            #     print(item.material_interface.get_path_name())                  # /Game/3dxml/ATA32-1/Materials/color_d2d2ffff.color_d2d2ffff
            #     print(item.material_interface.get_name())                       # color_d2d2ffff
            #     print(item.material_interface.get_class())                      # <Object '/Script/Engine.MaterialInstanceConstant' (0x0000053C6B7B2800) Class 'Class'>
            #     print(item.material_interface.get_class().get_name())           # MaterialInstanceConstant
            #     print(item.material_interface.get_class().get_path_name())      # /Script/Engine.MaterialInstanceConstant
            mat_instance_name_list = get_material_instance_name_list(mat_folder_path)

            for i in range(len(static_materials)):
                current_name = static_materials[i].material_interface.get_name()
                current_path_name = static_materials[i].material_interface.get_path_name()
                current_slot_name = static_materials[i].material_slot_name
                if current_name in mat_instance_name_list:
                    unreal.log(f"Already in Taget Folder : {asset.get_name()} : {current_slot_name} : {current_name}")
                else:
                    unreal.log(f"Not in Taget Folder : {asset.get_name()} : {current_slot_name} : {current_name}")
                    # BUG: 会报错，因为此时 mat_instance_name_list 没有更新
                    duplicate_material = unreal.EditorAssetLibrary.duplicate_asset(current_path_name, mat_folder_path + current_name)
                    unreal.log(f"{duplicate_material} is duplicated to {mat_folder_path + current_name}")

                new_material = unreal.EditorAssetLibrary.load_asset(mat_folder_path + current_name)
                asset.set_material(i, new_material)
        unreal.SystemLibrary.collect_garbage()
        unreal.EditorAssetSubsystem().save_directory('/Game/',only_if_is_dirty=True,recursive=True)


    # # 迁移所有材质的父级材质
    # mat_parent_folder_path = "/Game/Temp_Material/Master/"
    # mat_parent_path_list = unreal.EditorAssetLibrary.list_assets(mat_parent_folder_path, recursive=True, include_folder=False)
    #
    # for target_mat in mat_instance_list:
    # mat = unreal.EditorAssetLibrary.load_asset(target_mat)
    # # print(mat)                              # 返回object
    # # print(mat.get_class().get_name())       # 返回材质类型
    #
    # # 继承关系如下
    # # Material->
    # # MaterialInstance ->
    # # MaterialInstanceConstant / MaterialInstanceDynamic
    # # 所有这几个都是继承自MaterialInstance
    #
    # if mat.get_class().get_name() == "MaterialInstanceConstant":
    #     mat_parent = mat.parent                 # 获取父级材质
    #     # print(mat_parent.get_path_name())     # 获取父级材质路径：/Game/LevelPrototyping/Materials/M_Solid.M_Solid
    #     # print(mat_parent.get_name())          # 获取父级材质名称：M_Solid
    #
    #     if mat_parent:
    #         if mat_parent.get_path_name() not in mat_parent_path_list:
    #             duplicate_material = unreal.EditorAssetLibrary.duplicate_asset(mat_parent.get_path_name(), mat_parent_folder_path + str(mat_parent.get_name()))
    #             unreal.log_warning(f"{duplicate_material} is duplicated to {mat_folder_path + str(mat_parent.get_name())}")
    # unreal.SystemLibrary.collect_garbage()

