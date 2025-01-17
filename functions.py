import os.path
import numpy as np
from PIL import Image
from testData import TestData

#-------------VARIABLES------------------
neighbors = []
data = []

#---------FUNCTIONS DEFINITION-----------

def image_to_vector(image_name,path):
    # Get the path of this script
    current_dir = os.path.dirname(__file__)
    # Create the path of the image
    image_path = os.path.join(current_dir, path, image_name)
    # Open the image file
    img = Image.open(image_path)
    # Resize the image to 16x16 using bilinear interpolation
    img = img.resize((16, 16), Image.BILINEAR)
    # Convert the image to grayscale
    img = img.convert('L')
    # Apply threshold to create a binary image
    threshold = 128
    img = img.point(lambda p: p > threshold and 255) #<threshold : 0 / >threshold : 255
    # Convert the image to a numpy array
    img_array = np.array(img)
    img_array = (img_array >= threshold).astype(np.uint8)  # <threshold : 0 / >threshold : 1
    # Flatten the array to create a vector
    img_vector = img_array.flatten()

    return img_vector

def distance(vec1, vec2):
    sum = 0
    for i in range (0,len(vec1)):
        # Calculate the difference between the i-coordinate of the two vectors
        sum += np.power(int(vec2[i]) - int(vec1[i]),2)
    return np.sqrt(sum) #gives the Euclidian distance between vectors

# Gives index of the greatest distance to vector "vect" inside data represented by testData objects
def longestDistance(data, vect):
    max=-10000
    index=-1
    i=0
    for d in data:
        val = d.distanceTo(vect)
        if(val>max):
            max=val #new max
            index = i
        i+=1
    return index, max

# Returns the last index used for data nb in data
def data_index(nb):
    i=0 #index counter
    exists=True
    while(exists):
        if os.path.exists("data/" + str(nb) + "data" + str(i) +".png"):
            i += 1
        else:
            exists=False
    return i

# Find the number of data for each figure and return the minimum
def find_min_data_index(fig):
    min = 10000
    for nb in range(fig):
        if(data_index(nb)<min):
            min=data_index(nb)
    return min

def find_neighbors(j,k,figures,testVector):
    data.clear()
    neighbors.clear()
    for n in range(0, figures):  # data from figure 0 to the last figure in the database
        for i in range(0, j):  # j data per figure
            # Generate the image name
            img_name = str(n) + "data" + str(i) + ".png"
            # Transform image to vector
            imgVector2 = image_to_vector(img_name, "data")
            # Create a testData object with info about this data
            data.append(TestData(str(n), imgVector2, img_name))
    initVect = [1000] * (16*16) # vector with big values, will be replaced by real data
    # Initialize the array of neighbors with fake data
    for i in range(0, k):
        neighbors.append(TestData("null", initVect, "init"))
    for d in data:
        #print(d.distanceTo(testVector))
        index, max = longestDistance(neighbors, testVector)  # gives info on the farest neighbor
        if (d.distanceTo(testVector) < max):  # if distance is inf. to farest neighbor
            del neighbors[index]  # delete farest neighbor
            neighbors.append(d)  # add the new neighbor
    return neighbors

def print_result(neighbors,figures):
    counters = [0]*figures #counter for occurences of each figure in the neighborhood
    for n in neighbors:
        for nb in range (figures):
            if (n.className==str(nb)):
                counters[nb]+=1
                break
    return counters.index(max(counters)) #return the figure with the highest occurence


def print_vector(vector):
    i = 0
    # Display a vector in rows of 32 elements
    for i in range(0, 32):
        print("")
        print(vector[0 + i:32 + i])
        i += 1