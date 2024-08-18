import unreal
import os

# https://blog.l0v0.com/posts/a6d6fe7d.html

level_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_lib = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

selected_actors = level_lib.get_selected_level_actors()
selected_static_actors =  unreal.EditorFilterLibrary.by_class(selected_actors , unreal.StaticMeshActor.static_class())
# for actor in selected_static_actors:
#     actor_class = actor.get_class()
#     class_name = actor_class.get_name()
#     print(f"Actor: {actor.get_name()}, Class: {class_name}")

setting = unreal.MeshMergingSettings()
setting.pivot_point_at_zero = True

options = unreal.EditorScriptingMergeStaticMeshActorsOptions(
    destroy_source_actors   =   False,
    spawn_merged_actor      =   False,
    mesh_merging_settings   =   setting
)

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

# 建立临时导出路径
temp_dir = '/Game/Temp_Fbx_Export'

# 导出fbx
export_path = r'C:/FBX_Export_0815'
for actor in selected_static_actors:
    actor_name = actor.get_name()
    asset_path = os.path.join(temp_dir, actor_name)

    # If temp_directory is "/tmp/assets" and actor_name is "MyActor", then:
    # asset_path = posixpath.join("/tmp/assets", "MyActor")             # 在字符之间插入‘/’
    # The value of asset_path would be "/tmp/assets/MyActor"

    options.base_package_name = asset_path

    # 将选中的actor合并成 static mesh
    merge_actor = static_mesh_lib.merge_static_mesh_actors([actor],options)     # 单独导出
    
    # fbx_path = os.path.join(export_path, '%s.fbx' % actor_name)                 # 占位符

    # mesh = unreal.load_asset(asset_path)
    # task = unreal.AssetExportTask()
    # task.object = mesh
    # task.filename = fbx_path
    # task.exporter = fbx_exporter
    # task.automated = True
    # task.prompt = False
    # task.options = fbx_option

    # unreal.Exporter.run_asset_export_task(task)
    # 为啥不直接写ExporterFBX

# 删除临时列表
# asset_lib.delete_directory("temp_dir")
print("执行完毕！")