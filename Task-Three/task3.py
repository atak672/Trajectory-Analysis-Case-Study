import math
import csv
from matplotlib import pyplot as plt
import task2

# Euclidean distance calculation
def calculate_distance(A, B):
    x_diff = A[0]-B[0]
    y_diff = A[1]-B[1]
    return math.sqrt(x_diff*x_diff + y_diff*y_diff)


# Intuition: walking your dog on path Q and you're on path P, how long is the leash (maximum distance on minimum distance path)
def fd(P, Q):
    #start with a minimum distance between all pairs of points
    dist = [[0 for i in range(len(Q))] for j in range(len(P))]
    path = [[0 for i in range(len(Q))] for j in range(len(P))]
    
    #for each possible pair of points in P and Q
    for i in range(len(P)): 
        for j in range(len(Q)):
            # calculate the distance between the points in the pair
            distance = calculate_distance(P[i], Q[j])
            if i > 0 and j > 0:
                # choose the maximum distance on the minimum path to this point
                min_path = min(dist[i-1][j-1], dist[i-1][j], dist[i][j-1])
                dist[i][j] = max(distance, min_path)
                if(dist[i-1][j-1] == min_path):
                    path[i][j] = [i-1, j-1]
                elif(dist[i][j-1] == min_path):
                    path[i][j] = [i, j-1]
                elif(dist[i-1][j] == min_path):
                    path[i][j] = [i-1, j]
            elif i > 0 and j == 0: #out of bounds check
                dist[i][j] = max(dist[i-1][0], distance)
                path[i][j] = [i-1, j]
            elif i == 0 and j > 0: #out of bounds check
                dist[i][j] = max(dist[0][j-1], distance)
                path[i][j] = [i, j-1]
            else: #out of bounds check
                dist[i][j] = distance
                path[i][j] = [i-1, j-1]

    points = [] # accumulate points in optimal path
    while(i != -1 and j != -1):
        points.append([P[i], Q[j]])
        i = path[i][j][0]
        j = path[i][j][1]
    return points


def dtw(P, Q):
    #start with a minimum distance between all pairs of points
    dist = [[0 for i in range(len(Q))] for j in range(len(P))]
    size = [[0 for i in range(len(Q))] for j in range(len(P))]
    path = [[0 for i in range(len(Q))] for j in range(len(P))]
    
    #for each possible pair of points in P and Q
    for i in range(len(P)): 
        for j in range(len(Q)):
            # calculate the distance between the points in the pair
            distance = calculate_distance(P[i], Q[j])
            if i > 0 and j > 0:
                # add the distance to the minimum path to this point
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

    points = [] # accumulate points in optimal path
    while(i != -1 and j != -1):
        points.append([P[i], Q[j]])
        i = path[i][j][0]
        j = path[i][j][1]
    return points


#CSV function that reads the given pairs from the csv
def read_pairs(pairId1, pairId2):
    file = "../Data/geolife-cars.csv"
    pointsA = []
    pointsB = []
    with open(file, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for line in csvreader:
            if(line[1] == pairId1):
                x, y = float(line[2]), float(line[3])
                pointsA.append([x, y])
            elif(line[1] == pairId2):
                x, y = float(line[2]), float(line[3])
                pointsB.append([x, y])
    return pointsA, pointsB


# make histogram for fd and dtw on same histogram
def make_histogram(fd_path, dtw_path, title):
    fd_dist = [calculate_distance(i, j) for i, j in fd_path]
    dtw_dist = [calculate_distance(i, j) for i, j in dtw_path]
    plt.hist(fd_dist, 10, alpha=0.5, label='fd')
    plt.hist(dtw_dist, 10, alpha=0.5, label='dtw')
    plt.legend(loc='upper right')
    plt.title(title)
    plt.xlabel("Distance")
    plt.ylabel("Number of Edges")
    plt.show()


if __name__ == "__main__":
    # make histograms for pairs 128
    pointsA, pointsB = read_pairs('128-20080503104400', '128-20080509135846')
    path_dtw = dtw(pointsA, pointsB)
    path_fd = fd(pointsA, pointsB)
    make_histogram(path_fd, path_dtw, "Frequency of Edge Lengths for Pairs 128")

    # make histograms for pairs 010
    pointsA, pointsB = read_pairs('010-20081016113953', '010-20080923124453')
    path_dtw = dtw(pointsA, pointsB)
    path_fd = fd(pointsA, pointsB)
    make_histogram(path_fd, path_dtw, "Frequency of Edge Lengths for Pairs 010")

    # make histograms for pairs 115
    pointsA, pointsB = read_pairs('115-20080520225850', '115-20080615225707')
    path_dtw = dtw(pointsA, pointsB)
    path_fd = fd(pointsA, pointsB)
    make_histogram(path_fd, path_dtw, "Frequency of Edge Lengths for Pairs 115")
    
    # compute simplification for T1, T2
    t1, t2 = read_pairs('115-20080520225850', '115-20080615225707')
    e = [0.03, 0.1, 0.3]
    e1 = dtw(task2.TS_greedy(t1, e[0]), task2.TS_greedy(t2, e[0]))
    e2 = dtw(task2.TS_greedy(t1, e[1]), task2.TS_greedy(t2, e[1]))
    e3 = dtw(task2.TS_greedy(t1, e[2]), task2.TS_greedy(t2, e[2]))
    
    e1_dist = [calculate_distance(i, j) for i, j in e1]
    e2_dist = [calculate_distance(i, j) for i, j in e2]
    e3_dist = [calculate_distance(i, j) for i, j in e3]
    
    plt.hist(e1_dist, 20, alpha=0.5, label='e=0.03')
    plt.hist(e2_dist, 2, alpha=0.5, label='e=0.1')
    plt.hist(e3_dist, 2, alpha=0.5, label='e=0.3')

    plt.legend(loc='upper right')
    plt.title("DTW Compressed Path Edge Distance Frequencies")
    plt.xlabel("Distance")
    plt.ylabel("Number of Edges")
    plt.show()