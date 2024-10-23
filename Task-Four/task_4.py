# Import packages and files utilized below 
from segment import Segment
import math
import csv
import matplotlib.pyplot as plt


# Center Trajectory: Approach I
# Need to simplifiy trajectotries and then O(m^2 * n^2) compare them to find minimied trajectory

# Takes in a collection of trajectories T' represented as a dictionary
# With id:points pairs that define its simplified trajectory
# Returns a trajectory in collection of trajectories T s.t. the
# Trajectory minimizes the total distance from all trajectories in T
def center_approach_one(trajectories):
    min_trajectory = ""
    min_trajectory_value = float('inf')
    for traj_one in trajectories.keys(): 
        distance = 0
        for traj_two in trajectories.keys():
            if traj_one != traj_two:
                distance += dtw(trajectories[traj_one], trajectories[traj_two])
        
        if distance < min_trajectory_value:
            min_trajectory_value = distance
            min_trajectory = traj_one
    return trajectories[min_trajectory]


# Center Trajectory: Approach II

# Takes in input of a dictionary of the necessary trajectory values id:points key-value pairs
# Output is a dictionary containing the average y values for each unique x value.
# Returns the dictionary above that contains the centered trajectory
def center_approach_two(trajectories_dict):
    n = len(trajectories_dict)
    total_points = sum(len(points) for points in trajectories_dict.values())
    avg_points = int(total_points / n)

    # Initialize sums and counts lists
    sums = [(0, 0) for _ in range(avg_points)]
    counts = [0 for _ in range(avg_points)]

    # Iterate through trajectories and update sums and counts
    for trajectory in trajectories_dict.values():
        points_count = len(trajectory)
        for i in range(avg_points):
            idx = int(i * (points_count - 1) / (avg_points - 1))
            point = trajectory[idx]
            sums[i] = (sums[i][0] + point[0], sums[i][1] + point[1])
            counts[i] += 1

    # Calculate the central trajectory
    central_trajectory = [(s[0] / c, s[1] / c) for s, c in zip(sums, counts)]

    return central_trajectory



# Methods for distance measuring between trajectories/points
# Code adapted from first three task files

# Euclidean distance calculation
def calculate_distance(A, B):
    x_diff = A[0]-B[0]
    y_diff = A[1]-B[1]
    return math.sqrt(x_diff*x_diff + y_diff*y_diff)

# Dynamic Time Warping (DTW) measuremnet between two trajectories P & Q
# That are represented as a list of tuple (x, y) coordinates
def dtw(P, Q):
    # Start with a minimum distance between all pairs of points
    dist = [[0 for i in range(len(Q))] for j in range(len(P))]
    size = [[0 for i in range(len(Q))] for j in range(len(P))]
    path = [[0 for i in range(len(Q))] for j in range(len(P))]
    
    # For each possible pair of points in P and Q
    for i in range(len(P)): 
        for j in range(len(Q)):
            # Calculate the distance between the points in the pair
            distance = calculate_distance(P[i], Q[j])
            if i > 0 and j > 0:
                # Add the distance to the minimum path to this point
                min_path = min(dist[i-1][j-1], dist[i-1][j], dist[i][j-1])
                if(dist[i-1][j-1] == min_path):
                    path[i][j] = [i-1, j-1]
                    size[i][j] = size[i-1][j-1] + 1
                    dist[i][j] = (distance + min_path)/size[i][j]
                elif(dist[i][j-1] == min_path):
                    path[i][j] = [i, j-1]
                    size[i][j] = size[i][j-1] + 1
                    dist[i][j] = (distance + min_path)/size[i][j]
                elif(dist[i-1][j] == min_path):
                    path[i][j] = [i-1, j]
                    size[i][j] = size[i-1][j] + 1
                    dist[i][j] = (distance + min_path)/size[i][j]
            elif i > 0 and j == 0: #out of bounds check
                path[i][j] = [i-1, j]
                size[i][j] = size[i-1][j] + 1
                dist[i][j] = (distance + dist[i-1][j])/size[i][j]
            elif i == 0 and j > 0: #out of bounds check
                path[i][j] = [i, j-1]
                size[i][j] = size[i-1][j-1] + 1
                dist[i][j] = (distance + dist[i][j-1])/size[i][j]
            else: #out of bounds check
                dist[i][j] = distance
                size[i][j] = 1
                path[i][j] = [i-1, j-1]

    points = [] # Accumulate points in optimal path
    while(i != -1 and j != -1):
        points.append([P[i], Q[j]])
        i = path[i][j][0]
        j = path[i][j][1]

    numerator = 0
    denominator = len(points)
    for x, y in points:
        temp = (calculate_distance(x, y))
        numerator += ((temp)**2)
    return (numerator/denominator)**0.5


# Simplified Trajectory algorithm to enhance scalability
# Takes in an epsilon value (float) and a trajectory T 
# And returns a simplified trajectory as a list of tuples
# Code adapted from Case Study Part I
def TS_greedy(T, my_epsilon):
    
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


# Initialize data for above approaches

# Function to read the CSV file and return a dictionary with trajectory IDs as keys and lists of tuples as values
def read_trajectory_csv(file_name, ids_to_process):
    trajectories = {id: [] for id in ids_to_process}
    
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader)  # Skip the header row
        
        for row in csv_reader:
            id, x, y = row[0], float(row[1]), float(row[2])
            
            if id in ids_to_process:
                trajectories[id].append((x, y))
    
    return trajectories

