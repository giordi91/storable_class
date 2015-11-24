"""
This module implements a basic class able to store and 
load itself
"""
import inspect

from storable_class import attribute
from storable_class import json_utils

class Container(object):
    """
    @brief basic storable class
    """
    def get_data(self):
        """
        This function will gather all the needed data from 
        all the attribute from the given class and then 
        will return it in a dict where the key is the name 
        of the attribute and the value is the value of
        the attribute itself
        @return dict
        """
        #Find the attribute of the shader
        attrs_to_save = self.get_attrs()
        
        #Build the dict
        to_return = dict((name, getattr(self, name)) for name in attrs_to_save)
        to_return["type"] = self.__class__.__name__
        return to_return

    def set_data(self, data):
        """
        This function tries to see what 
        atribute have matching keys in the data and then
        if found sets the value for that attribute
        @param data: dict, the dict previously generate from a
                     get_data() call
        """
        attrs_to_load = self.get_attrs()
        for name in attrs_to_load:
            if name in data:
                setattr(self, name, data[name])
        #to do logging if not possible to set


    @classmethod
    def get_attrs(cls):
        """
        This function is used to scan the class and find all the
        attributes in the class, returns a dictonary where
        the key is the name of the attribute and the value
        is the instance of that attribute
        @param cls: the class instance to work on
        @returns str[], a list of names of the different attributes
        """

        results = [a
                   for b in inspect.getmro(cls)[::-1]
                   for a, v in vars(b).items()
                   if issubclass(type(v), attribute.Attribute)
                   ]
        
        return results

    def save(self, path=None):
        """
        This function save all the data of the 
        class to a json file , of course is up to the user
        to make sure that the data if the attribute can be clasted
        to string or serializable format
        @param path : str, where to save the class
        """ 
        to_save = self.get_data()
        json_utils.save(to_save, path)


    def load(self, path=None):
        """
        This functions loads all the data in the  class
        from a json file
        @param path: str, the location of the file to read, if not
                     provided a popup dialog browser will show up
        """
        #read the data from file
        
        data = json_utils.load(path)
        #set the data in the class
        self.set_data(data)
