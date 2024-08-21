import unreal

path = '/Game/_Game/Character'

def listAssets(path):
    # 获取所有资产
    assets = unreal.EditorAssetLibrary.list_assets(path, recursive=True, include_folder=False)
    for asset in assets:
        print(asset)

# get users selection of content and outliner
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

    assetPaths = EAL.list_assets('/Game/StarterContent/Props/')

    assets = []

    for assetPath in assetPaths:
        assetData = EAL.find_asset_data(assetPath)
        assetClass = assetData.asset_class_path
        if assetClass.asset_name == classType:
            assets.append(assetData.get_asset())
            # NOTE：这里get_asset()返回的'StaticMesh'，不是路径，不是名称，而是Object本身
            # 因此，此方法返回的是符合要求的Object Array
    
    # for asset in assets:
    #     print(asset)
    
    return assets


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

# 平均数量
# 每个static mesh的每个lod的三角形数量
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
        
        # print(staticMesh.get_name())
        # print(staticMeshTriCount)       # python中的占位符,我不会用
        # print(staticMeshReduction)
        # print(".................")

        # 按照LOD 1作为当前mesh多个lod之间的平均网格数
        staticMeshLODData = []
        LODData = (staticMesh.get_name() , staticMeshTriCount[0])
        staticMeshLODData.append(LODData)
    
    return staticMeshLODData

# 每个static mesh在场景中出现的次数
# 当前场景中的static mesh的资产lod的三角形面数，平均为多少
def getStaticMeshInstanceCounts():

    levelActors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()

    # TODO:如何获取下面挂的所有子物体？
    staticMeshActors = []
    staticMeshActorCounts = []      # 作为元组，存储actor和count

    for levelActor in levelActors:
    # print(levelActor.get_class())           # <Object '/Script/Engine.Actor' (0x00000BCCA9E41E00) Class 'Class'>
        if(levelActor.get_class().get_name() == 'StaticMeshActor'):
            staticMeshComponent = levelActor.static_mesh_component
            staticMesh = staticMeshComponent.static_mesh
            staticMeshActors.append(staticMesh.get_name())
    
    # levelActor.get_name()   #StaticMeshActor_13260
    # 或者使用actor.get_actor_label()

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
    # 按照每个item第二个元素排序
    # 它告诉sort()方法使用列表中每个元素的第二个元素（索引为1）作为排序依据。
    # 这里的a代表列表中的每个元素。
    # TODO:lambda表达式

    # The sort() function modifies the original list and does not return a new sorted list.

    LODData = getStaticMeshLODData()

    aggregateTriCounts = []

    for i in range(len(staticMeshActorCounts)):
        for j in range(len(LODData)):
            if staticMeshActorCounts[i][0] == LODData[j][0]:
                aggregateTriCount = (staticMeshActorCounts[i][0] , staticMeshActorCounts[i][1] * LODData[j][1])
                aggregateTriCounts.append(aggregateTriCount)

    aggregateTriCounts.sort(key = lambda a :a[1] , reverse= True)
    if not aggregateTriCounts:
        print("none")
    for item in aggregateTriCounts:
        print(item)

# 通过简单代码，查看unreal类之间的关系。比如，深挖static mesh component

# 善于使用dir/help
# 一键替换材质
def returnMaterialInfomationSMC():

    levelActors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    testMat = unreal.EditorAssetLibrary.find_asset_data('/Game/Megascans/Surfaces/Brick_Wall_xevtfjz/MI_Brick_Wall_xevtfjz_2K').get_asset()
    # 到底啥时候用get_editor_subsustem啊？反正这里的library不用

    # TODO:找到静态网格体，几种方法？
    for levelActor in levelActors:
        if(levelActor.get_class().get_name() == 'StaticMeshActor'):
            staticMeshComponent = levelActor.static_mesh_component
            # 一定要这样获取材质吗？
            # actor -> SMactor -> staticMeshComponent -> material?
            # materials = staticMeshComponent.get_materials()

            # for material in materials:
            #     print(material.get_name())

            #     # TODO:复习try except语句
            #     try:
            #         for item in material.texture_parameter_values:
            #             print(item)
            #             # 如果有texture，会输出texture的路径
            #     except:
            #         pass

            #     print('___')

            # 一键替换 Material
            for i in range(staticMeshComponent.get_num_materials()):
                staticMeshComponent.set_material(i,testMat)

getAssetClass('StaticMesh')