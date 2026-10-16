from enum import Enum, auto

class DataPolicy(Enum):
    ImageInt = auto()    
    ImageFloat = auto()  
    ImageBinary = auto()       
    ValueInt = auto()      
    ValueFloat = auto()  
    ArrayFloat = auto()
    ArrayInt = auto()

    @classmethod
    def policies(cls) -> set:
        return {cls.ImageInt, cls.ImageFloat, cls.ImageBinary,
                cls.ValueInt, cls.ValueFloat,
                cls.ArrayInt, cls.ArrayFloat}
                

    # allows resolving of target class from DataType (e.g, can access DataType.ValueInt.to_numpy() as DataType.ValueInt.target_class.to_numpy()
    @property
    def target_class(self):
        from core.type_policies import ImageInt, ImageFloat, ImageBinary, ValueInt, ValueFloat, ArrayInt, ArrayFloat
        
        mapping = {
            DataPolicy.ImageInt: ImageInt,
            DataPolicy.ImageFloat: ImageFloat,
            DataPolicy.ImageBinary: ImageBinary,
            DataPolicy.ValueInt: ValueInt,
            DataPolicy.ValueFloat: ValueFloat,
            DataPolicy.ArrayInt: ArrayInt,
            DataPolicy.ArrayFloat: ArrayFloat
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

