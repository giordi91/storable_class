#!/apps/Linux64/aw/maya2014-x64-sp2/bin/mayapy

import sys,os
'''
if env_settings.ROOT_PATH in sys.path :
    sys.path.append(env_settings.ROOT_PATH) 
import env_settings
import autorig_settings
'''
import unittest
#import maya.standalone



def main():
    #maya.standalone.initialize(name='python')
    loader = unittest.TestLoader()
    #autorig_settings.testsPath,
    test_path =os.path.abspath(__file__).rsplit(os.path.sep,1)[0] + "/tests" 
    tests = loader.discover(test_path,  'test_*.py' )
    testRunner = unittest.runner.TextTestRunner(verbosity=2)

    #formatting 
    print "\n"
    print "----------------------------------------------------------------------"
    testRunner.run(tests)

if __name__ == "__main__" :
    main()
