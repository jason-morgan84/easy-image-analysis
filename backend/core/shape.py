import numpy as np
import copy

"""Shape class exists to hold data related to the shape of transmitted images. """
class Shape:
# defines acceptable dimensions and default order
     max_image_dimensions = 4
     min_image_dimensions = 4

     dimensions = ('c','z','y','x')

     # arguements in __init_ must equal dimensions above
     # in future, consider change to kwargs to remove hardcoded dimensions
     def __init__(self, c, z, y, x):
            self.c = c
            self.z = z
            self.y = y
            self.x = x

     def __iter__(self):
        for dimension in self.dimensions:
             yield getattr(self, dimension)

     # allows getitem or setitem by dimension name or by dimension index
     def __getitem__(self, key):
          if isinstance(key, int):
               return getattr(self, self.dimensions[key])
          elif isinstance(key, str):
               return getattr(self, key.lower())
          else:
               raise TypeError("Key must be an integer index or a string identifier")

     def __setitem__(self, key, value):
          if isinstance(key, int):
               setattr(self,self.dimensions[key],value)
          elif isinstance(key, str):
               setattr(self,key,value)
          else:
               raise TypeError("Key must be an integer index or a string identifier")

     def __copy__(self):
          return Shape(self.c,self.z,self.y,self.x)

     def copy(self):
        return copy.copy(self)

     # translates back and forward between dimension name and dimension index
     @classmethod
     def to_name(cls, index: int) -> str:
        return cls.dimensions[index]

     @classmethod
     def to_index(cls, name: str) -> int:
        return cls.dimensions.index(name.lower())

     def __str__(self):
          return str((self.c,self.z,self.y,self.x))

     # for each arguement, checks its an integer
     @property
     def c(self):
          return self._c
     @c.setter
     def c(self, c):
          if not isinstance(c, int) and not isinstance(c,np.integer):
               raise TypeError (f"Expected integer, got {type(c)}")
          self._c = c

     @property
     def z(self):
          return self._z
     @z.setter
     def z(self, z):
          if not isinstance(z, int) and not isinstance(z,np.integer):
               raise TypeError (f"Expected integer, got {type(z)}")
          self._z = z

     @property
     def y(self):
          return self._y
     @y.setter
     def y(self, y):
          if not isinstance(y, int) and not isinstance(y, np.integer):
               raise TypeError (f"Expected integer, got {type(y)}")
          self._y = y


     @property
     def x(self):
          return self._x
     @x.setter
     def x(self, x):
          if not isinstance(x, int) and not isinstance(x,np.integer):
               raise TypeError (f"Expected integer, got {type(x)}")
          self._x = x






