"""
This module holds the definition of manager 
for storable classes
"""
import os
import imp

from storable_class import container 
from storable_class import attribute
from storable_class import json_utils

class StorableManager(object):
    """
    @brief This is the manager class
    The manager class is in carge of putting togheter the finder and 
    storable class, in this way you are able to create session (collection of classes)
    and be able to save and reload the session
    """
    def __init__(self):
        """
        This is the constructor
        """
        ##this is a list where the classes can be saved and loaded
        ## it s up to the user to make sure to keep the list up to date 
        self.classes = []

    def instance_from_string(self, class_name, finder):
        """
        This funciton return the wanted class instance 
        if available
        @param class_name: str, the class we want to instantiate
        @param finder: Finder, the finder configured for finding 
                       the files and load the modules
        """

        module_dict = finder.modules_dict
        #lets check if the class is instantiabile 
        #if so we return it
        if class_name in module_dict:
            return module_dict[class_name].get_instance()

    def save_classes(self, path=None):
        """
        This function saves all the content of the classes
        on a json file
        @param path: str, where to save the file (filename include),
                    if not provided will be promed through a 
                    PySide browser
        """
        data = [my_class.get_data() for my_class in self.classes]
        json_utils.save(data, path)

    def load_classes(self, finder, path=None ):
        """
        This function load all the  classes
        from a json file
        @param finder: Finder, the finder we wish to use for loading the class
        @param path: str, from where to laod the file (filename include),
                    if not provided will be promed through a 
                    PySide browser
        """
        self.classes = []
        data = json_utils.load(path)
        for sub_data in data:
            my_class = self.instance_from_string(sub_data["type"], finder)
            if not my_class:
                #logging?
                continue
            my_class.set_data(sub_data)
            self.classes.append(my_class)
