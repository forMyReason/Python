# https://www.youtube.com/watch?v=rPIKf8YQnYU&list=PLBLmKCAjA25Br8cOVzUroqi_Nwipg-IdP&index=7
import unreal
# 需要指定到资产路径
def saveAsset():
    # 5.2
    # unreal.EditorAssetSubsystem().save_asset('/Game/_Actor/merge_test',only_if_is_dirty=True)
    # 5.3 API
    unreal.get_editor_subsystem(unreal.EditorAssetSubsystem).save_asset('/Game/_Actor/merge_test/SM_MERGED_StaticMeshActor_955',only_if_is_dirty=True)
    print("执行完毕")

# 指定文件夹路径
def saveDirectory():
    unreal.EditorAssetSubsystem().save_directory('/Game/_Actor/merge_test/',only_if_is_dirty=False,recursive=True)

# load Package to memory
def getPackageFromPath():
    package_path = '/Game/_Actor/merge_test/SM_MERGED_StaticMeshActor_955'
    loaded_package = unreal.load_package(package_path)
    if loaded_package:
        print(f"Package {package_path} loaded successfully!")
    else:
        print(f"Failed to load package {package_path}.")

# 找到所有dirty的package，包括umap/uasset
def getAllDirtyPakages():
    packages = unreal.Array(unreal.Package)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
        packages.append(x)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
        packages.append(x)
    for item in packages:
        print(item.get_full_name())

# 保存所有dirty Package
def saveAllDirtyPackages(show_dialog = False):
    if show_dialog:
        # 这个dialog就是保存的时候的弹窗，需要重新确认一下
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(save_map_packages=True,save_content_packages=True)
    else:
        package_path = "/Game/_Actor/merge_test/SM_MERGED_StaticMeshActor_553"
        # Load the package containing the asset first, then save it
        loaded_package = unreal.load_package(package_path)
        unreal.EditorLoadingAndSavingUtils.save_packages([loaded_package],only_dirty= False)
        # 注意，这里的package写了个list

# 获取所以loaded的package
def getAllLoadedPackages():
    loaded_packages = unreal.EditorAssetLibrary.list_loaded_packages()
    for item in loaded_packages:
        print(item.get_name())

# TODO：查找所有loaded的package

########################################################################################################################

def merge():
    # merges actors based on label
    actor_list = unreal.EditorLevelLibrary.get_all_level_actors()
    # actor_list = unreal.EditorFilterLibrary.by_class(actor_list, unreal.StaticMeshActor.static_class())
    # actor_list = unreal.EditorFilterLibrary.by_actor_label(actor_list, "*", unreal.EditorScriptingStringMatchType.MATCHES_WILDCARD)
    for item in actor_list:
        print(item.get_actor_label())
    
merge()