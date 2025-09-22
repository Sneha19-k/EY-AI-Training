import numpy as np

marks= np.array([80,90,70])
print("max marks:", marks.max())
print("min marks:", marks.min())
print("Average marks:", marks.mean())

data= np.array([10,20,30,40,50])

print("first 3 elements: ",data[:3])    #slicing
print("reversed", data[::-1])
print("sum", np.sum(data))
print("standard deviation", np.std(data))
