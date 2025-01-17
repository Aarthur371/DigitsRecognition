import numpy as np

# Type of data associated with an image
class TestData:
    def __init__(self, className, vector, id):
        self.className = className
        self.vector = vector
        self.id = id
    def print(self):
        print("Data belongs to class",self.className,", Name : ",self.id)
        #calculate the distance between the data vector and a given vector
    def distanceTo(self,vect2):
        sum = 0
        if(len(self.vector)!=len(vect2)):
            print("data: "+self.id)
            raise ValueError("Vectors must have the same length !"+str(len(self.vector))+"/"+str(len(vect2)))
        else:
            for i in range(0, len(self.vector)):
                # Calculate the difference between the i-coordinate of the two vectors
                sum += np.power(int(self.vector[i]) - int(vect2[i]), 2)
        return np.sqrt(sum)  # gives the Euclidian distance between vectors