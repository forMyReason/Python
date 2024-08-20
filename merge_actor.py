import unreal

# get selected actors class type
# selected_actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()

# for actor in selected_actors:
#     actor_class = actor.get_class()
#     class_name = actor_class.get_name()
#     print(f"Actor: {actor.get_name()}, Class: {class_name}")
###################################################################################

# Merge all static mesh actors (either based on layer or level)
## merges actors based on label
actor_list = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
actor_list = unreal.EditorFilterLibrary.by_class(actor_list, unreal.StaticMeshActor.static_class())       # 过滤所有的actors，只保留static mesh的列表，筛选actors的第二种方式
for i in actor_list:
    print(i.get_actor_label())
# actor_list = unreal.EditorFilterLibrary.by_actor_label(actor_list, "*", unreal.EditorScriptingStringMatchType.MATCHES_WILDCARD) 

# ## merges actors based on layer
# levelname = unreal.GameplayStatics.get_current_level_name(unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_editor_world())
# actor_list = unreal.EditorFilterLibrary.by_layer(unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors(), "Walls") # Find all actors in layer

# # Set the option and merge the selected static meshe actors
# merge_options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
# merge_options.new_actor_label = "MergedActor" 
# merge_options.base_package_name = "/Game/peavy/OSU_Peavy_Central_RC16_2019_03_05/MergedAsset" # Path to new asset
# merge_options.destroy_source_actors = True # Delete the old actor
# result = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).merge_static_mesh_actors(actor_list, merge_options)


# merge actors
# Set all the merge options
merge_options = EditorScriptingMergeStaticMeshActorsOptions()
merge_options.base_package_name = "/Game/Content/MergedActors/MergedTestActor"
merge_options.destroy_source_actors = False
merge_options.new_actor_label = "MergedTestActor"
merge_options.spawn_merged_actor = True
merge_options.mesh_merging_settings.bake_vertex_data_to_mesh = False
merge_options.mesh_merging_settings.computed_light_map_resolution = False
merge_options.mesh_merging_settings.generate_light_map_uv = False
merge_options.mesh_merging_settings.lod_selection_type = MeshLODSelectionType.ALL_LO_DS
merge_options.mesh_merging_settings.merge_physics_data = True
merge_options.mesh_merging_settings.pivot_point_at_zero = True

# merge meshes actors and retrieve spawned actor
merged_actor = EditorLevelLibrary.merge_static_mesh_actors(actors_to_merge, merge_options)