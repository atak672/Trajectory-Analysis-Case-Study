import math
import matplotlib.pyplot as plt
import csv

class Segment:
    
    '''
    This is simply a copy of code from Task_Two folder
    
    This algorithm utilizes an initialized line segment using xy points. And minDistanceFromPoint is used by the Segment class
    to calculate the minimum distance from itself to a point q.
    
    If a line starts at point a, x1 is the
    x coordinate of a and y1 is the y coordinate of a.
    
    And if the line ends at b, x2 is the x coordinate of b
    and y2 is the y coordinate of b.
    
    Now that we have a class which signifies a segment, minDistanceFromSeg calcualtes the minimum distance between the line segment
    and a point q (with coordiantes qx and qy on the xy plane). It then returns the minimum distance. 
    '''
   
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        
    def minDistanceFromPoint(self,qx,qy):
        v = (self.x2-self.x1, self.y2-self.y1)  # Vector representing line segment, which is v = (x2-x1, y2-y1)
        u = (qx-self.x1, qy-self.y1)            # Vector from start point of the line segment to the point q, which is u = (qx-x1, qy-y1)
        
        vu = v[0]*u[0] + v[1]*u[1]              # Calculate dot product of vectors v and u, which is v·u = (x2-x1)(qx-x1) + (y2-y1)(qy-y1)
        vv = v[0]*v[0] + v[1]*v[1]              # Calculate squared length of vector v, which is v·v = (x2-x1)^2 + (y2-y1)^2
        if vv == 0:
            return 0
        t = vu / vv                             # Calculate parameter t = v·u / v·v, which represents position of projection of point q on the line
        
        
        # Calculate the coordinates of q' which I named qx_proj, qy_proj
        # t is used to determine if it is better to calculate distance from projection or end points
        if t < 0:
            qx_proj, qy_proj = self.x1, self.y1
        elif t > 1:
            qx_proj, qy_proj = self.x2, self.y2
        else:
            qx_proj, qy_proj = self.x1 + t*(self.x2-self.x1), self.y1 + t*(self.y2-self.y1)
        
        
        d = ((qx-qx_proj)**2 + (qy-qy_proj)**2)**0.5 # d is the distance between the point q and its projection (q') on the line
        return d 
        
    # Define the distance
    def dist(self):

        # Calculate the Euclidean distance between two points
        return math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)
        
# Implement the TS-greedy algorithm by computing an epsilon-simplification of a given polygonal line T
def TS_greedy(T, my_epsilon):

   # Add the first point of T to the simplified polygonal line
    if len(T) < 3:
        return T
    
    # Find the point farthest from the line segment formed by the first and last points
    segment = Segment(*T[0], *T[-1])
    
    max_dist = 0
    max_index = 0
    for i in range(1, len(T)-1):
        dist = segment.minDistanceFromPoint(*T[i])
        if dist > max_dist:
            max_dist = dist
            max_index = i
    
    # If the farthest point is within the error tolerance, return the endpoints of the trajectory
    if max_dist <= my_epsilon:
        return [T[0], T[-1]]
    
    # Recursively simplify the sub-trajectories before and after the farthest point
    left_T = T[:max_index+1]
    right_T = T[max_index:]
    left_simplification = TS_greedy(left_T, my_epsilon)
    right_simplification = TS_greedy(right_T, my_epsilon)
    
    # Combine the simplified sub-trajectories
    return left_simplification[:-1] + right_simplification


def read_pairs(pairId1):
    file = "./Data/geolife-cars.csv"
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
    # GOAL: Plot the trajectory ID 128-20080503104400 and its simplification using the above function forε = 0.03,0.1,0.3 (kilometers). 
    # Each figure should contain two line plots: trajectory and itssimplification, with markers of different colors.


    # Load the trajectory data from the CSV file

    # Convert the data to a list of tuples of floats
    
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
    