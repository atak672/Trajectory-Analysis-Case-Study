import random 
import math
import task_4
import csv
import matplotlib.pyplot as plt


# Input: Two lists of clusters c1 and c2
# Output: Boolean indicating whether the input clusters are the same
# Description: Compares the input clusters and returns True if they have the same structure, False otherwise.
def same_clusters(c1, c2):
    if len(c1) != len(c2):
        return False

    for i in range(len(c1)):
        if set(c1[i].keys()) != set(c2[i].keys()):
            return False

    return True

# Input: A dictionary of trajectories and an integer k representing the number of clusters
# Output: A tuple containing the initial center trajectories and initial trajectory clusters
# Description: Implements the random seeding approach for k-means clustering initialization.
def random_seeding(trajectories, k):

    # initial key split
    # [
    #   [key, key, key],
    #   [key, key, key],
    #   [key, key, key],
    # ]
   
    # initial trajectory split
    # [
    #   {key: [points], key: [points], key: [points]},
    #   {key: [points], key: [points], key: [points]},
    #   {key: [points], key: [points], key: [points]}
    # ]
   
    keys = trajectories.keys()
    center_keys = random.sample(keys, k)
    initial_center_trajectories = []
    for c in center_keys:
        initial_center_trajectories.append(trajectories[c])
       
    initial_trajectory_clusters = [{} for i in range(k)]
    for t in trajectories:
        min_dist = math.inf
        center_index = -1
        for i in range(len(initial_center_trajectories)):
            dist = task_4.dtw(initial_center_trajectories[i], trajectories[t])
            if(dist < min_dist):
                min_dist = dist
                center_index = i
        initial_trajectory_clusters[center_index][t] = trajectories[t]
    return initial_center_trajectories, initial_trajectory_clusters


# Input: A dictionary of trajectories, an integer k representing the number of clusters, and an integer t_max representing the maximum number of iterations
# Output: A tuple containing the final trajectory clusters and the clustering costs at each iteration
# Description: Implements the k-means clustering algorithm with random seeding for t_max iterations
def random_lloyds(trajectories, k, t_max):
    initial_center_trajectories, initial_trajectory_clusters = random_seeding(trajectories, k)
    t_cost = [0 for _ in range(t_max)]
    trajectory_clusters = [{} for i in range(k)]
   
   
    for x in range(t_max):
        center_trajectories = [{} for _ in range(k)]
        for i in range(k):
            if len(initial_trajectory_clusters[i]) != 0:
                center_trajectories[i] = task_4.center_approach_two(initial_trajectory_clusters[i])

        trajectory_clusters = [{} for i in range(k)]
        for t in trajectories:
            min_dist = math.inf
            center_index = -1
            for i in range(len(center_trajectories)):
                if len(center_trajectories[i]) != 0:
                    dist = task_4.dtw(center_trajectories[i], trajectories[t])
                    if(dist < min_dist):
                        min_dist = dist
                        center_index = i
            trajectory_clusters[center_index][t] = trajectories[t]

        cost = 0
        for i in range(len(trajectory_clusters)):
            for trajectory_id, trajectory_points in trajectory_clusters[i].items():
                cost += task_4.dtw(center_trajectories[i], trajectory_points)

        print("iter, cost", x, cost)
        t_cost[x] = cost
       
        if same_clusters(trajectory_clusters, initial_trajectory_clusters):
            print("BREAKING")
            return trajectory_clusters, t_cost
        else:
            initial_center_trajectories = center_trajectories
            initial_trajectory_clusters = trajectory_clusters

       
       
    return initial_trajectory_clusters, t_cost
       
       
# Input: A dictionary of trajectories, an integer k representing the number of clusters, and an integer t_max representing the maximum number of iterations
# Output: A tuple containing the final trajectory clusters and the clustering costs at each iteration
# Description: Implements the k-means clustering algorithm with optimized seeding for t_max iterations
def optimized_lloyds(trajectories, k, t_max):
    initial_center_trajectories, initial_trajectory_clusters = optimize_seeding(trajectories, k)
    t_cost = [0 for _ in range(t_max)]
    trajectory_clusters = [{} for i in range(k)]
   
   
    for x in range(t_max):
        center_trajectories = [{} for _ in range(k)]
        for i in range(k):
            if len(initial_trajectory_clusters[i]) != 0:
                center_trajectories[i] = task_4.center_approach_two(initial_trajectory_clusters[i])

        trajectory_clusters = [{} for i in range(k)]
        for t in trajectories:
            min_dist = math.inf
            center_index = -1
            for i in range(len(center_trajectories)):
                if len(center_trajectories[i]) != 0:
                    dist = task_4.dtw(center_trajectories[i], trajectories[t])
                    if(dist < min_dist):
                        min_dist = dist
                        center_index = i
            trajectory_clusters[center_index][t] = trajectories[t]


        cost = 0
        for i in range(len(trajectory_clusters)):
            for trajectory_id, trajectory_points in trajectory_clusters[i].items():
                cost += task_4.dtw(center_trajectories[i], trajectory_points)

        print("iter, cost", x, cost)
        t_cost[x] = cost
       
        if same_clusters(trajectory_clusters, initial_trajectory_clusters):
            print("BREAKING")
            return trajectory_clusters, t_cost
        else:
            initial_center_trajectories = center_trajectories
            initial_trajectory_clusters = trajectory_clusters
   
    return initial_trajectory_clusters, t_cost


