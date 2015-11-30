from storable_class import container 
from storable_class import attribute 


class TestClass(container.Container):

    test = attribute.GenericAttr()
    test2 = attribute.GenericAttr()
    test3 = attribute.GenericAttr()
    test4 = attribute.TypedAttr(["float"],10.0)

class ChildClass(TestClass):

    child1= attribute.TypedAttr(["float"],10.0)
    child2= attribute.TypedAttr(["int"],5)
    child3= attribute.TypedAttr(["bool"],False)


