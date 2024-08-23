# develop 分支

import unreal
import csv
import time
import os
import pandas as pd


def saveToAsset(actor , GW , AO):
    setting = unreal.MeshMergingSettings()
    setting.pivot_point_at_zero = True
    setting.merge_materials = False

    options = unreal.EditorScriptingMergeStaticMeshActorsOptions(
        destroy_source_actors   =   False,
        spawn_merged_actor      =   False,
        mesh_merging_settings   =   setting
    )

    temp_dir = os.path.join('/Game/ARJ_Model',GW,AO)

    actor_name = actor.get_name()
    actor_label = actor.get_actor_label()
    asset_path = os.path.join(temp_dir, actor_label).replace('\\','/')
    print(asset_path)
    options.base_package_name = asset_path              # The package path you want to save to

    # TODO:将选中的actor合并成 static mesh

    if unreal.EditorAssetLibrary().does_asset_exist(asset_path):
        print("当前资产 %s 已存在" % actor_label)
    else:
        merge_actor = static_mesh_lib.merge_static_mesh_actors([actor],options)     # 单独导出
        print("EXPORT SUCCESS : %s is save to %s" % (actor.get_actor_label(), asset_path.replace('\\','/')))

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

all_static_mesh_actors = []

for item in selected_actors:
    if (item.get_name().split('_')[0] == "StaticMeshActor" ):
        all_static_mesh_actors.append(item)

# 检查命名是否匹配
df = pd.read_csv('C:\\Users\\DELL\\Desktop\\所有工位_0823.csv')
df_target_col = df.loc[:,['工位','零组件号',"下级工艺件"]]

timeStart = time.time()
for item in all_static_mesh_actors:
    df_copy = df_target_col[df['零组件号'] == item.get_actor_label().split('_')[0]].copy()
    # print(f' %s 找到匹配数据 %d 条' % (item.get_actor_label(),df_copy.size))

    if df_copy.size:
        for index, row in df_copy.iterrows():
            saveToAsset(item, str(row['工位']), str(row['下级工艺件'])) 
print(time.time() - timeStart)