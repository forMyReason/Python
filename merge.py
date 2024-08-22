# develop 分支

import unreal
import csv
import time
import os
import pandas as pd

# 迭代下去找子级，开销较大
# def get_all_attached_actors(actor, collected_actors=None):
#     if collected_actors is None:
#         collected_actors = []
    
#     # Get attached child actors
#     attached_actors = actor.get_attached_actors()
    
#     # Add attached actors to the list
#     for attached_actor in attached_actors:
#         collected_actors.append(attached_actor)
#         # Recursively get actors attached to this actor
#         get_all_attached_actors(attached_actor, collected_actors)
#     return collected_actors

level_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_lib = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

selected_actors = level_lib.get_selected_level_actors()
selected_actor = level_lib.get_selected_level_actors()[0]
# print(len(level_lib.get_selected_level_actors()))
# print(selected_actors[0].get_class().get_name())

all_static_mesh_actors = []

for item in selected_actors:
    if (item.get_name().split('_')[0] == "StaticMeshActor" ):
        all_static_mesh_actors.append(item)

# for i in all_static_mesh_actors:
#     print(i.get_actor_label())
#     # 1800个也才9s

# print("111111111111111")
# 0.0145s

# 检查命名是否匹配
df = pd.read_csv('C:\\Users\\DELL\\Desktop\\所有工位_0822.csv')
df_target_col = df.loc[:,['工位','零组件号',"下级工艺件"]]

timeStart = time.time()
for item in all_static_mesh_actors:
    print(item.get_actor_label().split('_')[0])
    df_copy = df[df['零组件号'] == item.get_actor_label().split('_')[0]].copy()
    # print(df_copy)
    # for data in df_copy:
    #     if item.get_actor_label().split('_')[0] == data:
    #         print(item.get_actor_label().split('_')[0])
    #         # TODO:save to asset in specific name
    #         # saveToAsset(item)
    #         print(f" - {item.get_actor_label()} is save!")
    #     else:
    #         print(f" - {item.get_actor_label()} is not find!")
print(time.time() - timeStart)

# # selected_static_actors =  unreal.EditorFilterLibrary.by_class(selected_actors , unreal.StaticMeshActor.static_class())
# # for actor in selected_static_actors:
# #     actor_class = actor.get_class()
# #     class_name = actor_class.get_name()
# #     print(f"Actor: {actor.get_name()}, Class: {class_name}")

# def saveToAsset(actor):

#     setting = unreal.MeshMergingSettings()
#     setting.pivot_point_at_zero = True

#     options = unreal.EditorScriptingMergeStaticMeshActorsOptions(
#         destroy_source_actors   =   False,
#         spawn_merged_actor      =   False,
#         mesh_merging_settings   =   setting
#     )

#     temp_dir = '/Game/Temp_Fbx_Export'

#     actor_name = actor.get_name()
#     asset_path = os.path.join(temp_dir, actor_name)         #在字符中间插入/
#     options.base_package_name = asset_path

#     # 将选中的actor合并成 static mesh
#     merge_actor = static_mesh_lib.merge_static_mesh_actors([actor],options)     # 单独导出
    
#     print("当前actor保存完毕！")