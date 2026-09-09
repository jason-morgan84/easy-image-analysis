from enum import Enum, auto

class DataType(Enum):
    ImageInt = auto()    
    ImageFloat = auto()  
    ImageBinary = auto()       
    ValueInt = auto()      
    ValueFloat = auto()  

    #categorise DataTypes into image_types, for multi-dimensional arrays, and value_types, for 1d variables.
    @classmethod
    def image_types(cls) -> set:
        return {cls.ImageInt, cls.ImageFloat, cls.ImageBinary}

    @classmethod
    def value_types(cls) -> set:
        return {cls.ValueInt, cls.ValueFloat}

    # allows resolving of target class from DataType (e.g, can access DataType.ValueInt.to_numpy() as DataType.ValueInt.target_class.to_numpy()
    @property
    def target_class(self):
        from core.type import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat
        
        mapping = {
            DataType.ImageInt: ImageInt,
            DataType.ImageFloat: ImageFloat,
            DataType.ImageBinary: ImageBinary,
            DataType.ValueInt: ValueInt,
            DataType.ValueFloat: ValueFloat,
        }
        
        cls_ = mapping.get(self)
        if cls_ is None:
            raise NotImplementedError(f"No class mapped for data type: {self.name}")
        return cls_

    # gets to numpy class variable using DataType.Type.numpy rather than DataType.Type.target_class.numpy
    @property
    def numpy(self):
        return self.target_class.numpy

    # allows direct instantiation of target_class (ie, can say a = DataType.ValueInt(5) and a will be a member of ValueInt with value = 5)
    def __call__(self, *args, **kwargs):
        return self.target_class(*args, **kwargs)