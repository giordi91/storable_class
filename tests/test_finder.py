import unittest
import os
from storable_class import finder
from fixtures import classes

fixtures_path1 = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "fixtures"
fixtures_path2 = fixtures_path1 + os.path.sep  + "nested" 
fixtures_path3 = fixtures_path2 + os.path.sep  + "sublevel" 


class TestFinder(unittest.TestCase):

    def setUp(self):

        self.find = finder.Finder()
        self.find.path = fixtures_path1

    def test_finding_avaiable_files(self):
       
        files = self.find.available_files
        self.assertTrue("classes.py" in files)
        self.assertTrue("find_me.py" in files)
        self.assertTrue("me.rm" not in files)
        self.assertTrue("sub_second.py" in files)
        self.assertTrue("nested.py" in files)
        self.assertTrue("nested_skip1.py" in files)
        
        find2 = finder.Finder()
        find2.path = fixtures_path2
        files = find2.available_files
         
        self.assertTrue("nested.py" in files)
        self.assertTrue("nested_skip1.py" in files)
        self.assertTrue("nested_skip2.py" in files)

    def test_auto_update(self):

        files = self.find.available_files
        self.find.path = fixtures_path2
        self.find.auto_update = True 
        files = self.find.available_files

        self.assertTrue("nested.py" in files)
        self.assertTrue("nested_skip1.py" in files)
        self.assertTrue("nested_skip2.py" in files)
        
        self.find.path = fixtures_path3
        files = self.find.available_files
        
        self.assertTrue("me.rm" not in files)
        self.assertTrue("sub_second.py" in files)

    def test_folders_to_exclude(self):
        
        self.find.folders_to_esclude.append("sublevel")
        self.find.auto_update=True
        files = self.find.available_files
        
        self.assertTrue("classes.py" in files)
        self.assertTrue("find_me.py" in files)
        self.assertTrue("me.rm" not in files)
        self.assertTrue("sub_second.py" not in files)
        self.assertTrue("sub.py" not in files)
        self.assertTrue("nested.py" in files)
        self.assertTrue("nested_skip1.py" in files)

        self.find.folders_to_esclude.append("nested")
        files = self.find.available_files
        
        self.assertTrue("classes.py" in files)
        self.assertTrue("find_me.py" in files)
        self.assertTrue("me.rm" not in files)
        self.assertTrue("sub_second.py" not in files)
        self.assertTrue("sub.py" not in files)
        self.assertTrue("nested.py" not in files)
        self.assertTrue("nested_skip1.py" not in files)

    def test_files_to_exclude(self):
        
        self.find.files_to_exclude.append("__init__.py")
        self.find.files_to_exclude.append("classes.py")
        self.find.auto_update=True

        files = self.find.available_files
        self.assertTrue("classes.py" not in files)
        self.assertTrue("find_me.py" in files)
        self.assertTrue("me.rm" not in files)
        self.assertTrue("sub_second.py"  in files)

    def test_files_dict(self):

        files= self.find.files_dict
        self.assertTrue("nested_skip2.py"  in files)
        self.assertTrue("classes.py"  in files)
        self.assertTrue("sub.py"  in files)

        p = fixtures_path3 + os.path.sep + "sub_second.py"
        self.assertTrue(files["sub_second.py"] == p)
        p = fixtures_path2 + os.path.sep + "nested_skip2.py"
        self.assertTrue(files["nested_skip2.py"] == p)
        
        p = fixtures_path1 + os.path.sep + "classes.py"
        self.assertTrue(files["classes.py"] == p)
    
    def test_modules_dict(self):
        
         
        modules= self.find.modules_dict
        
        self.assertTrue("NestedSkip2"  in modules)
        self.assertTrue("SubSecond"  in modules)
        self.assertTrue("Nested"  in modules)

    def test_module_to_class_name(self):


        self.assertTrue("NestedSkip2" == self.find.module_to_class_name("nested_skip_2"))
        self.assertTrue("Nested" == self.find.module_to_class_name("nested"))
        self.assertTrue("Sub" == self.find.module_to_class_name("sub"))

