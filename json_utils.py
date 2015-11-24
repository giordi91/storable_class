"""
This modules contains useful function to deal with
json files
"""

import json

def check_pyside():
    """
    This function checks if PySide is available
    """
    found = False
    try :
        from PySide import QtGui
        return True
    except :
        return False

def ensure_path(start_path, save=True):
    """
    This function ensure to return a path or 
    raises an error if is not possible to do so
    @param start_path: str, the starting path of the browser
    """

    if not start_path:
        start_path = __file__
    if check_pyside() == True:
        from PySide import QtGui
        if save:
            picked_path= QtGui.QFileDialog.getSaveFileName(None,
        "Pick path", start_path, "AnyFile *.*")[0]
        else :
            picked_path= QtGui.QFileDialog.getOpenFileName(None,
        "Pick path", start_path, "AnyFile *.*")[0]


        return picked_path
    else:
        raise ValueError("PySide not availbe for import. \
            \n You cannot dynamically provide a path. \n \
            You have to provide a valid path as argument")

def save(stuff_to_save=None, path=None, start_path=None):
    '''
    This procedure saves given data in a json file
    @param[in] stuff_to_save : this is the data you want to save ,
                                be sure it s json serializable
    @param path : where you want to save the file
    '''
    if not path :
        path = ensure_path(start_path)
    
    if path == "":
        return

    to_be_saved = json.dumps(stuff_to_save, sort_keys=True, \
                            ensure_ascii=True, indent=2)
    current_file = open(path, 'w')
    current_file.write(to_be_saved)
    current_file.close()

    print "------> file correctly saved here : ", path
    return path

def load(path=None, start_path=None):
    '''
    This procedure loads and returns the content of a json file
    @param path:  what file you want to load
    @return : the content of the file
    '''
    if not path :
        path = ensure_path(start_path, False)
    
    if path == "":
        return


    current_file = open(path)
    data_file = json.load(current_file)
    
    return data_file
