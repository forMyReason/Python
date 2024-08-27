import unreal
import os

# 合并actor为fbx
# 一般思路为，先保存为asset，再导出asset
# https://blog.l0v0.com/posts/a6d6fe7d.html

level_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_lib = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)

selected_actors = level_lib.get_selected_level_actors()
selected_static_actors = unreal.EditorFilterLibrary.by_class(selected_actors,unreal.StaticMeshActor)
selected_static_actors = unreal.EditorFilterLibrary.by_class(selected_actors,unreal.StaticMeshActor)

setting = unreal.MeshMergingSettings()
setting.pivot_point_at_zero = True

merge_options = unreal.MergeStaticMeshActorsOptions(
    destroy_source_actors   =   False,
    spawn_merged_actor      =   False,
    mesh_merging_settings   =   setting
)

save_path = r'/Game/Temp_Fbx_Export'

fbx_exporter = unreal.StaticMeshExporterFBX()
fbx_option = unreal.FbxExportOption()

export_path = r"C:/Users/79160/Desktop/fbx_export/"     # 最后要加 /

static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

for actor in selected_static_actors:
    actor_name = actor.get_name()
    actor_path = os.path.join(save_path, actor_name)

    # TODO：这种path到底啥时候带具体文件名称啊？
    merge_options.base_package_name = actor_path            # The package path you want to save to

    # 将选中的actor合并成 static mesh
    merge_actor = static_mesh_lib.merge_static_mesh_actors([actor],merge_options)     # 单独导出

    mesh = unreal.load_asset(actor_path)                    # load asset to memory,allowing to access and manipulate it programmatically.

    # 导出fbx
    task = unreal.AssetExportTask()

    task.object = mesh                  # Asset to export
    task.filename = export_path + actor_name + '.fbx'
    task.exporter = fbx_exporter        # Optional exporter, otherwise it will be determined automatically
    task.automated = True               # Unattended export:按我的理解,就是不会弹出fbx导出窗口供用户选择
    task.prompt = False                 # Allow dialog prompts
    task.options = fbx_option           # Exporter specific options

    unreal.Exporter.run_asset_export_task(task)

# 删除临时列表
asset_lib.delete_directory("save_path")
print("执行完毕！")