# Function to read the TXT file with trajectory IDs and return a list of IDs
def read_trajectory_ids(file_name):
    with open(file_name, 'r') as f:
        ids = [id.strip() for id in f.readlines()]
    return ids


if __name__ == "__main__":

    # Paths for data files
    csv_file = '../data/geolife-cars-upd8.csv'
    txt_file = '../data/trajectory-ids.txt'
    
    # Read the TXT file with trajectory IDs
    trajectory_ids_to_process = read_trajectory_ids(txt_file)

    # Builds set from on average O(1) contains ID check
    set_traj = set()
    for id in trajectory_ids_to_process:
        set_traj.add(id)

    # Read the CSV file and build the trajectories dictionary
    # Returns dictionary of ID [(x1, y1), (x2, y2),...] pairs
    trajectories = read_trajectory_csv(csv_file, set_traj)

    '''
    Below Represents Code for raw trajectories for further analysis. 

    Uncomment the below code for data replication utilizing non-simplification with approach I & II
    '''

    # Non-Simplified Centers approach calculations
    approach_1 = center_approach_one(trajectories)
    
    approach_2 = center_approach_two(trajectories)

    # Avg distance from Approach I Center to all other trajectories
    print("Avg distance from Approach 1 to all other Trajectories")
    distance_1 = 0
    for id in trajectories.keys():
        distance_1 += dtw(trajectories[id], approach_1)
    avg_distance_1 = distance_1 / 11
    print("Avg distance via Approach I is: " + str(avg_distance_1))

    # Avg distance from Approach I Center to all other trajectories
    print("Avg distance from Approach 2 to all other Trajectories")
    distance_2 = 0
    for id in trajectories.keys():
        distance_2 += dtw(trajectories[id], approach_2)
    avg_distance_2 = distance_2 / 11
    print("Avg distance via approach II is: " + str(avg_distance_2))
    
    # Plot each of the trajectories in the trajectory-ids.txt
    count = 1
    for i in trajectories.keys():
        # Plot the trajectory 
        value = "Trajectory " + str(count)
        plt.plot([p[0] for p in trajectories[i]], [p[1] for p in trajectories[i]], label=value)
        plt.xlabel('Longitude (degrees)')
        plt.ylabel('Latitude (degrees)')
        plt.title(f'Trajectory Plots')
        plt.legend()
        count += 1

    # Plot centered trajectories
    plt.plot([p[0] for p in approach_1], [p[1] for p in approach_1], '--', label="Center Approach 1", linewidth = 3)
    plt.plot([p[0] for p in approach_2], [p[1] for p in approach_2], label="Center Approach 2")
    plt.legend()
    
    # Show the plot -- All trajectories unsimplified with both plotted approaches
    plt.tight_layout()
    plt.show()


    '''
    Below Represents Code for epsilon simplifications of trajectories for further analysis. 
    Used for repetition of plotting for approach I

    Uncomment the below code for data replication utilizing simplification with approach I
    '''


    # # Get user input to select epsilon value
    # epsilons = input("Which epsilon value: 0.03, 0.1, 0.3? ")
    # if epsilons == "0.03":
    #     ep = 0.03
    # elif epsilons == "0.1":
    #     ep = 0.1
    # elif epsilons == "0.3":
    #     ep = 0.3
    # else:
    #     print("Please select a valid epsilon value")
    #     exit()

    # print("Starting")
    # approach_1 = center_approach_one(trajectories)
    # print("Finished approach 1")


    # # For each id in dic.keys() --> run simplification algo to form new dictionary with simplified trajectory
    # simplified_trajectories = {}
    # for id in trajectory_ids_to_process:
    #     simplified_trajectories[id] = []

    # # Process each trajectory and obtain and assign its 
    # # Simplified trajectory in the same dictionary format
    # for id in simplified_trajectories.keys():
    #     simplification = TS_greedy(trajectories[id], ep)
    #     simplified_trajectories[id] = simplification

    # # Distances from Simplified Approach I Center to all other trajectories
    # print("Distance from Simplified Approach 1 T_Center to all other Trajectories")
    # distance_simp = 0
    # for id in simplified_trajectories.keys():
    #     distance_simp += dtw(simplified_trajectories[id], approach_1)
    # avg_distance_simp = distance_simp / 11
    # print("Avg distance from center trajectory for ep = " + str(ep) +  "is " + str(avg_distance_simp))


    # # Plot each of the simplified trajectories in the trajectory-ids.txt
    # count = 1
    # label = "Simplified Trajectory Plots for " + "Epsilon = " + str(ep)
    # for i in simplified_trajectories.keys():
    #     # Plot the trajectory 
    #     value = "Trajectory " + str(count)
    #     plt.plot([p[0] for p in simplified_trajectories[i]], [p[1] for p in simplified_trajectories[i]], label=value)
    #     plt.xlabel('Longitude (degrees)')
    #     plt.ylabel('Latitude (degrees)')
    #     plt.title(label)
    #     plt.legend()
    #     count += 1

    # # Plot centered trajectory from approach I for a given epsilon 
    # plt.plot([p[0] for p in approach_1], [p[1] for p in approach_1], '--', label='Center Approach I', linewidth = 3, )
    # plt.legend()
    
    # # Show the plot -- All trajectories unsimplified with both plotted approaches
    # plt.tight_layout()
    # plt.show()

    