# Input: A dictionary of trajectories and an integer k representing the number of clusters
# Output: A tuple containing the initial center trajectories and initial trajectory clusters
# Description: Implements an optimized seeding approach for k-means clustering initialization
def optimize_seeding(trajectories, k):
    trajectory_keys = list(trajectories.keys())
    center_keys = []

    # Choose the first center uniformly at random
    first_center_key = random.choice(trajectory_keys)
    center_keys.append(first_center_key)

    # Choose the remaining k-1 centers
    for _ in range(1, k):
        distances = []
        for key in trajectory_keys:
            min_distance = math.inf
            for center_key in center_keys:
                distance = task_4.dtw(trajectories[key], trajectories[center_key])
                min_distance = min(min_distance, distance)
            distances.append(min_distance)
       
        # Choose the next center based on the probability distribution
        total_distance = sum(distances)
        if total_distance != 0:
            probabilities = [d / total_distance for d in distances]
            next_center_key = random.choices(trajectory_keys, probabilities)[0]
            center_keys.append(next_center_key)
   
    print(center_keys)
    initial_center_trajectories = []
    for c in center_keys:
        initial_center_trajectories.append(trajectories[c])
       
    initial_trajectory_clusters = [{} for i in range(k)]
    for t in trajectories:
        min_dist = math.inf
        center_index = -1
        for i in range(len(initial_center_trajectories)):
            if len(initial_center_trajectories[i]) != 0:
                dist = task_4.dtw(initial_center_trajectories[i], trajectories[t])
                if(dist < min_dist):
                    min_dist = dist
                    center_index = i
        initial_trajectory_clusters[center_index][t] = trajectories[t]
    return initial_center_trajectories, initial_trajectory_clusters

# Input: A dictionary of trajectories and a list of integer values for k
# Output: A list of average clustering costs for each k
# Description: Evaluates the average clustering cost for random seeding across multiple runs and k values.
def evaluate_cost_random(trajectories, k_values):
    avg_costs = []
    # avg_t_costs = []
    seeds = [10, 20, 30]
    for k in k_values:
        print("RANDOM")
        print("length", len(trajectories))
        print("k", k)
        costs = []
        # t_costs = []
        for j in range(3):
            print("RUN", j)
            random.seed(seeds[j])
            clusters, t_costs = random_lloyds(trajectories, k, 50)
            cost = 0
            for cluster in clusters:
                if len(cluster) != 0:
                    center_trajectory = task_4.center_approach_two(cluster)
                    for trajectory_id, trajectory_points in cluster.items():
                        cost += task_4.dtw(center_trajectory, trajectory_points)
            costs.append(cost)
            # t_costs.append(t_cost)
       
        avg_costs.append(sum(costs) / len(costs))
        # avg_t_costs.append(sum(t_costs) / len(t_costs))
       
    return avg_costs

# Input: A dictionary of trajectories and a list of integer values for k
# Output: A list of average clustering costs for each k
# Description: Evaluates the average clustering cost for optimized seeding across multiple runs and k values
def evaluate_cost_optimized(trajectories, k_values):
    avg_costs = []
    # avg_t_costs = []
    seeds = [10, 20, 30]
    for k in k_values:
        print("OPTIMIZED")
        print("length", len(trajectories))
        print("k", k)
        costs = []
        # t_costs = []
        for j in range(3):
            print("RUN", j)
            random.seed(seeds[j])
            clusters, t_costs = optimized_lloyds(trajectories, k, 50)
            cost = 0
            for cluster in clusters:
                if len(cluster) != 0:
                    center_trajectory = task_4.center_approach_two(cluster)
                    for trajectory_id, trajectory_points in cluster.items():
                        cost += task_4.dtw(center_trajectory, trajectory_points)
            costs.append(cost)
            # t_costs.append(t_cost)
           
        avg_costs.append(sum(costs) / len(costs))
        # avg_t_costs.append(sum(t_costs)/len(t_costs))
   
    return avg_costs


# Input: A string representing the file name of the trajectory data in CSV format
# Output: A dictionary of trajectories, where each key is a trajectory ID and each value is a list of points (x, y) in the trajectory
# Description: Reads the input CSV file and builds a dictionary of trajectories
def read_trajectory_csv(file_name):
    trajectories = {}
   
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader)  # Skip the header row
       
        for row in csv_reader:
            id, x, y = row[0], float(row[1]), float(row[2])
            if id not in trajectories:
                trajectories[id] = []
            trajectories[id].append((x, y))
   
    return trajectories

