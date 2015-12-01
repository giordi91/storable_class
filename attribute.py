"""
This module implements an abstract attribute descriptor
"""
import weakref

class Attribute(object):
    """
    @brief This class implements an abstract attribute

    The attribute is a basic component added to the class,
    the peculiarity is that it s a descriptor, this means that
    the class using the descriptor will be able to pick all
    the added descriptor for later use
    """
    def __get__(self, instance, owner):
        """
        getter method of the attribute
        @param instance: the instance of which we are accessing the attribute
        @param owner: class type of the instance
        """
        
        raise NotImplementedError("Attribute : __get__ is an abstract method \
                            and needs to be re-implemented")

    def __set__(self, instance, value):
        """
        Setter method of the attribute
        @param instance: the instance of the class we are using the attribute of
        @param value: the input value we need to set internally
        """
        raise NotImplementedError("Attribute : __set__ is an abstract method \
                    and needs to be re-implemented")


class GenericAttr(Attribute):
    """
    @brief Implements a generic descriptor to be sublclassed
    if needed.
    The use of this descriptor is for dinamically find the
    attributes added to the class
    """
    def __init__(self, default = None):
        """
        Constructor
        @param default: value to return in case there is no set value for the 
                        key asked in the weakref dict 
        """
        Attribute.__init__(self)
        ##the internal dict holding all the data
        self.data = weakref.WeakKeyDictionary()
        ##default value to return in case __get__ funtcion
        ##fails
        self.default = default

    def __get__(self, instance, owner):
        """
        Getter function
        @param instance: class, the instance we need the data of
        @param owner the type class
        """
        if instance in self.data:
            return self.data[instance]
        else:
            return self.default

    def __set__(self, instance, value):
        """
        Setter function
        @param instance: class, the instance we need the data of
        @param value : the value we need to store
        """
        self.data[instance] = value


class TypedAttr(GenericAttr):
    """
    @brief This class implements type attribute

    This attribute filters it's input based on 
    data types allowed which are set a creation 
    time

    """
    def __init__(self, data_type , default = None):
        """
        Constructor
        @param data_type: str,list, the supported data for this attribute
        @param default: value to return in case there is no set value for the 
                        key asked in the weakref dict 
        """
        GenericAttr.__init__(self, default)

        ##The data type of the constructor
        self.data_type = data_type

    def __set__(self, instance, value):
        """
        Setter function of the descriptor,
        which first performs the check 
        on the data type , if passed
        sets the value internally 
        """
        #check the data type if is corect
        if not self.check_data_type(value):
            return

        GenericAttr.__set__(self,instance,value)

    def check_data_type(self, value):
        """
        This function checks that the input data is valid
        @param value: the value to test
        @return bool
        """
        #since the attribute supports multiple data type
        #we check if the data_type is a list
        if type(self.data_type).__name__ != "list":
            #If not a list we check normally the type
            if type(value).__name__ != self.data_type:
                raise ValueError("Typed_attr : expected {x} got {y}".format(
                    x=self.data_type, y=type(value).__name__))
            else:
                return 1
        else:
            #if it s a list we check if the type is in the accepted list
            if type(value).__name__ not in self.data_type:
                raise ValueError("Typed_attr : expected {x} got {y}".format(
                    x=self.data_type, y=type(value).__name__))

            else:
                return 1

class DefaultFunAttr(TypedAttr):    
    """
    @brief This class implements type attribute

    This attribute is needed for being able to return 
    default values which are mutables, like a list of a dictionry.
    Rather then setting that as default value in a TypedAttr , which we knows
    leads to bugs and problems (like every list and dict default value), we instead
    use a functon which generates a bispoke default value whenever is needed, in the case
    of a list we can just pass the list and dict function
    """
    def __init__(self, data_type, default_function ):
        """
        Constructor
        @param data_type: str,list, the supported data for this attribute
        @param default_function: this is a function which has to be parametreless, 
                                 (use partial to wrap arguments) which is in charge
                                 to generate a default value for the attribute
                        
        """
        TypedAttr.__init__(self,data_type, default_function)
    
    def __get__(self, instance, owner):
        """
        Getter function
        @param instance: class, the instance we need the data of
        @param owner the type class
        """
        if instance in self.data:
            return self.data[instance]
        else:
            self.data[instance] = self.default()
            return self.data[instance]

