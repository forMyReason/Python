# develop 分支

import unreal
import csv
import time
import os
import pandas as pd
from multiprocessing import Pool, Process
import threading
from concurrent.futures import ThreadPoolExecutor

def saveToAsset(actor , GW , AO):
    try:
        setting = unreal.MeshMergingSettings()
        setting.pivot_point_at_zero = True
        setting.merge_materials = False

        options = unreal.EditorScriptingMergeStaticMeshActorsOptions(
            destroy_source_actors   =   False,
            spawn_merged_actor      =   False,
            mesh_merging_settings   =   setting
        )

        temp_dir = os.path.join('/Game/ARJ_Model', str(GW), str(AO))

        actor_name = actor.get_name()
        actor_label = actor.get_actor_label()
        asset_path = os.path.join(temp_dir, actor_label).replace('\\','/')
        options.base_package_name = asset_path              # The package path you want to save to

        # TODO:将选中的actor合并成 static mesh

        if unreal.EditorAssetLibrary().does_asset_exist(asset_path):
            unreal.log_warning("当前资产 %s 已存在" % actor_label)
        else:
            merge_actor = static_mesh_lib.merge_static_mesh_actors([actor],options)     # 单独导出
            print("EXPORT SUCCESS : %s is save to %s" % (actor.get_actor_label(), asset_path.replace('\\','/')))
    except Exception as e:
        unreal.log_error(f"Error in saveToAsset: {e}")

# 迭代下去找子级，开销较大
def get_all_attached_actors(actor, collected_actors=None):
    if collected_actors is None:
        collected_actors = []
    
    # Get attached child actors
    attached_actors = actor.get_attached_actors()

    # Add attached actors to the list
    for attached_actor in attached_actors:
        collected_actors.append(attached_actor)
        # Recursively get actors attached to this actor
        get_all_attached_actors(attached_actor, collected_actors)
    return collected_actors

level_lib = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_lib = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
static_mesh_lib = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)

selected_actors = level_lib.get_selected_level_actors()
if not selected_actors:
    unreal.log_error("No actors selected.")
    exit()

all_static_mesh_actors = []

for item in selected_actors:
    label = item.get_name().split('_')
    if label and label[0] == "StaticMeshActor":
        all_static_mesh_actors.append(item)

# for item in all_static_mesh_actors:
#     print(item.get_actor_label().split('_')[0])

# 检查命名是否匹配
df = pd.read_csv('C:\\Users\\DELL\\Desktop\\所有工位_0823.csv')
df_target_col = df.loc[:,['工位','零组件号',"下级工艺件"]]

timeStart = time.time()

# # 原始逻辑:已修改
# for item in all_static_mesh_actors:
#     if item.static_mesh_component.static_mesh:
#         label = item.get_actor_label().split('_')
#         if label:
#             df_copy = df_target_col[df['零组件号'] == label[0]].copy()
#             # print(df_copy)
#             if df_copy.size:
#                 for index, row in df_copy.iterrows():
#                     saveToAsset(item, row['工位'], row['下级工艺件'])
#     else:
#         unreal.log_error(f"{item.get_actor_label()} has no static mesh component.")


# 使用多线程提高执行效率，但ue的某些操作只能放在主线程中执行
# with ThreadPoolExecutor(max_workers=4) as p:
#     for item in all_static_mesh_actors:
#         df_copy = df_target_col[df['零组件号'] == item.get_actor_label().split('_')[0]].copy()

#         if df_copy.size:
#             for index, row in df_copy.iterrows():
#                 p.submit(saveToAsset, item, row['工位'], row['下级工艺件'])

# 批量处理：逻辑已修改
batch_size = 500  # 每批处理的数量
num_batches = (len(all_static_mesh_actors) + batch_size - 1)        # batch_size

for i in range(num_batches):
    batch = all_static_mesh_actors[i*batch_size:(i+1)*batch_size]
    for item in batch:
        if item.static_mesh_component.static_mesh:
            df_copy = df_target_col[df['零组件号'] == item.get_actor_label().split('_')[0]].copy()

            if df_copy.size:
                for index, row in df_copy.iterrows():
                    saveToAsset(item, row['工位'], row['下级工艺件'])

    # 处理完一批后，可以调用GC（垃圾回收），以释放内存
    unreal.SystemLibrary.collect_garbage()

unreal.log_error(time.time() - timeStart)