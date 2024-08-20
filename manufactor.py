import unreal
import csv
import os
import pandas as pd

# 获取当前选中的Actor列表
selected_actors = unreal.EditorActorSubsystem().get_selected_level_actors()
 
if not selected_actors:
    print("未选中Actor")

for actor in selected_actors:
    print(actor.get_actor_label())

    # Save to Content Broweser as new a Asset
    # TODO:需要处理csv数据，从而指定新Asset的名称和路径
    asset_name = "MyNewActorAsset"
    asset_path = "/Game/_Actor/merge_test/"

    # 创建一个新的Asset（这里以StaticMesh为例）
    # 注意：你需要根据实际的Actor类型来创建相应的Asset
    # TODO:最终合并之后的actor是啥类型的？暂停static mesh
    # TODO：应该首先判断asset是否存在，如果存在则不创建/先删除原始文件，再重新创建

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    new_asset = asset_tools.create_asset(
        asset_name=asset_name,
        package_path=asset_path,
        asset_class=unreal.StaticMesh,
        factory= unreal.StaticMeshFactory()
        # NOTE:factory参数是一个Factory类的实例，用于创建新的Asset
        # Q: 为什么这里的factory是None？
        # A: 因为StaticMeshFactoryNew()的构造函数需要传入一个StaticMesh，而我们这里是创建一个新的StaticMesh，所以不需要传入StaticMesh
    )
    
    if new_asset:
        print("创建成功")

    # 复制Actor的数据到新Asset。这里需要根据你的具体需求来复制数据，例如，如果你的Actor是一个StaticMeshActor，你可能需要复制其StaticMeshComponent
    new_asset.set_editor_property("StaticMesh", actor.get_editor_property("StaticMesh"))

    # 保存Asset
    new_asset.save()
    # 刷新编辑器
    unreal.EditorAssetLibrary.refresh_editor()
    print(actor.get_full_name + " is save to " + asset_path)


# Merge all static mesh actors (either based on layer or level)

## merges actors based on label
# actor_list = unreal.EditorLevelLibrary.get_all_level_actors()
# actor_list = unreal.EditorFilterLibrary.by_class(actor_list, unreal.StaticMeshActor.static_class())
# actor_list = unreal.EditorFilterLibrary.by_actor_label(actor_list, "*", unreal.EditorScriptingStringMatchType.MATCHES_WILDCARD) 


# --------------------------------
## merges actors based on layer
# levelname = unreal.GameplayStatics.get_current_level_name(unreal.EditorLevelLibrary.get_editor_world())
# actor_list = unreal.EditorFilterLibrary.by_layer(unreal.EditorLevelLibrary.get_all_level_actors(), "Walls") # Find all actors in layer

# # Set the option and merge the selected static meshe actors
# merge_options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
# merge_options.new_actor_label = "MergedActor" 
# merge_options.base_package_name = "/Game/peavy/OSU_Peavy_Central_RC16_2019_03_05/MergedAsset" # Path to new asset
# merge_options.destroy_source_actors = True # Delete the old actor
# result = unreal.EditorLevelLibrary.merge_static_mesh_actors(actor_list, merge_options)
#  --------------------------------




# dataframe = pd.read_csv('C:\\Users\\DELL\\Desktop\\221.csv' , sep=',')
# for
# print("1111111")
# with open ('C:\\Users\\DELL\\Desktop\\221.csv', 'r' ,encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)



# EditorAssetLibrary
# unreal.EditorActorSubsystem().get_all_level_actors()
# unreal.EditorActorSubsystem().get_selected_level_actors()
# actor.get_attached_actors()       # 只能查找下一子级，无法迭代
# actor.get_all_child_actors(include_descendants=True)
# get_name() 方法返回的是 Actor 的内部名称
# get_actor_label() 
# 判断 asset是否存在：asset = unreal.EditorAssetLibrary.find_asset_data(asset_path)