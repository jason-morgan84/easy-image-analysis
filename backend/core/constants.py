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

    def __call__(self, *args, **kwargs):
        from core.type import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat
        
        mapping = {
            DataType.ImageInt: ImageInt,
            DataType.ImageFloat: ImageFloat,
            DataType.ImageBinary: ImageBinary,
            DataType.ValueInt: ValueInt,
            DataType.ValueFloat: ValueFloat,
        }
        
        target_class = mapping.get(self)
        if target_class is None:
            raise NotImplementedError(f"No class mapped for data type: {self.name}")
            
        return target_class(*args, **kwargs)