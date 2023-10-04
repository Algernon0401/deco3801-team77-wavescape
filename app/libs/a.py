# class Test():
#     def __init__(self, a):
#         self.a = a
    
#     def __eq__(self, other):
#         return self.a == other.a and type(self) == type(other)

# class sdf(Test):
#     def __init__(self, a):
#         super().__init__(a)
    
# a = Test(1)
# b = sdf(1)
# print(a==b)

import numpy as np
import math
a = (0, 0)
b = (1, 3)
d = math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) 

r = np.arccos((abs(b[0]-a[0]))/d)
print(r*180/math.pi)