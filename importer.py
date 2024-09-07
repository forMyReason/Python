import unreal
import os
import time

# https://dev.epicgames.com/community/learning/tutorials/LnE7/unreal-engine-asset-import-export-using-unreal-python-api

# 两种导入方式
# 指定资产文件夹
# 指定资产具体路径

# filenames = [
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Clay_Beveled_N.png",
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Clay_New_D.png",
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Clay_New_M.png",
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Clay_New_N.png",
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Clay_Old_D.png",
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Clay_Old_N.png",
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Cut_Stone_D.png",
#     "C:\\Users\\DELL\\Desktop\\export_fbx\\T_Brick_Cut_Stone_N.png"
# ]


file_path = r"C:\\Users\\DELL\\Desktop\\export_fbx\\"

files = os.listdir(file_path)       # 每个文件的文件名
png_files = [file for file in files if file.endswith('.png')]
filenames = []
for file in png_files:
    filename = file_path + file
    filenames.append(filename)

# 两种导入方式：
# import_assets_automated(import_data)
# import_asset_tasks(import_tasks)

assetTools = unreal.AssetToolsHelpers().get_asset_tools()

import_data = unreal.AutomatedAssetImportData()
import_data.filenames = filenames
import_data.destination_path = '/Game/_Actor/'

assetTools.import_assets_automated(import_data)
