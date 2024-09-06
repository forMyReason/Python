#***************************************************************
#   Purpose:   blender通过python实现3dxml((版本4.3))文件格式的导入
#   Author:    爱看书的小沐
#   Date:      2022-5-1
#   Languages: python
#   Platform:  blender-3.1.2, python3.10
#   OS:        Win10 win64
# **************************************************************
################################################################
# This addon enables blender to import 3D XML 4.3 documents.
# It partially implemented the 3D XML specification 4.3 from
# Dassault Syst¨¨mes. Testing was done with files exported
################################################################

import xml.etree.ElementTree as etree
import pathlib,zipfile,time,os,tempfile,math
import bpy,bmesh,bpy_extras,mathutils

bl_info={
	"name":"3D XML (4.3) import",
	"description":"Import 3D XML 4.3",
	"author":"Chris Xiong",
	"version":(0,1),
	"blender":(3,1,2),
	"category":"Import-Export",
	"support":"TESTING"
}

unitfactor=1
meshes = dict()
meshmat = dict()
NS="{http://www.3ds.com/xsd/3DXML}"
XSI="{http://www.w3.org/2001/XMLSchema-instance}"
texdir="/3dxml/Textures/"

def unflatten2Strips(seq):
    seq_j = []
    seq=seq.strip()
    seqArr=seq.split(',')
    for i in range(len(seqArr)):
        seq=seqArr[i].replace(' ',',')
        seq=seq.split(',')
        seq=list(map(int,seq))
        
        for j in range(0, len(seq)-2):
            if j % 2 == 0 :
                seq_j.append(seq[j])
                seq_j.append(seq[j+1])
                seq_j.append(seq[j+2])
            else :
                seq_j.append(seq[j+1])
                seq_j.append(seq[j])
                seq_j.append(seq[j+2])
        # print(seq_j)

    nseq=len(seq_j)
    step = 3
    fac = 1
    return [tuple(seq_j[i+j]*fac for j in range(0,step))for i in range(0,nseq,step)]

def unflatten2Fans(seq):
    seq_j = []
    seq=seq.strip()
    seqArr=seq.split(',')
    for i in range(len(seqArr)):
        seq=seqArr[i].replace(' ',',')
        seq=seq.split(',')
        seq=list(map(int,seq))
        
        for j in range(1, len(seq)-1):
            seq_j.append(seq[0])
            seq_j.append(seq[j])
            seq_j.append(seq[j+1])
        # print(seq_j)

    nseq=len(seq_j)
    step = 3
    fac = 1
    return [tuple(seq_j[i+j]*fac for j in range(0,step))for i in range(0,nseq,step)]

def unflattenXmlNode(seqNode,func,step,fac=1):
    if seqNode == None:
        return []

    seq = seqNode.text
    seq=seq.strip()
    seq=seq.replace(' ',',')
    seq=seq.split(',')
    seq=list(map(func,seq))
    nseq=len(seq)
    return [tuple(seq[i+j]*fac for j in range(0,step))for i in range(0,nseq,step)]

def unflatten(seq,func,step,fac=1):
    seq=seq.strip()
    seq=seq.replace(' ',',')
    seq=seq.split(',')
    seq=list(map(func,seq))
    nseq=len(seq)
    return [tuple(seq[i+j]*fac for j in range(0,step))for i in range(0,nseq,step)]

def create_mesh(verts,faces,facemat,norms,uvs,meshidx):

    meshname=f"Mesh_{meshidx}"
    mesh=bmesh.new()
    for vert,norm in zip(verts,norms):
        v=mesh.verts.new(vert)
        v.normal=norm
    mesh.verts.ensure_lookup_table()
    mesh.verts.index_update()
    for i,m in zip(faces,facemat):
        f=[mesh.verts[j]for j in i]
        try:
            nf=mesh.faces.new(f)
            if m!=-1:nf.material_index=m
        except ValueError:
            pass
    uv=mesh.loops.layers.uv.new()
    msh=bpy.data.meshes.new(meshname)

    mesh.to_mesh(msh)
    meshes[meshidx]=msh
    mesh.free()
	
