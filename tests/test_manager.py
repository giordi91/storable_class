import unittest
import os
from storable_class import manager 
from storable_class import finder
from storable_class.tests.fixtures.nested import nested

fixtures_path1 = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "fixtures"

class TestManager(unittest.TestCase):
    def setUp(self):

        self.find = finder.Finder()
        self.find.path = fixtures_path1
        
        self.manager = manager.Manager()
    def test_instance_from_string(self):

        cl = self.manager.instance_from_string("Nested",self.find)
        
        self.assertTrue(cl != None)
        self.assertTrue(cl.__class__.__name__, "Nested")

