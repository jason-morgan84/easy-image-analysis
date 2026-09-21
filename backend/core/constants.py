from enum import Enum, auto

class DataType(Enum):
    ImageInt = auto()    
    ImageFloat = auto()  
    ImageBinary = auto()       
    ValueInt = auto()      
    ValueFloat = auto()  
    ArrayFloat = auto()
    ArrayInt = auto()

    #categorise DataTypes into image_types, for multi-dimensional arrays, and value_types, for 1d variables.
    @classmethod
    def image_types(cls) -> set:
        return {cls.ImageInt, cls.ImageFloat, cls.ImageBinary}

    @classmethod
    def value_types(cls) -> set:
        return {cls.ValueInt, cls.ValueFloat}

    @classmethod
    def array_types(cls) -> set:
        return {cls.ArrayInt, cls.ArrayFloat}

    @classmethod
    def types(cls) -> set:
        return {cls.ImageInt, cls.ImageFloat, cls.ImageBinary,
                cls.ValueInt, cls.ValueFloat,
                cls.ArrayInt, cls.ArrayFloat}
                

    # allows resolving of target class from DataType (e.g, can access DataType.ValueInt.to_numpy() as DataType.ValueInt.target_class.to_numpy()
    @property
    def target_class(self):
        from core.type import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat, ArrayInt, ArrayFloat
        
        mapping = {
            DataType.ImageInt: ImageInt,
            DataType.ImageFloat: ImageFloat,
            DataType.ImageBinary: ImageBinary,
            DataType.ValueInt: ValueInt,
            DataType.ValueFloat: ValueFloat,
            DataType.ArrayInt: ArrayInt,
            DataType.ArrayFloat: ArrayFloat
        }
        
        cls_ = mapping.get(self)
        if cls_ is None:
            raise NotImplementedError(f"No class mapped for data type: {self.name}")
        return cls_

    # Automatically gets attribute lookups from the underly enum target class
    # ie, can do DataType.ImageInt.numpy rather than DataType.Type.target_class.numpy
    def __getattr__(self, name):
        
       # Prevents infinite recursion during Enum initialization
        if name.startswith("_"):
            raise AttributeError(name)

        # returns attribute if it exists
        target = self.target_class
        if hasattr(target, name):
            return getattr(target, name)

        # otherwise, returns error
        raise AttributeError(f"target class {target.__name__} has no attribute {name}")

    # allows direct instantiation of target_class (ie, can say a = DataType.ValueInt(5) and a will be a member of ValueInt with value = 5)
    def __call__(self, *args, **kwargs):
        return self.target_class(*args, **kwargs)