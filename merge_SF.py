# develop 分支
from operator import contains

# UPDATE: 2024/9/19 15:01 -> 新增命名匹配逻辑，对于PD开头，body结尾的actor，进行正则表达式匹配，将__body后面的字符替换为空字符串
# UPDATE: 2024/9/13 16:24 -> 本脚本是对于merge.py的简化，用于针对性的对供应商的模型按原AO+工位进行分类。原始脚本请看merge.py

import unreal
import csv
import time
import os
import pandas as pd
# 正则表达式模块
import re

def saveToAsset(actor, GW, AO):
    try:
        setting = unreal.MeshMergingSettings()
        setting.pivot_point_at_zero = True
        setting.merge_materials = False

        options = unreal.MergeStaticMeshActorsOptions(
            destroy_source_actors=False,
            spawn_merged_actor=False,
            mesh_merging_settings=setting
        )

        # TODO：模型保存路径
        # 供应商模型保存路径
        # temp_dir = os.path.join('/Game/ARJ_Model_GYS/', str(GW), str(AO))
        # 上飞厂模型保存路径
        temp_dir = os.path.join('/Game/ARJ_Model/', str(GW), str(AO))

        actor_label = actor.get_actor_label()
        asset_path = os.path.join(temp_dir,actor_label).replace('\\', '/') # /Game/ARJ_Model_GYS/221/531A0000-000-403/PD_269A1011-011-001__body1
        options.base_package_name = asset_path  # The package path you want to save to1

        if unreal.EditorAssetLibrary().does_asset_exist(asset_path):
            unreal.log_warning("当前资产 %s 已存在" % actor_label)
        else:
            merge_actor = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).merge_static_mesh_actors([actor], options)
            unreal.log("EXPORT SUCCESS : %s is save to %s" % (actor.get_actor_label(), asset_path.replace('\\', '/')))
    except Exception as e:
        unreal.log_error(f"Error in saveToAsset: {e}")

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

# TODO：CSV路径
# 供应商CSV路径
# csv_path = r"C:\Users\DELL\Desktop\0911\531A0000-000-403\531A0000-000-403_0918.csv"
# 上飞厂CSV路径
csv_path = r"C:\Users\DELL\Desktop\所有工位_0823.csv"

file_name = csv_path.split('\\')[-1].split('_')[0]
df = pd.read_csv(csv_path)

# TODO:仅需针对性修改列名称即可筛选目标列
# 供应商CSV列名
# df_target_col = df.loc[:, ['零组件编号',"下级工程组件"]]
# 上飞厂CSV列名
df_target_col = df.loc[:,['工位','零组件号',"下级工艺件"]]

timeStart = time.time()

# 批量处理：逻辑已修改
batch_size = 5000  # 每批处理的数量
num_batches = (len(all_static_mesh_actors) + batch_size - 1)  # batch_size
csv_count = 0
no_data_count = 0

for i in range(num_batches):
    batch = all_static_mesh_actors[i * batch_size:(i + 1) * batch_size]
    # for item in batch:
    #     unreal.log(item.get_actor_label())
    for item in batch:
        item_name = item.get_actor_label()
        if item.get_actor_label().startswith("PD_"):
            item_name = item.get_actor_label().replace("PD_", "" , 1)
        if contains(item_name, "__body"):
            # 使用正则表达式匹配 '__body' 及其后面的所有字符，并替换为空字符串
            # sub函数用于替换字符串中匹配正则表达式模式的部分
            # r：表示原始字符串，告诉 Python 不要处理字符串中的转义字符。
            # .*：匹配除换行符之外的任何单个字符
            # $：表示字符串的末尾
            item_name = re.sub(r'__body.*$', '', item_name)
        # print(item_name)

        if item.static_mesh_component.static_mesh:
            # TODO:替换列名称：零组件号 / 零组件编号
            # 供应商CSV列名
            # df_copy = df_target_col[df['零组件编号'] == item_name].copy()
            # 上飞厂CSV列名
            df_copy = df_target_col[df['零组件号'] == item_name].copy()
            if df_copy.size:
                for index, row in df_copy.iterrows():
                    # TODO：修改工位和保存名称
                    # 供应商工位号和保存零件名称
                    # saveToAsset(item, '221', file_name)
                    # 上飞厂工位号和保存零件名称
                    saveToAsset(item, row['工位'], row['下级工艺件'])

                    unreal.log("save_to_asset")
            else:
                unreal.log(f"当前csv数据中未找到：{item.get_actor_label()}")
                csv_count += 1
        else:
            unreal.log_error(f"丢失static mesh component：{item.get_actor_label()}")
            no_data_count += 1

    # 处理完一批后，可以调用GC（垃圾回收），以释放内存
    unreal.SystemLibrary.collect_garbage()

unreal.log(csv_count)
unreal.log(no_data_count)
unreal.log_warning(time.time() - timeStart)

# TODO:修改资产保存逻辑
# 供应商模型保存
# unreal.get_editor_subsystem(unreal.EditorAssetSubsystem).save_directory('/Game/ARJ_Model_GYS/',only_if_is_dirty=True,recursive=True)
# 上飞厂模型保存
unreal.get_editor_subsystem(unreal.EditorAssetSubsystem).save_directory('/Game/ARJ_Model/',only_if_is_dirty=True,recursive=True)
unreal.log("保存执行完毕！")