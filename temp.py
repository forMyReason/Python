level_lib = unreal.EditorLevelLibrary
asset_lib = unreal.EditorAssetLibrary

# merge_static_actor_to_fbx
# original code
# TODO：列表推导式
selected_static_actors = [
      a
      for a in level_lib.get_selected_level_actors()
      if isinstance(a, unreal.StaticMeshActor)
  ]

options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
options.set_editor_property("destroy_source_actors", False)
options.set_editor_property("spawn_merged_actor", False)
setting = unreal.MeshMergingSettings()

# NOTE 保留 Actor 的坐标
setting.set_editor_property("pivot_point_at_zero", True)
options.set_editor_property("mesh_merging_settings", setting)

# NOTE 配置 FBX 导出选项
fbx_exporter = unreal.StaticMeshExporterFBX()
fbx_option = unreal.FbxExportOption()
fbx_option.export_morph_targets = False
fbx_option.export_preview_mesh = False
fbx_option.level_of_detail = False
fbx_option.collision = False
fbx_option.export_local_time = False
fbx_option.ascii = False
fbx_option.vertex_color = True

# NOTE 在工程里面创建一个临时导出路径
temp_directory = "/Game/Temp_FBX_Export"
# NOTE 设置 FBX 导出路径
export_path = r"C:\FBX_EXPORT"
for actor in selected_static_actors:
    actor_name = actor.get_name()
    asset_path = posixpath.join(temp_directory, actor_name)
    options.set_editor_property("base_package_name", asset_path)
    # NOTE 将选中的 Actor 合并为 StaticMesh 资源
    level_lib.merge_static_mesh_actors([actor], options)

    fbx_path = os.path.join(export_path, "%s.fbx" % actor_name)

    mesh = unreal.load_asset(asset_path)
    task = unreal.AssetExportTask()
    task.set_editor_property("object", mesh)
    task.set_editor_property("filename", fbx_path)
    task.set_editor_property("exporter", fbx_exporter)
    task.set_editor_property("automated", True)
    task.set_editor_property("prompt", False)
    task.set_editor_property("options", fbx_option)

    unreal.Exporter.run_asset_export_task(task)

# NOTE 删除临时目录
asset_lib.delete_directory(temp_directory)
