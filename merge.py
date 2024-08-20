import unreal
import csv
import os
import pandas as pd

def get_all_attached_actors(actor, collected_actors=None):
    if collected_actors is None:
        collected_actors = []
    
    # Get attached child actors
    attached_actors = actor.get_attached_actors()
    
    # Add attached actors to the list
    for attached_actor in attached_actors:
        collected_actors.append(attached_actor)
        # Recursively get actors attached to this actor
        # get_all_attached_actors(attached_actor, collected_actors)
    
    return collected_actors

level_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_lib = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

selected_actor = level_lib.get_selected_level_actors()[0]
print(selected_actor.get_class().get_name())

# 迭代获取所有子级
all_attached_actors = get_all_attached_actors(selected_actor)

all_static_mesh_actors = []
for item in all_attached_actors:
    if (item.get_name().split('_')[0] == "StaticMeshActor" ):
        all_static_mesh_actors.append(item)

if all_attached_actors:
    print(f"Actor '{selected_actor.get_name()}' has {len(all_static_mesh_actors)} attached static mesh actor(s) (including all levels of hierarchy).")
    for item in all_static_mesh_actors:
        print(f" - {item.get_actor_label()}")
else:
    print(f"Actor '{selected_actor.get_actor_label()}' has no attached static mesh actors.")

# 对于世界大纲中的actor：
# get_name()            # StaticMeshActor_18453
# get_actor_label()     # 822-1864-551__body9

# 检查命名是否匹配
df = pd.read_csv('C:\\Users\\DELL\\Desktop\\所有工位_0819.csv')
df_target_col = df.loc[:,['工位','零组件号',"下级零组件"]]
# print(df_target_col['零组件号'])

# 大的去小的里面找
for item in all_static_mesh_actors:
    for data in df_target_col['零组件号']:
        if item.get_actor_label().split('_')[0] == data:
            # save to asset in specific name
            saveToAsset(item)
            print(f" - {item.get_actor_label()} is save!")
        else:
            print(f" - {item.get_actor_label()} is not find!")


# selected_static_actors =  unreal.EditorFilterLibrary.by_class(selected_actors , unreal.StaticMeshActor.static_class())
# for actor in selected_static_actors:
#     actor_class = actor.get_class()
#     class_name = actor_class.get_name()
#     print(f"Actor: {actor.get_name()}, Class: {class_name}")

def saveToAsset(actor):

    setting = unreal.MeshMergingSettings()
    setting.pivot_point_at_zero = True

    options = unreal.EditorScriptingMergeStaticMeshActorsOptions(
        destroy_source_actors   =   False,
        spawn_merged_actor      =   False,
        mesh_merging_settings   =   setting
    )

    temp_dir = '/Game/Temp_Fbx_Export'

    actor_name = actor.get_name()
    asset_path = os.path.join(temp_dir, actor_name)         #在字符中间插入/
    options.base_package_name = asset_path

    # 将选中的actor合并成 static mesh
    merge_actor = static_mesh_lib.merge_static_mesh_actors([actor],options)     # 单独导出
    
    print("当前actor保存完毕！")