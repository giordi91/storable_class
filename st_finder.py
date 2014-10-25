"""
This module holds a class used for the discovery of the files
"""
import os
import imp

from storable_class import st_class 
from storable_class import st_attribute

class Finder(st_class.StorableClass):
    """
    @brief modules finder class
    This class is specialized in being able to find the modules 
    we need and load them and make them accessible for other 
    classes to use
    you have several way to access to the modules
    first of all you have a class property called available_files.
    This property holds a list of all the valialble files, meaning they
    have the extension.py
    There is another property called files_dict, which holds a dict 
    mapping the class name to the module already loaded ready to be
    accessed
    NB : in order to work at best this class needs to respect a 
    convention between the module name and class name, this is due to
    the fact that makes live much much more easier for the coder, the 
    convention is the following:
    the name of the module separates words with underscores, the name
    of the class has no underscore and use camel-case standard.
    example:
    if we have a module called remote_server.py the corresponding class
    inside the module will be called RemoteServer.
    """
    ##attribute holdings the start path for the scan
    path = st_attribute.TypedAttr("str")
    ##this attribute holds the list of folders we want to exclude
    ##from the scan
    folders_to_eclude = st_attribute.TypedAttr("list" , [])
    ##this attribute holds files we want to exclude from the scan
    files_to_exclude = st_attribute.TypedAttr("list" , [])
    ##feature not fully implemented yet, auto_update
    auto_update = st_attribute.TypedAttr("bool" , False)

    def __init__(self):
        """
        This is the constructor
        """
        st_class.StorableClass.__init__(self)

        self.__available_files = []
        self.__files_dict = {}
        self.__modules_dict = {}
        ##feature not fully implemented yet, auto_update
        self.auto_update = False

    @property
    def available_files(self):
        """
        This is the getter function for the attribute
        available_actions, this attribute holds all the possible
        actions that the user can instanciate
        """
        if self.auto_update == 1 or self.__available_files == []: 
            self.__available_files = []
            self.__files_dict = {}
            self.__get_available_files()
        
        return self.__available_files


    @property
    def files_dict(self):
        """
        This is the getter function for the attribute
        available_actions, this attribute holds all the possible
        actions that the user can instanciate
        """
        if self.auto_update == 1 or self.__files_dict == {}: 
            self.__available_files = []
            self.__files_dict = {}
            self.__get_available_files()
        return self.__files_dict

    @property
    def modules_dict(self):
        """
        This property lets you access the dict of the modules available
        the dict maps the name of the class to the alredy loaded module
        holding the instance
        """
        #force the refresh of dict and files
        self.__modules_dict = {}
        for sub_file in self.files_dict:
            file_name = sub_file.replace(".py","")
            mod = imp.load_source(file_name , self.__files_dict[sub_file])
            class_name = self.module_to_class_name(file_name)
            self.__modules_dict[class_name] = mod

        return self.__modules_dict

    def module_to_class_name(self,input_name):
        """
        This function converts an input module name(without .py)
        into a corresponding class name.
        Default bahavior is using PEP8 directive, 
        so if a module name is:
        "my_test_for_class"
        the converted class name will be:
        MyTestFotClass

        Meaning stripped underscore and capitalize letters
        """

        return "".join(input_name.title().split("_"))


    def __get_available_files(self):
        """
        This function returns a list of all availble actions
        """
        if not self.path :
            return []

        self.__check_path(self.path)

    def __check_path(self, path):
        """
        This procedure checks a path for the py files and kicks the recursions
        @param path: str, the path that needs to be checked
        """

        res = os.listdir(path)
        to_return = []
        for sub_res in res:
            if sub_res not in self.folders_to_eclude and \
            os.path.isdir(path + sub_res) == 1:
                self.__check_path(path  + sub_res + "/")


            if sub_res.find("py") != -1 and sub_res.find(".pyc") == -1 \
            and sub_res not in self.files_to_exclude:
                if sub_res.find("reload") == -1:
                    to_return.append(sub_res)
                    self.__files_dict[sub_res] = path +"/" + sub_res
        self.__available_files += to_return
