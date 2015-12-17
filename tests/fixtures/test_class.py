from storable_class import container
from storable_class import attribute 


class TestClass(container.Container):

    test = attribute.GenericAttr()
    test2 = attribute.GenericAttr()
    test3 = attribute.GenericAttr()
    test4 = attribute.TypedAttr(["float"],10.0)


def get_instance():
    return TestClass()
