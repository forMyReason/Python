# 本脚本主要用于合并当前选择文件夹下面的所有的static mesh asset

import unreal
import time

# 合并actor list
# TODO：需要整理merge相关操作
def MergeActors(actor_list , merge_name , save_path):
    try:
        setting = unreal.MeshMergingSettings()
        setting.pivot_point_at_zero = True
        setting.merge_materials = False

        merge_options = unreal.MergeStaticMeshActorsOptions(
            destroy_source_actors   =   True,
            spawn_merged_actor      =   False,
            mesh_merging_settings   =   setting
        )

        merge_options.base_package_name = save_path              # The package path you want to save to
        # /Game/ARJ_Model/130/130A103BB0030

        if unreal.EditorAssetLibrary().does_asset_exist(save_path):
            unreal.log_warning("当前资产 %s 已存在" % merge_name)
        else:
            merge_actor = static_mesh_lib.merge_static_mesh_actors(actor_list , merge_options)
            unreal.log_warning("MERGE SUCCESS : The folder %s is save to %s" % (merge_name, save_path.replace('\\','/')))
    except Exception as e:
        unreal.log_error(f"Error in saveToAsset: {e}")

time0 = time.time()

# 获取选中的文件夹路径
selected_paths = unreal.EditorUtilityLibrary.get_selected_folder_paths()
active_path = selected_paths[0]             # /Game/ARJ_Model/221/221A101SR0010
for active_path in selected_paths:
    merge_name = active_path.split('/')[-1]     # 221A101SR0010

    # 获取当前文件夹中所有的资产路径
    assets_path = unreal.EditorAssetLibrary.list_assets(active_path, recursive=True, include_folder=False)

    # Get the current level
    current_world = unreal.UnrealEditorSubsystem().get_editor_world()

    for asset_path in assets_path:
        # 根据路径加载资产进内存
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        print(f"Loaded asset: {asset_path}")

        if asset:
            if isinstance(asset, unreal.StaticMesh):
                actor = unreal.EditorActorSubsystem().spawn_actor_from_object(asset, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
            elif isinstance(asset, unreal.Blueprint):
                actor = unreal.EditorActorSubsystem.spawn_actor_from_class(asset.GeneratedClass, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
            else:
                # Handle other asset types if needed
                actor = None

            asset = None
            actor = None
            unreal.SystemLibrary.collect_garbage()

    # 加载完成，之后进行合并操作
    # 选中所有static mesh
    level_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    asset_lib = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

    level_actors = level_lib.get_all_level_actors()
    static_mesh_actors = unreal.EditorFilterLibrary.by_class(level_actors, unreal.StaticMeshActor)

    # for item in static_mesh_actors:
    #     print(item.get_actor_label())

    # 合并所有选中的static mesh actor
    MergeActors(static_mesh_actors, merge_name, active_path)

    # 保存逻辑
    unreal.get_editor_subsystem(unreal.EditorAssetSubsystem).save_directory('/Game/',only_if_is_dirty=True,recursive=True)
    unreal.log("保存执行完毕！")
    print('Time Cost:', time.time()-time0)