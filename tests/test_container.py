import unittest

from storable_class import attribute
from storable_class import container

import tempfile
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
        t= TestClass() 

        data={"test": "x", "test2": 1, "test3" : False, "test4": 1.0}
        t.set_data(data)

        self.assertTrue(data["test"] == "x")
        self.assertTrue(data["test2"] == 1)
        self.assertTrue(data["test3"] == False)
        self.assertTrue(data["test4"] == 1.0)

    def test_get_attributes(self):

        attrs = ChildClass.get_attrs()

        self.assertTrue("test" in attrs)
        self.assertTrue("test2" in attrs)
        self.assertTrue("child1" in attrs)
        self.assertTrue("child3" in attrs)

    def test_save_load_class(self):
         
        t= TestClass() 
        t.test = "x"
        t.test2 = False
        t.test3 = 2
        t.test4 = 22234.342

        temp_f = tempfile.NamedTemporaryFile(delete =False)
        t.save(temp_f.name)

        t2 = TestClass()
        t2.load(temp_f.name)


        self.assertTrue(t.test == t2.test)
        self.assertTrue(t.test2 == t2.test2)
        self.assertTrue(t.test3 == t2.test3)
        self.assertTrue(t.test4 == t2.test4)
        
        #no need for explicit closing of the file, will be done automatically when
        #out of scope but just to clean up after myself i will do it
        temp_f.close()

    def test_recursive_class_extract_data(self):

        class TestNestedClass(container.Container):

            test = attribute.GenericAttr()
            testNest = attribute.GenericAttr()
            test2 = attribute.GenericAttr()
            test3 = attribute.GenericAttr()
            test4 = attribute.TypedAttr(["float"],10.0)

        t = TestNestedClass()
        t.testNest = TestNestedClass()
        t.testNest.testNest = TestClass()

        data = t.get_data()
        container_key = container.Container.__dict__["__CONTAINER_KEYWORD__"] 
        self.assertTrue(type(data["testNest"]) is dict)
        self.assertTrue(container_key in data["testNest"].keys())
        self.assertTrue(type(data["testNest"]["testNest"]) is dict)
        self.assertTrue(container_key in data["testNest"]["testNest"].keys())

        self.assertTrue(type(data["testNest"]["testNest"]) is dict)
        self.assertTrue(container_key in data["testNest"]["testNest"].keys())
        self.assertTrue(data["testNest"]["testNest"]["type"] == "TestClass")



