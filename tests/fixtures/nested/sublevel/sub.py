from storable_class import container 
from storable_class import attribute 


class Sub(container.Container):

    test = attribute.GenericAttr()
    test2 = attribute.GenericAttr()
    test3 = attribute.GenericAttr()
    test4 = attribute.TypedAttr(["float"],10.0)


