# 材质的相关操作
# 1. 一键批量替换材质
import unreal

assets_path = unreal.EditorAssetLibrary.list_assets('/Game/StaticMeshes', True, False)
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

static_mesh_assets = unreal.EditorFilterLibrary.by_class(selected_assets, unreal.StaticMesh)

if static_mesh_assets:
    for static_mesh_asset in static_mesh_assets:
        static_materials = static_mesh_asset.static_materials
        # print(f"The {static_mesh_asset.get_name()} has {len(static_materials)} meterials")
        # for material in static_materials:
        #     print(f'-{material.material_slot_name}')
        
        for i in range(len(static_materials)):
            material_path = r"/Game/Python/MI_red"
            red_material = unreal.EditorAssetLibrary.load_asset(material_path)
            static_mesh_asset.set_material(i, red_material)
            
            # TODO：这个不知道是啥？
            # static_mesh_component.set_material(materials.index(material), new_material)