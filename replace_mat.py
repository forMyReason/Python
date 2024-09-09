# 一键替换材质
import unreal

selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
static_mesh_assets = unreal.EditorFilterLibrary.by_class(selected_assets, unreal.StaticMesh)

if static_mesh_assets:
    for static_mesh_asset in static_mesh_assets:
        static_materials = static_mesh_asset.static_materials
        # print(f"The {static_mesh_asset.get_name()} has {len(static_materials)} meterials")
        # for material in static_materials:
        #     print(f'-{material.material_slot_name}')
        
        for i in range(len(static_materials)):
            # 修改材质
            material_path = r"/Game/Python/MI_red"
            red_material = unreal.EditorAssetLibrary.load_asset(material_path)
            static_mesh_asset.set_material(i, red_material)

            # Game/StarterContent/Materials/M_Basic_Wall