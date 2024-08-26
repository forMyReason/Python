import unreal
# https://dev.epicgames.com/community/learning/tutorials/LnE7/unreal-engine-asset-import-export-using-unreal-python-api

def exportSelectedAssets():
    # get selected assets from content browser
    selectedAssets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem).get_selected_assets()
    # iterate over selection and export
    for selectedAsset in selectedAssets:
        assetName = selectedAsset.get_name()
        #create asset export task
        exportTask = unreal.AssetExportTask()
        exportTask.automated = True
        # object is the asset to be exported
        exportTask.object = selectedAsset
        exportTask.prompt = False
        # export static mesh assets
        if isinstance(selectedAsset, unreal.StaticMesh):
            #create class specific exporter
            exportTask.filename = 'C:\\[filePath]\\' + assetName + '.fbx'
            # necessary to include options or options dialog will appear
            exportTask.options = unreal.FbxExportOption()
            fbxExporter = unreal.StaticMeshExporterFBX()
            exportTask.exporter = fbxExporter
            fbxExporter.run_asset_export_task(exportTask)
        # export textures
        if isinstance(selectedAsset, unreal.Texture):
            exportTask.filename = 'C:\\[filePath]\\' + assetName + '.tga'
            tgaExporter = unreal.TextureExporterTGA()
            exportTask.exporter = tgaExporter
            tgaExporter.run_asset_export_task(exportTask)


exportSelectedAssets()