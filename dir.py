import unreal

# 大多都可以在文档中找到，但是有些文档中没有的API
for item in dir(unreal.StaticMeshComponent):
    print(item)