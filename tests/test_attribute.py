import unittest
import attribute
class Temp(object):
        def __init__(self, value):
            self.value = value

class TestGenericAttribute(unittest.TestCase):

    def test_creation(self):

        test = attribute.GenericAttr()
        test = 5

        test2 = attribute.GenericAttr()
        test2 = "lol"
        
        test3 = attribute.GenericAttr()
        test3 =  Temp("class instance")
        
        self.assertEqual(test , 5)
        self.assertEqual(test2 , "lol")
        self.assertEqual(test3.value , "class instance")

    def test_reassignment(self):

        test = attribute.GenericAttr()
        test = 5

        test2 = attribute.GenericAttr()
        test2 = "lol"

        test = "reassign"
        test2= 10
        self.assertEqual(test , "reassign")
        self.assertEqual(test2 , 10)
