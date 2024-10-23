import math
import numpy as np

def calculate_distance(p, q):
    x_diff = p[0] - q[0]
    y_diff = p[1] - q[1]
    return math.sqrt(x_diff * x_diff + y_diff * y_diff)


# Dynamic Time Warping (DTW) measuremnet between two trajectories P & Q
# That are represented as a list of tuple (x, y) coordinates
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

    numerator = 0
    denominator = len(points)
    for x, y in points:
        temp = (calculate_distance(x, y))
        numerator += ((temp)**2)
    return (numerator/denominator)**0.5



if __name__ == "__main__":
    T1 = [(2, 1), (3, 4), (4, 1), (5, 3)]
    T2 = [(1, 1), (2, 2), (3, 3)]
    print(dtw(T1, T2))
