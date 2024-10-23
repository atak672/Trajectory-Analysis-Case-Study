import math 
import csv
import random
import time
import matplotlib.pyplot as plt

# Global points variable
p = []
# Global radius set for pre-processing
r_c = 0.1
# Global grid preprocessed data structure
grid = None

# CSV function that reads inputted CSV file
def read_csv(str):
    if str == "ten":
         file = "../Data/geolife-cars-ten-percent.csv"
    elif str == "thirty":
        file = "../Data/geolife-cars-thirty-percent.csv"
    elif str == "sixty":
        file = "../Data/geolife-cars-sixty-percent.csv"
    elif str == "full":
        file = "../Data/geolife-cars.csv"
    else: 
        print("Invalid CSV request for str")
        return -1

    with open(file, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for line in csvreader:
            x, y = float(line[2]), float(line[3])
            p.append((x, y))
    return 0


# Density function returns point count in fixed radius 
def density(grid, x, y):

    # Determine the grid cell that the point (x,y) falls in
    cell_x = int((x - min([p[i][0] for i in range(len(p))])) // r_c)
    cell_y = int((y - min([p[i][1] for i in range(len(p))])) // r_c)
    
    # Find all neighboring cells
    neighbors = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if 0 <= cell_x+i < len(grid) and 0 <= cell_y+j < len(grid[0]):
                neighbors.append(grid[cell_x+i][cell_y+j])
    
    # Count the number of particles within radius r_c of (x,y)
    count = 0
    in_set = False
    for particle_list in neighbors:
        for particle in particle_list:
            if particle == (x, y):
                in_set = True
            dx = particle[0] - x
            dy = particle[1] - y
            if dx**2 + dy**2 <= r_c**2:
                count += 1
    # Does not count search (x, y) in solution if present            
    if in_set:
        return count - 1
    else:
        return count

# This function takes a list of centers, an integer k, and a minimum distance r
# It returns True if all the centers are at least r distance away from each other, False otherwise
def validCenters(centers, k, r):
    for i in range(k):
        for j in range(i+1, k):
            if math.dist(centers[i], centers[j]) < r:
                return False
    return True


# This is the main function that takes a list of points, an integer k, and a minimum distance r
# It uses the k-means++ algorithm to initialize the cluster centers then iterates and updates the centers until valid
# It returns a list of k cluster centers
def hubs(points, k, r):
    # K-means++ initialization
    centers = [random.choice(points)]  # Choose the first center randomly from the points
    while len(centers) < k:  # Choose k-1 more centers using probabilities proportional to the squared distances from the current centers
        distances = [min([math.dist(p, c) for c in centers])**2 for p in points]
        sum_distances = sum(distances)
        probabilities = [d/sum_distances for d in distances]
        centers.append(random.choices(points, weights=probabilities, k=1)[0])

    while not validCenters(centers, k, r):  # Regenerate centers using k-means++ initialization if not valid
        centers = [random.choice(points)]
        while len(centers) < k:
            distances = [min([math.dist(p, c) for c in centers])**2 for p in points]
            sum_distances = sum(distances)
            probabilities = [d/sum_distances for d in distances]
            centers.append(random.choices(points, weights=probabilities, k=1)[0])

    while True:  # Iteratively update centers until they are valid
        clusters = [[] for i in range(k)]  # Initialize empty clusters
        for point in points:  # Assign each point to the cluster with the closest center
            min_dist = math.inf
            min_center = -1
            for i in range(len(centers)):
                dist = math.dist(point, centers[i])
                if dist < min_dist:
                    min_dist = dist
                    min_center = i
            clusters[min_center].append(point)

        for i in range(k):  # Update each center by choosing the point in its cluster that minimizes the total distance to all other centers
            old_center = centers[i]
            new_center = None
            for j in range(len(clusters[i])):
                new_centers = centers.copy()
                new_centers[i] = clusters[i][j]
                if validCenters(new_centers, k, r):
                    new_center = clusters[i][j]
                    break
            if new_center is None:
                centers[i] = old_center
            else:
                centers[i] = new_center

        if validCenters(centers, k, r):  # Return the centers if they are valid
            return centers


# Compute the Euclidean distance between two points
def distance(p, q):
    return ((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5
    

# Preprocessing returns 2D array that splices 2D plane with the respective points
# Listed within each spatial block. Basis for density function
def preprocess_grid():
    # Secure and read desired CSV file

    # Make sure CSV read correctly
    if check == -1:  
        exit()

    # Preprocessing step to form grid
    min_x = min([x[0] for x in p])
    max_x = max([x[0] for x in p])
    min_y = min([x[1] for x in p])
    max_y = max([x[1] for x in p])

    n_cells_x = int(math.ceil((max_x - min_x) / r_c))
    n_cells_y = int(math.ceil((max_y - min_y) / r_c))

    g = [[[] for j in range(n_cells_y)] for i in range(n_cells_x)]

    count = 1
    for i in p:
        count += 1
        cell_x = int((i[0] - min_x) // r_c)
        cell_y = int((i[1] - min_y) // r_c)
        g[cell_x][cell_y].append(i)

    return g


if __name__ == "__main__":
    # Plot the trajectory and its simplification
    inp = input("Which CSV file?\n")
    check = read_csv(inp)


    grid = preprocess_grid()
    #print(density(grid, 1, 2))

    temp1 = time.time()

    # r value for hubs
    r = 8
    #Call for hubs
    array = hubs(p, 5,r)

    # Timing mechanism
    temp2 = time.time()
    print(temp2 - temp1)





    # Visualizations code for points P scatterplot with hubs identified
    all_x = [i[0] for i in p]
    all_y = [i[1] for i in p]
    hubs_x = [i[0] for i in array]
    hubs_y = [i[1] for i in array]
    plt.scatter(all_x, all_y, c ="blue", s= [1])
    
    plt.scatter(hubs_x, hubs_y, c = "red", s = 20)
    for i in range(len(hubs_x)):
        c1 = plt.Circle((hubs_x[i],hubs_y[i]), r, fill=False,edgecolor='black')
        plt.gca().add_patch(c1)
    # # Show the plot
    # plt.tight_layout()
    plt.show()