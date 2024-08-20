import unreal

path = '/Game/_Game/Character'

def listAssets(path):
    # 获取所有资产
    assets = unreal.EditorAssetLibrary.list_assets(path, recursive=True, include_folder=False)
    for asset in assets:
        print(asset)

# get users selection   of content and outliner
def getSelectionContentBrowser():
    EUL = unreal.EditorUtilityLibrary
    selectionAssets = EUL.get_selected_assets()
    for item in selectionAssets:
        print(item)

def getAllActors():
    EAS = unreal.EditorActorSubsystem
    actors = EAS.get_all_level_actors()
    for item in actors:
        print(item)

def getSelectedActors():
    EAS = unreal.EditorActorSubsystem()
    selectedActors = EAS.get_selected_level_actors()
    for item in selectedActors:
        print(item)

def getAssetClass():
    EAL = unreal.EditorAssetLibrary()

    assetPaths = EAL.list_assets('/Game/_Game/Character')
    # 与其说是返回资产本身，其实返回的是资产的相对路径：/Game/StarterContent/Shapes/Shape_Cylinder.Shape_Cylinder

    for assetPath in assetPaths:
        assetData = EAL.find_asset_data(assetPath)
        assetClass = assetData.asset_class_path             # <Struct 'TopLevelAssetPath' (0x0000067A5656A8FC) {package_name: "/Script/Engine", asset_name: "Texture2D"}>
        # assetClass = assetData.asset_class
            # [Read-Only] The name of the asset’s class deprecated: 
            # Short asset class name must be converted to full asset pathname.
            # Use AssetClassPath instead.
        print(assetClass.asset_name)                        # Texture2D

def getAssetClass(classType):
    EAL = unreal.EditorAssetLibrary()

    # assetPaths = EAL.list_assets('/Game/StarterContent/Architecture/')
    assetPaths = EAL.list_assets('/Game/StarterContent/Props/')

    assets = []

    for assetPath in assetPaths:
        assetData = EAL.find_asset_data(assetPath)
        assetClass = assetData.asset_class_path
        if assetClass.asset_name == classType:
            assets.append(assetData.get_asset())
            # 这里的static mesh不是路径，不是名称，而是Object本身
            # <Object '/Game/_Game/Character/Ch19_nonPBR.Ch19_nonPBR' (0x0000067A749DD200) Class 'SkeletalMesh'>
    
    # for asset in assets:
    #     print(asset)
    
    return assets

# 注意函数顺序


def getStaticMeshData():
    staticMeshes = getAssetClass('StaticMesh')
    for staticMesh in staticMeshes:
        # asset_import_data 是 static mesh 的editor property
        # assetImportData = staticMesh.get_editor_property('asset_import_data')             # <Object '/Game/StarterContent/Architecture/Floor_400x400.Floor_400x400:FbxStaticMeshImportData_23' (0x0000067A6A632000) Class 'FbxStaticMeshImportData'>
        # fbxFilePath = assetImportData.extract_filenames()                                 # ["D:/../../Dropbox/Rocket/SourceArt/StarterContent/SM_Floor_400x400.FBX"]
        # print(fbxFilePath)

        lod_GroupInfo = staticMesh.get_editor_property('lod_group')
            # 即使打印为 None，也并不代表没有lod，有可能用户使用了dcc创建了自定义的lod。这是一种判断确定是否使用通用lod的方案配置
            # 这里的 lod_group 只表示 UE 针对 SM 自动生成的LOD信息
        print(lod_GroupInfo)
        if lod_GroupInfo == 'None':
            # print(staticMesh.get_name())
            if staticMesh.get_num_lods() == 1:
                staticMesh.set_editor_property('lod_group','LargeProp')                     # 对于静态网格体实施LOD优化

# 每个lod的三角形数量
def getStaticMeshLODData():
    
    PML = unreal.ProceduralMeshLibrary

    staticMeshes = getAssetClass('StaticMesh')

    for staticMesh in staticMeshes:
        staticMeshTriCount = []                 # 当前SM中三角形数量
        numLODs = staticMesh.get_num_lods()     # 当前static mesh ue自动生成的lod层级数量

        for i in range(numLODs):
            numSections = staticMesh.get_num_sections(i)        # A section is a group of triangles that share the same material.
            LodTriCount = 0
            for j in range(numSections):
                sectionData = PML.get_section_from_static_mesh(staticMesh,i,j)
                sectionTriCount = len(sectionData[1]) / 3       # 当前section,三角形数量
                LodTriCount += (int)(sectionTriCount)      # 当前lod中三角形的数量

            staticMeshTriCount.append(LodTriCount)
        staticMeshReduction = [100]                 # 初始模型三角形占比100%

        for i in range(1,len(staticMeshTriCount)):
            staticMeshReduction.append((int)((staticMeshTriCount[i] / staticMeshTriCount[0]) * 100))

        # staticMeshReduction = [str(item) + '%' for item in staticMeshReduction]       # TODO:这是一种什么写法?这种写法会有什么好处?
        # 后续可以删除三角形网格数量少于20%的lod，算是一种优化的手段了
        
        print(staticMesh.get_name())
        print(staticMeshTriCount)       # python中的占位符,我不会用
        print(staticMeshReduction)
        print(".................")

# 每个static mesh在场景中出现的次数
def getStaticMeshInstanceCounts():

    levelActors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()

    # 如何获取下面挂的所有子物体？
    staticMeshActors = []
    staticMeshActorCounts = []

    for levelActor in levelActors:
        if(levelActor.get_class().get_name() == 'StaticMeshActor'):
            staticMeshComponent = levelActor.static_mesh_component
            staticMesh = staticMeshComponent.static_mesh
            staticMeshActors.append(staticMesh.get_name())
    
    # for staticMeshActor in staticMeshActors:
    #     print(staticMeshActor)

    # 防止重复，输出当前actor在场景中出现的次数
    # TODO:前缀一样作为相同的actor
    processedActors = []
    for staticMeshActor in staticMeshActors:
        if staticMeshActor not in processedActors:
            # print(staticMeshActor , staticMeshActors.count(staticMeshActor))
            # 作为元组添加到list
            actorCounts = (staticMeshActor , staticMeshActors.count(staticMeshActor))
            staticMeshActorCounts.append(actorCounts)
            processedActors.append(staticMeshActor)
    # 排序
    staticMeshActorCounts.sort(key=lambda a: a[1] , reverse=True)
    for item in staticMeshActorCounts:
        print(item)



# getStaticMeshData()
getStaticMeshInstanceCounts()