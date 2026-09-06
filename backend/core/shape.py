import numpy as np

class Shape:

     max_image_dimensions = 4
     min_image_dimensions = 4
     dimension_order = {"c": lambda self: self.c,
                        "z": lambda self: self.z,
                        "y": lambda self: self.y,
                        "x": lambda self: self.x}

     def __init__(self, c, z, y, x):
            self.c = c
            self.z = z
            self.y = y
            self.x = x

     def __iter__(self):
          for item in self.dimension_order.values:
               yield item
     
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

     @property
     def y(self):
          return self._y

     @property
     def x(self):
          return self._x

     @z.setter
     def z(self, z):
          if not isinstance(z, int) and not isinstance(z,np.integer):
               raise TypeError (f"Expected integer, got {type(z)}")
          self._z = z

     @y.setter
     def y(self, y):
          if not isinstance(y, int) and not isinstance(y, np.integer):
               raise TypeError (f"Expected integer, got {type(y)}")
          self._y = y

     @x.setter
     def x(self, x):
          if not isinstance(x, int) and not isinstance(x,np.integer):
               raise TypeError (f"Expected integer, got {type(x)}")
          self._x = x

