import unittest
import tempfile
import os

from storable_class import attribute
from storable_class import container
from storable_class import finder 
from fixtures.test_class import TestClass 
from fixtures.child_class import ChildClass 
from fixtures.test_nested_class import TestNestedClass
#Fixtures
fixtures_path1 = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "fixtures"



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
    
    def test_recursive_class_load_data(self):
        
        #this test just asserts it works and no error are thrown, later if we 
        #add errors throwing if class not in finder we will try to catch it

        t = TestNestedClass()
        t.testNest = TestNestedClass()
        t.testNest.testNest = TestClass()

        find = finder.Finder()
        find.path = fixtures_path1
        data = t.get_data()
        t.set_data(data, find)
    
    def test_recursive_class_load_data_values(self):

        t = TestNestedClass()
        t.testNest = TestNestedClass()
        t.testNest.testNest = TestClass()
        
        t.test2 = "foo"
        t.test4 = 11.1
        t.testNest.test = False
        t.testNest.test4 = 1234.345
        t.testNest.testNest.test4= 8.1
        t.testNest.testNest.test2= 1
        t.testNest.testNest.test3= True 

        find = finder.Finder()
        find.path = fixtures_path1
        data = t.get_data()
        
        
        t.test2 = "bar"
        t.test4 = 0.1
        t.testNest.test = True 
        t.testNest.test4 = 9999.9 
        t.testNest.testNest.test4= 4.9 
        t.testNest.testNest.test2= 82 
        t.testNest.testNest.test3 = False 
        
        t.set_data(data, find)

        self.assertTrue(t.test2 == "foo")
        self.assertTrue(t.test4 ==  11.1)
        self.assertTrue(t.testNest.test == False)
        self.assertTrue(t.testNest.test4 == 1234.345)
        self.assertTrue(t.testNest.testNest.test4 == 8.1)
        self.assertTrue(t.testNest.testNest.test2 == 1)
        self.assertTrue(t.testNest.testNest.test3 == True)
