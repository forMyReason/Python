import unreal

# # 一键修改当前资产材质
# selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
# static_mesh_assets = unreal.EditorFilterLibrary.by_class(selected_assets, unreal.StaticMesh)
#
# if static_mesh_assets:
#     for static_mesh_asset in static_mesh_assets:
#         static_materials = static_mesh_asset.static_materials
#         # print(f"The {static_mesh_asset.get_name()} has {len(static_materials)} meterials")
#         # for material in static_materials:
#         #     print(f'-{material.material_slot_name}')
#
#         for i in range(len(static_materials)):
#             # 修改材质
#             material_path = r"/Game/Python/MI_red"
#             red_material = unreal.EditorAssetLibrary.load_asset(material_path)
#             static_mesh_asset.set_material(i, red_material)
#
#             # Game/StarterContent/Materials/M_Basic_Wall


# def replace_material(original, replacement):
#     original_asset = unreal.EditorAssetLibrary.load_asset(original)
#     replacement_asset = unreal.EditorAssetLibrary.load_asset(replacement)
#     unreal.EditorAssetLibrary.consolidate_assets(
#         replacement_asset, [original_asset])
#
# replace_material(
#     '/Game/MyProject/Materials/Glass',
#     '/Game/AdvancedGlassPack/Materials/01_Clean/M_Glass_CleanMaster_Inst'
# )


# 修改材质实例的父材质
def change_material_instance_parent(material_instance_path, new_parent_path):
    # 加载材质实例和新的父材质
    material_instance = unreal.EditorAssetLibrary.load_asset(material_instance_path)
    new_parent = unreal.EditorAssetLibrary.load_asset(new_parent_path)

    # 确保加载成功，并且两个都是材质类型
    if isinstance(material_instance, unreal.MaterialInstance) and (isinstance(new_parent, unreal.Material) or isinstance(new_parent, unreal.MaterialInstance)):
        # 设置材质实例的父材质
        unreal.MaterialEditingLibrary.set_material_instance_parent(material_instance, new_parent)
        print(f"Changed parent of {material_instance_path} to {new_parent_path}")
    else:
        print("Error: Invalid material instance or new parent material.")

# 使用示例
# change_material_instance_parent('/Game/Python/MI_red',
#                                 '/Game/Python/M_Color')
#


assetData_matIns = unreal.EditorAssetLibrary.find_asset_data(mat.get_path_name()).get_asset()
duplicate_material = unreal.EditorAssetLibrary().duplicate_asset(mat_parent.get_path_name(),
                                                                 mat_parent_folder_path + str(mat_parent.get_name()))
assetData_matParent = unreal.EditorAssetLibrary.find_asset_data(duplicate_material.get_path_name()).get_asset()
assetData_matIns.set_editor_property('Parent', assetData_matParent)