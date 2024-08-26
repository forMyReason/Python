import unreal

# 导出当前选中的asset
# https://www.youtube.com/watch?v=TwCIRSCKe54

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()

# 两种导出方式，通过task和通过assettools，
# 后者导出对应右键bulk export，导入路径携带当前 /Game/_Actor/ 路径
# 前者更自由
# assetTools = unreal.AssetToolsHelpers().get_asset_tools()
# assetTools.export_assets(selectedAssets , "C:\\Users\\DELL\\Desktop\\export_fbx\\")

for selectedAsset in selectedAssets:
    assetName = selectedAsset.get_name()

    exportTask = unreal.AssetExportTask()
    exportTask.automated = True
    exportTask.object = selectedAsset
    exportTask.options = unreal.FbxExportOption()
    exportTask.selected = None
    exportTask.replace_identical = True

    if isinstance(selectedAsset,unreal.StaticMesh):
        exportTask.filename = "C:\\Users\\DELL\\Desktop\\export_fbx\\" + assetName + '.fbx'
        fbxExporter = unreal.StaticMeshExporterFBX()
        exportTask.exporter = fbxExporter
        fbxExporter.run_asset_export_task(exportTask)
        print(f"{assetName} is exported as fbx !!")

    if isinstance(selectedAsset,unreal.Texture2D):
        exportTask.filename = "C:\\Users\\DELL\\Desktop\\export_fbx\\" + assetName + '.png'
        pngExporter = unreal.TextureExporterPNG()
        exportTask.exporter = pngExporter
        pngExporter.run_asset_export_task(exportTask)
        print(f"{assetName} is exported as PNG!")