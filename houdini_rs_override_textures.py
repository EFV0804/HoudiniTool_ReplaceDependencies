import hou
import os

overrides_path = "T:/overrides.txt"
new_texture_path = "T:/textures"

with open(overrides_path, 'a+') as overrides:

    for parm, path in hou.fileReferences():
        if type(parm).__name__ != 'NoneType':
            if parm.node().type() == hou.vopNodeTypeCategory().nodeType("redshift::TextureSampler"):
                overrides.write('"' + path + '"' + ' ' + '"' + new_texture_path + '"' + '\n')
        else:
            pass