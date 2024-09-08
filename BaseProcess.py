# HEADER   :
#   File     :   BaseProcess.py
#   Create   :   2024/09/06
#   Author   :   LiDanyang 
#   Branch   :   develop
#   Descript :   unreal 基本的保存逻辑

import unreal

unreal.EditorAssetSubsystem().save_directory('/Game/',only_if_is_dirty=True,recursive=True)