# Input: A dictionary of trajectories
# Output: A list of average clustering costs for optimized seeding across multiple runs and iterations
# Description: Evaluates the average clustering cost for optimized seeding across multiple runs and iterations
def evaluate_cost_optimized_PT2(trajectories):
    avg_costs = []
    t_costs = [0] * 50
    seeds = [10, 20, 30]
   
    for j in range(3):
        print("RUN", j)
        random.seed(seeds[j])
        clusters, t_cost = optimized_lloyds(trajectories, 10, 50)
        cost = 0
        # for cluster in clusters:
        #     if len(cluster) != 0:
        #         center_trajectory = task_4.center_approach_two(cluster)
        #         for trajectory_id, trajectory_points in cluster.items():
        #             cost += task_4.dtw(center_trajectory, trajectory_points)
        # avg_costs.append(cost)
        for i in range(50):
            t_costs[i] = t_costs[i] + t_cost[i]
           
           
    r = 3
    avg_t_costs = [x / r for x in t_costs]
    return avg_t_costs

# Input: A dictionary of trajectories
# Output: A list of average clustering costs for random seeding across multiple runs and iterations
# Description: Evaluates the average clustering cost for random seeding across multiple runs and iterations.
def evaluate_cost_random_PT2(trajectories):
    avg_costs = []
    t_costs = [0] * 50
    seeds = [10, 20, 30]
   
    for j in range(3):
        print("RUN", j)
        random.seed(seeds[j])
        clusters, t_cost = random_lloyds(trajectories, 10, 50)
        cost = 0
        # for cluster in clusters:
        #     if len(cluster) != 0:
        #         center_trajectory = task_4.center_approach_two(cluster)
        #         for trajectory_id, trajectory_points in cluster.items():
        #             cost += task_4.dtw(center_trajectory, trajectory_points)
        # avg_costs.append(cost)
       
       
       
        for i in range(50):
            t_costs[i] = t_costs[i] + t_cost[i]
       
        # t_costs = [x + y for x, y in zip(t_costs, t_cost)]
        # t_costs.append(t_cost)
   
    r = 3
    avg_t_costs = [x / r for x in t_costs]
    return avg_t_costs



if __name__ == "__main__":
   
    # Paths for data files
    csv_file = '../data/geolife-cars-upd8.csv'

    # Read the CSV file and build the trajectories dictionary
    # Returns dictionary of ID [(x1, y1), (x2, y2),...] pairs
    trajectories = read_trajectory_csv(csv_file)

    ep = 0.05
   
   
   
   
    # # For each id in dic.keys() --> run simplification algo to form new dictionary with simplified trajectory
    simplified_trajectories = {}

    # # Process each trajectory and obtain and assign its
    # # Simplified trajectory in the same dictionary format
    for id in trajectories.keys():
        simplified_trajectories[id] = []
        simplification = task_4.TS_greedy(trajectories[id], ep)
        print(len(simplification))
        simplified_trajectories[id] = simplification
       
   
   
   
    ############################################################## GET AVG_COST VS CLUSTERS ###############################################
   
    # k_values = [4,6,8,10,12]

    # random_costs = evaluate_cost_random(simplified_trajectories, k_values)
    # optimized_costs = evaluate_cost_optimized(simplified_trajectories, k_values)
   
    # # t_values = list(range(1, 100 + 1))

    # # plt.plot(t_values, t_cost, label='Random Seeding', marker='o')
    # # plt.plot(t_values, t_optimized_cost, label='Optimized Seeding', marker='o')
   
   
    # plt.plot(k_values, random_costs, label='Random Seeding', marker='o')
    # plt.plot(k_values, optimized_costs, label='Optimized Seeding', marker='o')
    # plt.xlabel('Number of Clusters (k)')
    # plt.ylabel('Average Cost')
    # plt.title('Average Cost of Clustering vs. k')
    # plt.legend()
    # plt.show()
       
   

   
   
    ############################################################### GET AVG_COST vs ITERATIONS #############################################
    # random_t_costs = evaluate_cost_random_PT2(simplified_trajectories)
    # optimized_t_costs = evaluate_cost_optimized_PT2(simplified_trajectories)

    # iterations = list(range(1, 51))

    # plt.plot(iterations, random_t_costs, label='Random Seeding', marker='o')
    # plt.plot(iterations, optimized_t_costs, label='Optimized Seeding', marker='o')
    # plt.xlabel('Iteration')
    # plt.ylabel('Average Cost')
    # plt.title('Average Cost of Clustering vs. Iteration')
    # plt.legend()
    # plt.show()
   
   
   
    ################################################################ GET CLUSTER TRAJECTORIES ################################################
   
    k = 10
    random.seed(10)  # Set seed for reproducibility
    optimized_clusters, t_cost = optimized_lloyds(simplified_trajectories, k, 50)

    # Calculate and plot the center trajectories of optimized clusters
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'pink', 'brown', 'purple']
    for i, cluster in enumerate(optimized_clusters):
        if len(cluster) != 0:
            center_trajectory = task_4.center_approach_two(cluster)
            x, y = zip(*center_trajectory)
            plt.plot(x, y, color=colors[i], marker='o', linestyle='-', linewidth=2, markersize=5)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Center Trajectories for Optimized Seeding (k=10)')
    # plt.legend()
    plt.show()