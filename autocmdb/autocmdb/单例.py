class Foo(object):
    _i = None
    def __new__(cls, *args, **kwargs):
        if cls._i:
            return cls._i
        else:
            o = object.__new__(cls, *args, **kwargs)
            cls._i = o
            return cls._i
obj1 = Foo()
print(obj1)
obj2 = Foo()
print(obj2)
