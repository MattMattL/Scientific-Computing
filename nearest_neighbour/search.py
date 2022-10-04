import numpy as np
import matplotlib.pyplot as plt


def generate_point_cloud(n:int, d:int = 2, seed=1234) -> np.ndarray:
    """Generates an array of d dimensional points in the range of [0, 1). The function generates n points. The result is stored in a n x d numpy array. 

    Args:
        n (int): The number of discrete points to generate.
        d (int, optional): The dimensionality of each point. Defaults to 2.
        seed (int, optional): The random seed used to generate the array. Defaults to 1234.

    Returns:
        np.ndarray: An n x d array of random numbers, whose coordinates are uniformly generated between [0, 1).
    """
    initial_seed = np.random.get_state()
    np.random.seed(seed)
    points = np.random.rand(n, d)
    np.random.set_state(initial_seed)
    return points


def find_nearest_neighbour_from_point(point_cloud:np.ndarray, point:int) -> int:

    minDistIndex = 1 if point == 0 else 0 # index of the nearest neighbour
    minDistSquared = 0 # distance to the nearest neighbour

    # initialise mininum distance squared with the first or second point
    for j in range(point_cloud.shape[1]):
        minDistSquared += (point_cloud[point][j] - point_cloud[minDistIndex][j]) ** 2
    
    # iterate over all points except itself
    for i in range(point_cloud.shape[0]):

        if i == point:
            continue
        
        # calculate the sum of distance squared for a single point
        distSquared = 0

        for j in range(point_cloud.shape[1]):
            distSquared += (point_cloud[point][j] - point_cloud[i][j])**2

        # update variables if the point is the closest so far
        if distSquared < minDistSquared:
            minDistSquared = distSquared
            minDistIndex = i

    return minDistIndex


def find_all_nearest_neighbours(point_cloud:np.ndarray) -> np.ndarray:

    # initialise a one dimentional array
    result = np.empty(point_cloud.shape[0], dtype=int)

    # call 'find_nearest_neighbour_from_point' for each point
    for i in range(point_cloud.shape[0]):
        result[i] = find_nearest_neighbour_from_point(point_cloud, i)

    return result
