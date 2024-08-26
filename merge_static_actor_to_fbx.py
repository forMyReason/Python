import unreal
import os

# 合并actor为fbx
# https://blog.l0v0.com/posts/a6d6fe7d.html

level_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_lib = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)

selected_actors = level_lib.get_selected_level_actors()
selected_static_actors = unreal.EditorFilterLibrary.by_class(selected_actors,unreal.StaticMeshActor)

setting = unreal.MeshMergingSettings()
setting.pivot_point_at_zero = True

options = unreal.MergeStaticMeshActorsOptions(
    destroy_source_actors   =   False,
    spawn_merged_actor      =   False,
    mesh_merging_settings   =   setting
)
# TODO:合并的option和合并的settings有啥区别?

#NOTE:导出Fbx导出选项
fbx_exporter = unreal.StaticMeshExporterFBX()
fbx_option = unreal.FbxExportOption()

fbx_option.export_morph_targets = False
fbx_option.export_preview_mesh = False
fbx_option.level_of_detail = False
fbx_option.collision = False
fbx_option.export_local_time = False
fbx_option.ascii = False
fbx_option.vertex_color = True

# 建立临时导出路径,用于保存合并的actor
temp_dir = r'/Game/Temp_Fbx_Export'

# 导出fbx
export_path = r"C:/Users/79160/Desktop/fbx_export"

static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

for actor in selected_static_actors:
    actor_name = actor.get_name()
    asset_path = os.path.join(temp_dir, actor_name)

    # The package path you want to save to
    options.base_package_name = asset_path

    # 将选中的actor合并成 static mesh
    merge_actor = static_mesh_lib.merge_static_mesh_actors([actor],options)     # 单独导出
    
    fbx_path = os.path.join(export_path, '%s.fbx' % actor_name)                 # 占位符

    # load asset to memory,allowing to access and manipulate it programmatically.
    mesh = unreal.load_asset(asset_path)

    task = unreal.AssetExportTask()
    # Contains data for a group of assets to export

    task.object = mesh                  # Asset to export
    task.filename = fbx_path
    task.exporter = fbx_exporter        # Optional exporter, otherwise it will be determined automatically
    task.automated = True               # Unattended export:按我的理解,就是不会弹出fbx导出窗口供用户选择
    task.prompt = False                 # Allow dialog prompts
    task.options = fbx_option           # Exporter specific options

    unreal.Exporter.run_asset_export_task(task)
    # Export the given object to file.
    # Child classes do not override this, but they do provide an Export() function to do the resource-specific export work.

# 删除临时列表
asset_lib.delete_directory("temp_dir")
print("执行完毕！")