def load_meshes(tree, objname, bpy_collection, bpy_node):
    for rep in tree.findall(f".//{NS}Rep[@{XSI}type='PolygonalRepType']"):
        print("PolygonalRepType:", rep.attrib["id"])
        rid=rep.attrib["id"]
        verts=unflattenXmlNode(rep.find(f".//{NS}Positions"),float,3,unitfactor)
        normals=unflattenXmlNode(rep.find(f".//{NS}Normals"),float,3)
        uvs=unflattenXmlNode(rep.find(f".//{NS}TextureCoordinates"),float,2)
        faces=[]
        facemat=[]
        matslots=[]
        defmat=-1
        facesel=rep.find(f".//{NS}Faces")
        if facesel.find(f"{NS}SurfaceAttributes/{NS}MaterialApplication/{NS}MaterialId") is not None:
            defmat=0
            matslots.append(facesel.find(f"./{NS}SurfaceAttributes/{NS}MaterialApplication/{NS}MaterialId").text)
        for face in facesel.findall(f"{NS}Face"):
            fmat=defmat
            if face.find(f".//{NS}MaterialId") is not None:
                matp=-1
                try:
                    matp=matslots.index(face.find(f".//{NS}MaterialId").text)
                except ValueError:
                    matp=len(matslots)
                    matslots.append(face.find(f".//{NS}MaterialId").text)
                fmat=matp
            if "triangles" in face.attrib:
                arr = unflatten(face.attrib["triangles"],int,3)
                faces.extend(arr)
                facemat.extend([fmat]*len(arr))
            if "fans" in face.attrib:
                arr = unflatten2Fans(face.attrib["fans"])
                faces.extend(arr)
                facemat.extend([fmat]*len(arr))
            if "strips" in face.attrib:
                arr = unflatten2Strips(face.attrib["strips"])
                faces.extend(arr)
                facemat.extend([fmat]*len(arr))       
        meshmat[rid]=matslots
        create_mesh(verts,faces,facemat,normals,uvs,rid)
        
        obj=bpy.data.objects.new(str(rid),meshes[rid])
        obj.parent = bpy_node
        bpy_collection.objects.link(obj)
        
def create_objects(tree, zf, xml_nodes, id, bpy_collection, bpy_node_parent):
    xml_node = xml_nodes[id]
    objname = xml_node['name']
    ref_id = xml_node['ref_id']
    mat = xml_node['matrix']
    print("======: ", id, ref_id, mat)
    
#    bpy_node = bpy.data.collections.new(objname)
    bpy_node = bpy.data.objects.new(objname, object_data=None)
    if bpy_node_parent != None:
        bpy_node.parent = bpy_node_parent
    bpy_collection.objects.link(bpy_node)
        
    if len(mat) >0:
        _wmat=mathutils.Matrix()
        for r in range(0,3):
            _wmat[r]=[mat[i] for i in range(r,12,3)]
        bpy_node.matrix_world=_wmat
    
    if ref_id != -1:
        xml_node_ref = xml_nodes[ref_id]
        associatedFile = xml_node_ref['associatedFile']
        print(associatedFile)
        if len(associatedFile) >0 :
            meshid=associatedFile.split(":")[-1]
            xml_text = zf.open(meshid)
            tree_child = etree.parse(xml_text)
            load_meshes(tree_child, objname, bpy_collection, bpy_node)

        for child_id in xml_node_ref['children']:
            create_objects(tree, zf, xml_nodes, child_id, bpy_collection, bpy_node)

    for child_id in xml_node['children']:
        create_objects(tree, zf, xml_nodes, child_id, bpy_collection, bpy_node)

def create_bpynode():
    for collection in bpy.data.collections:
        print(collection.name)
        for obj in collection.all_objects:
            print("obj: ", obj.name)
        bpy.data.collections.remove(collection)
            
    product = bpy.data.collections.get("Product")
    if product != None:
        print(dir(product.children))
        for c in product.children:
            product.children.unlink(c)
        bpy.data.collections.remove(product)
    
    product = bpy.data.collections.new("Product")
    bpy.context.scene.collection.children.link(product)
    return product

