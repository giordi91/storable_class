
import unittest

from storable_class import attribute
from storable_class import container


#Fixtures
class TestClass(container.Container):

    test = attribute.GenericAttr()
    test2 = attribute.GenericAttr()
    test3 = attribute.GenericAttr()
    test4 = attribute.TypedAttr(["float"],10.0)

class ChildClass(TestClass):

    child1= attribute.TypedAttr(["float"],10.0)
    child2= attribute.TypedAttr(["int"],5)
    child3= attribute.TypedAttr(["bool"],False)

class TestGenericAttribute(unittest.TestCase):

    def test_get_data_attribute(self):

        data = TestClass().get_data()
        self.assertTrue("test" in data)
        self.assertTrue("test2" in data)
        self.assertTrue("test3" in data)
        self.assertTrue("test4" in data)

    def test_get_data_attribute_inherited(self):
        
        
        data = ChildClass().get_data()
        self.assertTrue("test" in data)
        self.assertTrue("test2" in data)
        self.assertTrue("test3" in data)
        self.assertTrue("test4" in data)
        self.assertTrue("child1" in data)
        self.assertTrue("child2" in data)
        self.assertTrue("child3" in data)

    def test_get_data_attribute_value(self):
        
        
        inst = ChildClass()
        data = inst.get_data()
        self.assertTrue(data["test"] == None)
        self.assertTrue(data["child3"] == False)
        self.assertTrue(data["child1"] == 10.0)
        self.assertTrue(data["test4"] == 10.0)
        self.assertTrue(data["type"] == inst.__class__.__name__)


    def test_set_data(self):
        pass 

    def test_get_attributes(self):

        attrs = ChildClass.get_attrs()

        self.assertTrue("test" in attrs)
        self.assertTrue("test2" in attrs)
        self.assertTrue("child1" in attrs)
        self.assertTrue("child3" in attrs)

    def test_save_load_class(self):
        pass
    
    
