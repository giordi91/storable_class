from storable_class import container
from storable_class import attribute 
from test_class import TestClass


class ChildClass(TestClass):

    child1= attribute.TypedAttr(["float"],10.0)
    child2= attribute.TypedAttr(["int"],5)
    child3= attribute.TypedAttr(["bool"],False)

def get_instance():
    return ChildClass()