def load_objects(tree, zf):
    product = create_bpynode()
    
    # refRepArr=tree.findall(f".//{NS}ReferenceRep[@format='TESSELLATED']")
    # print(refRepArr)

    # inst3dArr=tree.findall(f".//{NS}Instance3D")
    # print(inst3dArr)

    xml_nodes = {}
    structure = tree.getroot().find(f".//{NS}ProductStructure")
    root_id = structure.attrib["root"]
    
    for child in structure:
        # print(child.attrib["id"], child.attrib["name"], child.tag)
        id = int(child.attrib["id"])
        dict = {}
        dict['id'] = id
        dict['name'] = child.attrib["name"]
        dict['children'] = []

        try:
            if child.attrib["format"] == "TESSELLATED":
                dict['associatedFile'] = child.attrib["associatedFile"]
        except KeyError:
            dict['associatedFile'] = ''

        child_attrib = child.find(f".//{NS}IsAggregatedBy")
        if child_attrib != None:
            parent_id = int(child_attrib.text)
            dict['parent_id'] = parent_id
            xml_nodes[parent_id]['children'].append(id)
        else:
            dict['parent_id'] = -1
            
        child_attrib = child.find(f".//{NS}IsInstanceOf")
        if child_attrib != None:
            dict['ref_id'] = int(child_attrib.text)
        else:
            dict['ref_id'] = -1

        child_attrib = child.find(f".//{NS}RelativeMatrix")
        if child_attrib != None:
            dict['matrix'] = mat=list(map(float,child_attrib.text.split(' ')))
        else:
            dict['matrix'] = []

        xml_nodes[id] = dict
    
    create_objects(tree, zf, xml_nodes, int(root_id), product, None)
    
def readStructXml(xml_text, zf):
    tree = etree.parse(xml_text)
    # for child in tree.getroot():
        # print(child.tag, child.attrib)
    header = tree.getroot().find(f".//{NS}Header")
    version = header.find(f".//{NS}SchemaVersion")
    print("SchemaVersion:", version.text)

    # load_materials(tree)
    # load_meshes(tree)
    load_objects(tree, zf)

def readManifestXml(xml_text):
    tree = etree.parse(xml_text)
    root = tree.getroot().find("./Root")
    return root.text

def read(filename):
    os.system("cls") if "nt" in os.name else os.system("clear")
    time1 = time.time()
    xml_text = ""
    if zipfile.is_zipfile(filename):
        zf = zipfile.ZipFile(filename, "r")
        try:
            member = zf.namelist().index("Manifest.xml")
        except ValueError:
            raise RuntimeError("not a 3D XML 4.3 file!")
        xml_text = zf.open("Manifest.xml")
    else:
        print("Warning: the file will be treated as a bare XML document.")

    filename = readManifestXml(xml_text)
    xml_text = zf.open(filename)
    readStructXml(xml_text, zf)

    bpy.ops.file.pack_all()
    time2=time.time()
    print("Total import time is: %.2f seconds."%(time2-time1))

class ImportDialog(bpy.types.Operator,bpy_extras.io_utils.ImportHelper):
	bl_idname="object.tdxml_import"
	bl_label="3DXML Import"
	filter_glob=bpy.props.StringProperty(default='*.3dxml',options={'HIDDEN'})

#	pt=bpy.props.StringProperty(name="Texture path",default=texdir)
#	uf=bpy.props.FloatProperty(name="Unit factor",default=unitfactor,min=0)
#	us=bpy.props.BoolProperty(name="Use auto smooth instead of the normal data in the 3DXML file",default=False)
#	aa=bpy.props.FloatProperty(name="Auto smooth angle",min=0,max=180,default=90)

	def execute(self,context):
		global texdir,unitfactor,usesmooth,smoothangle
		read(self.filepath)
		return {'FINISHED'}

class _3DXMLImport(bpy.types.Operator):
	"""Import a 3DXML 4.3 file"""
	bl_idname="import_mesh.tdxml"
	bl_label="Import 3DXML 4.3..."
	bl_options={'UNDO'}
	filename_ext=".3dxml"

	def execute(self,context):
		bpy.ops.object.tdxml_import('INVOKE_DEFAULT')
		return {'FINISHED'}

def menu_func_import_tdxml(self,context):
	self.layout.operator(_3DXMLImport.bl_idname,text="3DXML 4.3 (.3dxml)")

def register():
	bpy.utils.register_class(ImportDialog)
	bpy.utils.register_class(_3DXMLImport)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import_tdxml)

def unregister():
	bpy.utils.unregister_class(_3DXMLImport)
	bpy.utils.unrigister_class(ImportDialog)

if __name__=="__main__":
	register()