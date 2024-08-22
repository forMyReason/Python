import os

path = r'D:/ComacMetaUniverse_5.4/comacmetauniverse/Content/Arts/StaticMesh/HJ_HuanJing'
B_path = [B06,B09,B10,B16,B17,B18,B22,B24,B26,B50,B51,B54,B55,B56] 
C_path = [C01,C02,C03,C11,C12,C13,C51,C52,C54,C55,C57,C59]
D_path = [D01,D02,D04,D05,D06,D08_09]

for item in B_path:
    # new_path = os.join('path',str(item))
    print(item)

# if not os.path.exists(newpath):
#     os.makedirs(newpath)