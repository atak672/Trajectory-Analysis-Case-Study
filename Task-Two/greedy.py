# Goal: Implement the greedy algorithm TS-greedy(T,ε) to compute an ε-simplification of T.

# Import necessary packages
from segment import Segment
import matplotlib.pyplot as plt
import csv

# Implement the TS-greedy algorithm by computing an epsilon-simplification of a given polygonal line T
def TS_greedy(T, my_epsilon):
    
    # find the point farthest from the line segment formed by the first and last points
    segment = Segment(*T[0], *T[-1])
    
    max_dist = 0
    max_index = 0
    for i in range(1, len(T)-1):
        dist = segment.minDistanceFromPoint(*T[i])
        if dist > max_dist:
            max_dist = dist
            max_index = i
    
    # if the farthest point is within the error tolerance, return the endpoints of the trajectory
    if max_dist <= my_epsilon:
        return [T[0], T[-1]]
    
    # recursively simplify the sub-trajectories before and after the farthest point
    left_T = T[:max_index+1]
    right_T = T[max_index:]
    left_simplification = TS_greedy(left_T, my_epsilon)
    right_simplification = TS_greedy(right_T, my_epsilon)
    
    # combine the simplified sub-trajectories
    return left_simplification[:-1] + right_simplification


def read_pairs(pairId1):
    file = "../Data/geolife-cars.csv"
    pointsA = []
    with open(file, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for line in csvreader:
            if(line[1] == pairId1):
                x, y = float(line[2]), float(line[3])
                pointsA.append([x, y])
    return pointsA


def multipleEpsilons():
    # GOAL: Plot the trajectory ID 128-20080503104400 and its simplification using the above function forε = 0.03,0.1,0.3 (kilometers). Each figure should contain two line plots: trajectory and itssimplification, with markers of different colors.


    # Load the trajectory data from the CSV file
    # NEED TO ADD CODE ON HOW TO DO THIS

    # Convert the data to a list of tuples of floats???
    
    points = read_pairs('128-20080503104400')

    # Define the values of epsilon to use
    epsilons = [0.03, 0.1, 0.3]

    # Plot the trajectory and its simplification for each value of epsilon
    for i, my_epsilon in enumerate(epsilons):
        # Compute the simplification using the TS_greedy function
        simplification = TS_greedy(points, my_epsilon)
        
        # Plot the trajectory and its simplification
        plt.subplot(1, len(epsilons), i+1, aspect='equal')
        plt.plot([p[0] for p in points], [p[1] for p in points], 'bo-', label='Trajectory')
        plt.plot([p[0] for p in simplification], [p[1] for p in simplification], 'rx-', label='Simplification')
        plt.xlabel('Longitude (degrees)')
        plt.ylabel('Latitude (degrees)')
        plt.title(f'Trajectory ID 128-20080503104400, epsilon={my_epsilon} km')
        plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


def multipleTrej():
# GOAL: Evaluate and report the compression ratio |T |/|T ′| for trajectories 128-20080503104400,010-20081016113953, 115-20080520225850, and 115-20080615225707 using TS-greedy forε = 0.03km.

    # Define the value of epsilon
    my_epsilon = 0.03

    # Define the list of trajectory IDs to process
    trajectory_ids = ['128-20080503104400', '010-20081016113953', '115-20080520225850', '115-20080615225707']

    # Process each trajectory
    for trajectory_id in trajectory_ids:
        # Load the trajectory data from the CSV file
        points = read_pairs(trajectory_id)

        # Compute the simplification using the TS_greedy function
        simplification = TS_greedy(points, my_epsilon)

        # Compute the compression ratio
        compression_ratio = len(points) / len(simplification)

        # Print the results
        print(f'Trajectory ID: {trajectory_id}')
        print(f'Original points: {len(points)}')
        print(f'Simplified points: {len(simplification)}')
        print(f'Compression ratio: {compression_ratio:.2f}\n')


if __name__ == "__main__":
    # print(len(read_pairs('128-20080503104400')))
    multipleTrej()
    multipleEpsilons()

