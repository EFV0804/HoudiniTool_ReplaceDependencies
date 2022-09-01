import hou
import os
import json
import shutil

proxy_path = hou.getenv('RS_PROXY')

def get_dependencies():
    '''
    Returns a list of file references present in the hip file, if they have an existence on disk.

    args: None
    returns: list of tuples (parm, path).
    '''
    file_ref = hou.fileReferences()
    dependencies = []
    for file in file_ref:
        if os.path.exists(file[1]):
            dependencies.append(file)
    return dependencies
    
def get_src_dependency_path(dependency):
    '''
    Gets path from dependency tuple

    Args: tuple(parm, path)
    Return: str
    '''
    src_path = dependency[1]
    return src_path
    
def get_trg_dependency_path(src_path):
    '''
    Gets a target path based on src path and rs_proxy path

    Args: str path
    Return: str path
    '''
    basename = os.path.basename(src_path)
    target_path = proxy_path + "\\" + basename
    return target_path
    
def replace_dependencies_paths(dependencies, path_mapping):
    '''
    Replaces every dependency path for the proxy paths and sets proxy otlscan_path

    Args: list[tuple(parm, path)], dictionary
    Returns: None
    '''
    for file in dependencies:
        parm, path = file
        if parm != None:
            print(parm)
            parm.set(path_mapping[path])
    otlscan_path = hou.getenv('HOUDINI_OTLSCAN_PATH')
    otlscan_path += ";" + proxy_path
    hou.putenv('HOUDINI_OTLSCAN_PATH', otlscan_path)
            
def get_path_mapping():
    '''
    Creates and returns a dictionary where every key is an original path, and every value is the proxy equivalent.

    Args: None
    Returns: dictionary{'old_path' : 'new_path'}
    '''
    dependencies = get_dependencies()
    path_mapping = {}
    
    for x in dependencies:
        src_path = get_src_dependency_path(x)
        trg_path = get_trg_dependency_path(src_path)
        path_mapping[src_path] = trg_path
        
    return path_mapping
        
def write_path_mapping_file(path_mapping):
    '''
    Creates and/or writes to a text file in proxy folder, to store path mapping dictionary as JSON data.

    Args: dictionary{'old_path' : 'new_path'}
    Returns: None 
    '''
    with open(proxy_path + "\\" + 'path_mapping.txt', 'w') as path_mapping_file:
        json_string = json.dumps(path_mapping)
        path_mapping_file.write(json_string)
        
def read_path_mapping_file():
    '''
    Read JSON data from path mapping file on disk

    args: None
    Returns: dictionary organised like this: {'old_path' : 'new_path'}
    '''
    with open(proxy_path + "\\" + 'path_mapping.txt', 'r') as path_mapping_file:
        txt_data = path_mapping_file.read()
        path_mapping = json.loads(txt_data)
        
    return path_mapping
    
def copy_dependencies(path_mapping):
    '''
    Copies every file in the path mapping, from the original path to the proxy folder.

    Args: dictionary{'old_path' : 'new_path'}
    Returns: None
    '''
    for key in path_mapping.keys():
        src_path = key
        trg_path = path_mapping[key]
        shutil.copy(src_path, trg_path)
        
def revert_paths():
    '''
    Gets path mapping dict and list and list of dependencies, and updates the paths back to the original paths.

    Args: None
    Returns: None
    '''
    dependencies = get_dependencies()
    path_mapping = read_path_mapping_file()
    for key, value in path_mapping.items():
        for file in dependencies:
            parm, path = file
            if parm != None:
                if path == value:
                    parm.set(key)

def pre_render():
    dependencies = get_dependencies()
    path_mapping = get_path_mapping()
    write_path_mapping_file(path_mapping)
    copy_dependencies(path_mapping)
    replace_dependencies_paths(dependencies, path_mapping)

def post_render():
    revert_paths()