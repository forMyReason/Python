import unreal

# # 大多都可以在文档中找到，但是有些文档中没有的API，比如父类的method
# for item in dir(unreal.StaticMeshComponent):
#     print(item)

# 当前选中asset，获取packge_name
# selectionAssetData = unreal.EditorUtilityLibrary.get_selected_asset_data()[0]
# print(selectionAssetData.package_name)              # /Game/StarterContent/Architecture/SM_AssetPlatform
# print(selectionAssetData.asset_name)                # SM_AssetPlatform


# TODO：通过路径，查找获取 AssetData/Asset/ 
# 路径请遵循虚幻路径格式，文件名需以.隔开后再写一遍
# 如果要通过路径获取asset_data，还是不要直接写unreal.Asset()了
# 可以通过 find_asset_data 的方式
objectAssetData = unreal.EditorAssetLibrary.find_asset_data('/Game/StarterContent/Props/Materials/M_StatueGlass.M_StatueGlass')
# objectAssetData = unreal.AssetData('/Game/StarterContent/Architecture/SM_AssetPlatform.SM_AssetPlatform')
objectAsset = objectAssetData.get_asset()
# 为啥这里总输出None？
print(objectAsset)

# 获取对象的虚幻类
print(objectAsset.get_class())

# 获取对象名称，即文件名
print(objectAsset.get_fname())

# 获取对象的绝对路径
print(objectAsset.get_path_name())
