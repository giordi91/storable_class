import unittest

from storable_class import attribute

class Temp(object):
        def __init__(self, value):
            self.value = value

class TestGenericAttribute(unittest.TestCase):

    def test_creation(self):

        class TestClass(object):

            test = attribute.GenericAttr()
            test2 = attribute.GenericAttr()
            test3 = attribute.GenericAttr()

        tmp = TestClass() 
        tmp.test = 5
        tmp.test2 = "foo"
        tmp.test3 =  Temp("class instance")
        
        self.assertEqual(tmp.test , 5)
        self.assertEqual(tmp.test2 , "foo")
        self.assertEqual(tmp.test3.value , "class instance")

    def test_reassignment(self):

        class TestClass(object):
            test = attribute.GenericAttr()
            test2 = attribute.GenericAttr()
        
        tmp = TestClass() 
        tmp.test = 5
        tmp.test2 = "foo"

        tmp.test = "reassign"
        tmp.test2= 10

        self.assertEqual(tmp.test , "reassign")
        self.assertEqual(tmp.test2 , 10)


class TestTypedAttribute(unittest.TestCase):

    def test_creation(self):
        
        class TestClass(object):
            test = attribute.TypedAttr(["int"])
            test2 = attribute.TypedAttr(["str"])
            test3 = attribute.TypedAttr(["Temp"])

        tmp = TestClass() 
        tmp.test = 5
        tmp.test2 = "foo"
        tmp.test3 =  Temp("class instance")
        
        self.assertEqual(tmp.test , 5)
        self.assertEqual(tmp.test2 , "foo")
        self.assertEqual(tmp.test3.value , "class instance")

    def test_default(self):
        

        #llooks like that descriptor is not triggered properly if first is not set
        #so we need to set it in a class
        class TestClass(object):

            test = attribute.TypedAttr(["int"], 12)
            test2 = attribute.TypedAttr(["str"], "fooBar")
            test3 = attribute.TypedAttr(["Temp"])
            test4 = attribute.TypedAttr(["float"], 12.0)
        
        tmp = TestClass()

        self.assertEqual(tmp.test , 12)
        self.assertEqual(tmp.test2 , "fooBar")
        self.assertEqual(tmp.test3 , None)
        self.assertEqual(tmp.test4 , 12.0)

    
    def test_multiple_values(self):

        class TestClass(object):
            test = attribute.TypedAttr(["int","float"])
            test2 = attribute.TypedAttr(["str","bool"])

        tmp = TestClass()
        tmp.test = 5
        tmp.test2 = "foo"
        
        self.assertEqual(tmp.test , 5)
        self.assertEqual(tmp.test2 , "foo")

        tmp.test = 12.23
        tmp.test2 = False;
        self.assertEqual(tmp.test , 12.23)
        self.assertEqual(tmp.test2 , False)
        
        #here we get an hold of the descriptor, in order to avoid it to trigger
        #the value setter or getter we access it trough the class definition dict
        #and we get an hold to the function __set__
        descript = TestClass.__dict__["test"].__set__
        descript2 = TestClass.__dict__["test2"].__set__
        
        self.assertRaises(ValueError, descript, self,False)
        self.assertRaises(ValueError, descript2, self, 12.2)

