# Trajectory Analysis Case Study

## Project Overview
This project focuses on analyzing, simplifying, and clustering trajectory data to uncover patterns and optimize data processing. Using the GeoLife dataset, the project explores algorithms for identifying high-density hubs, simplifying trajectory paths, and clustering trajectories based on their similarity. Through these tasks, we aimed to balance **computational efficiency** and **accuracy**, experimenting with different techniques to find optimal solutions.

Compiled results and analysis are available in a PowerPoint file located under the Anlysis folder

## **Project Structure**
1. **Task 1: Identifying Hubs**
   - Developed an algorithm to identify high-traffic hubs from trajectory points.
   - Implemented a **density function** to calculate the concentration of data points and ensured hubs are separated by a minimum distance.

2. **Task 2: Trajectory Simplification**
   - Implemented a **greedy algorithm** to reduce the number of points in each trajectory while keeping the shape within an acceptable error threshold.
   - Analyzed the trade-off between **simplification** and **accuracy**, reporting compression ratios for several paths.

3. **Task 3: Trajectory Comparison**
   - Implemented **Dynamic Time Warping (DTW)** and **Frechet distance** algorithms to compare trajectories.
   - Visualized similarity scores between trajectory pairs to better understand alignment and deviation patterns.

4. **Task 4: Center Trajectories**
   - Developed two approaches to compute a representative center trajectory:
     1. **Approach I**: Selected an input trajectory that minimized the sum of DTW distances to all other trajectories.
     2. **Approach II**: Proposed a novel algorithm to compute an average trajectory as a function of time.
   - Visualized and compared the results of both methods to determine which produced better central representations.

5. **Task 5: Clustering Trajectories**
   - Implemented **Lloyd’s algorithm** to partition trajectories into clusters, each with a representative center trajectory.
   - Designed two seeding strategies—**random** and **custom seeding**—to initialize clusters and evaluated their performance.
   - Visualized clustering results and monitored performance over multiple iterations to recommend the optimal number of clusters.


## **Technologies and Dataset**
- **Programming Language:** Python
- **Dataset:** [Microsoft GeoLife Trajectory Data](https://www.microsoft.com/en-us/download/details.aspx?id=52367)


## Recreation Steps
- Functions within each file are defined below
- Specific recreation steps are detailed in comments within each respective file
- Certain paths might need to be corrected depending on local organization

### Task One: 
- density.py
    - Includes global variables:
        - p: List of tuples (x, y) -- Representing coordinates after CSV file reading
        - r_c: Represents the size of the 2D grids 
        - grid: Data structure produced by preprocessing function
    - read_csv: 
        - Takes in user input String via terminal 'ten', 'thirty', 'sixty', or 'full' depending on desired CSV
        - Will load in and populate list p with (x, y) tuples
    - Density(grid, x, y): 
        - Takes in the global data structure grid after preprocessing, as well as the x coordinate of the desired point (float), and the y coordinate of the desired point (float)
        - Returns the density of the inputted point by counting the total number of neighboring points found within a r_c x r_c area centered at the inputted (x, y) coordinate.
        - Returns density as float
    - validCenter(): 
        - Checks if any two centers are within a distance of r of each other. It takes as input the list of centers (centers), the number of hubs (k), and the minimum distance between hubs (r). It iterates over each pair of centers and checks if their distance is less than r. If any two centers are too close, the function returns False, indicating that a new set of centers should be chosen.
        - Returns boolean value
    - Hubs(p, k, r): 
        - Takes in a set of tuples--(x, y) coordinates--p, a desired number of hubs k, and a minimum radius between hub centers r and returns a set of coordinates (as a list) that represent the k   most dense hubs separated (from the middle) by at least radius r
        - Returns list that represent set of tuples-- (x, y) coordinate locations of the top k most dense hubs
    - Distance(p, q): 
        - Compute the Euclidean distance between two points
        - Returns float value representing the distance between inputted points p and q
        - Inputs p and q are inputted as tuples (x, y)
    - preprocess_grid(): 
        - Takes a set of points and a cell size as input, and returns a grid formed by dividing the 2D space into cells with the specified size and assigning each point to a cell
        - The output is a 2D list representing the grid, where each cell contains a list of points assigned to that cell. 
        - The function can be used as a preprocessing step
    - Main(): 
        - Intiializes CSV data depending on user input
        - Time is also recorded and output as necessary (automatically)
        - Line 161 has a r value that represents radius plugged into hubs -- used this to change radius
        - Can set k for hubs directly in the function call on line 162
        - Visualizations should automatically display after running

### Task Two:
- greedy.py
    - TS_greedy(T, my_epsilon):
        - Uses divide and conquer to calculate the a simplified trajectory from points in Array T. Simplified path is within error my_epsilon.
    - read_pairs(pairId1):
        - Used to read CSV file and filter out X and Y coordinates of trejectory with trejectory_ID = pairId1.
    - multipleEpsilons():
        - Used to run TS_greedy with different epsilon values. Results are then plotted using MatPlotLib.
    - multipleTrej():
        - Used to run TS_greedy with different points in array T, which pertain to different trajectory IDs. Results are printed to terminal. 
- segment.py
    - __init__(x1,y1,x2,y2):
        - Used to initialize the line segment. Line segment starts at (x1,y1) and ends at (x2,y2)
    - minDistanceFromPoint(qx,qy):
        - Used to calculate the minimum distance from the initialized segment, and a point at (qx, qy).
    - dist():
        - Used to get the length of the segment

### Task Three:
- task3.py
    - calculate_distance(A, B) 
        - Calculates the euclidean distance between two points
        - Inputs A and B are both integer arrays or tuples of size two where the first entry is the x coordinate of the point and the second entry is the y coordinate of the point
        - Returns a float that is the distance between two points A and B
    - fd(P, Q)
        - Calculates the frechet distance given two list of points representing the points in two curves
        - P and Q are each list of points for the curve. Each point is an array of size two with the first value as x and second value as y
        - Returns a list of floats that are the distance between the optimally aligned edges on the two curves
    - dtw(P, Q)
        - Calculates the dynamic time warping distance given two list of points representing the points in two curves
        - P and Q are each list of points for the curve. Each point is an array of size two with the first value as x and second value as y
        - Returns a list of floats that are the distance between the optimally aligned edges on the two curves
    - read_pairs(pairId1, pairId2)
        - CSV function that reads the given pairs from the csv based on the given ids
        - Inputs pairId1 and pairId2 are two ids of the curve whose points you want to read from the list of points in the csv
        - Returns a tuple of the points x and y coordinates in a list: one for each both ids 
    - make_histogram
        - Given the two paths (dtw and fd) calculates the edge distances on the optimal alignments and makes a histogram of the edge weights
        - fd_path is the frechet distance optimally aligned paths, dtw_path is the dtw distance optimally aligned paths
        - Returns nothing; just displays the plot (plt.show())
    - Main:
        - run to construct the images for submission
        - reads the points and runs the distance functions and constructs the histogram
        - each plot is constructed one at a time so exit out of one to view the next

### Task Four:
- task_4.py
    - center_approach_one(trajectories: Dict[str, List[Tuple[float, float]]]) -> List[Tuple[float, float]]
        - Input: Dictionary with trajectory IDs as keys and lists of points as values
        - Output: List of points representing the trajectory that minimizes the total distance from all other trajectories in the input
        - Description: Implements the first centering approach to find the center trajectory among a collection of input trajectories.
    - center_approach_two(trajectories_dict: Dict[str, List[Tuple[float, float]]]) -> List[Tuple[float, float]]
        - Input: Dictionary with trajectory IDs as keys and lists of points as values
        - Output: List of points representing the central trajectory
        - Description: Implements the second centering approach to find the central trajectory among a collection of input trajectories.
    - calculate_distance(A: Tuple[float, float], B: Tuple[float, float]) -> float
        - Input: Two points represented as tuples with x and y coordinates
        - Output: Euclidean distance between the two input points
        - Description: Computes the Euclidean distance between two points in a 2D plane.
    - dtw(P: List[Tuple[float, float]], Q: List[Tuple[float, float]]) -> float
        - Input: Two lists of points representing trajectories P and Q, where each point is a tuple with x and y coordinates
        - Output: Dynamic Time Warping (DTW) distance between the input trajectories
        - Description: Computes the DTW distance between two trajectories P and Q in a 2D plane (Adapted from Case Study Part I).
    - TS_greedy(T: List[Tuple[float, float]], my_epsilon: float) -> List[Tuple[float, float]]
        - Input: A list of points representing a trajectory and an epsilon value (float)
        - Output: A list of points representing a simplified trajectory
        - Description: Simplifies the input trajectory using the greedy algorithm based on the given epsilon value (Adapted from Case Study Part I).
    - read_trajectory_csv(file_name: str, ids_to_process: Set[str]) -> Dict[str, List[Tuple[float, float]]]
        - Input: A CSV file name containing trajectory data and a set of trajectory IDs to process
        - Output: A dictionary with trajectory IDs as keys and lists of points as values
        - Description: Reads the input CSV file and returns a dictionary containing the specified trajectory IDs and their corresponding point lists.
    - read_trajectory_ids(file_name: str) -> List[str]
        - Input: A TXT file name containing trajectory IDs
        - Output: A list of trajectory IDs
        - Description: Reads the input TXT file and returns a list of trajectory IDs.
- segment.py
    - Segment class: Utilized for data processing in the main task_4.py file (Adapted from Case Study Part I)
        - Initialization method (__init__):
            - Input: x1, y1, x2, y2 (coordinates of the starting and ending points of a line segment)
            - Initializes the class with the given coordinates.
        - minDistanceFromPoint method:
            - Input: qx, qy (coordinates of a point)
            - Calculates the minimum distance between the line segment and the given point using the projection of the point onto the line. Returns the minimum distance.
        - dist method:
        - No input
        - Calculates the Euclidean distance (i.e., length) of the line segment.
        - Returns the distance.
        - The Segment class is initialized with the coordinates of the starting and ending points of a line segment, and provides methods to calculate the minimum distance from a point to the line segment and the length of the segment.

#### Data Collection/Recreation for Task 4
- The code is divided into two sections found on the bottom of the task_4.py file:
    - The first section deals with the non-simplified (raw) trajectory data
        - Calculates the center trajectories using Approach I and Approach II utilizing unsimplified trajectories (utilizing the raw data points)
        - The average DTW distance between approach I center trajectory and all other trajectories are computed and printed
        - The average DTW distance between approach II center trajectory and all other trajectories are computed and printed
        - It then plots all the raw trajectories along with the new center trajectories derived from both approaches
     - The second section deals with the simplified trajectory data
        - It takes user input for the epsilon value (0.03, 0.1, or 0.3) and simplifies the trajectories accordingly based on this epislon value, returning the trajectories in a dictionary where the id corresponds to their simplified trajectory points.
        - We then recalculate the same center trajectory from approach I based on the unsimplified trajectories from the first section (Outputs same value as before)
        - The average DTW distance between this same center trajectory and all other simplified trajectories at the given epsilon are computed and printed
        - Finally, it plots the simplified trajectories along with the center trajectory derived from Approach I on the unsimplified trajectories
- To switch between the unsimplified and simplified versions, comment or uncomment the respective sections of the code.


### Task Five:
- task_5.py
    - same_clusters(c1, c2)
        - Input: Two lists of clusters c1 and c2
        - Output: Boolean indicating whether the input clusters are the same
        - Description: Compares the input clusters and returns True if they have the same structure, False otherwise.
    - random_seeding(trajectories, k)
        - Input: A dictionary of trajectories and an integer k representing the number of clusters
        - Output: A tuple containing the initial center trajectories and initial trajectory clusters
        - Description: Implements the random seeding approach for k-means clustering initialization.
    - random_lloyds(trajectories, k, t_max)
        - Input: A dictionary of trajectories, an integer k representing the number of clusters, and an integer t_max representing the maximum number of iterations
        - Output: A tuple containing the final trajectory clusters and the clustering costs at each iteration
        - Description: Implements the k-means clustering algorithm with random seeding for t_max iterations.
    - optimized_lloyds(trajectories, k, t_max)
        - Input: A dictionary of trajectories, an integer k representing the number of clusters, and an integer t_max representing the maximum number of iterations
        - Output: A tuple containing the final trajectory clusters and the clustering costs at each iteration
        - Description: Implements the k-means clustering algorithm with optimized seeding for t_max iterations.
    - optimize_seeding(trajectories, k)
        - Input: A dictionary of trajectories and an integer k representing the number of clusters
        - Output: A tuple containing the initial center trajectories and initial trajectory clusters
        - Description: Implements an optimized seeding approach for k-means clustering initialization.
    - evaluate_cost_random(trajectories, k_values)
        - Input: A dictionary of trajectories and a list of integer values for k
        - Output: A list of average clustering costs for each k
        - Description: Evaluates the average clustering cost for random seeding across multiple runs and k values.
    - evaluate_cost_optimized(trajectories, k_values)
        - Input: A dictionary of trajectories and a list of integer values for k
        - Output: A list of average clustering costs for each k
        - Description: Evaluates the average clustering cost for optimized seeding across multiple runs and k values.
    - read_trajectory_csv(file_name)
        - Input: A string representing the file name of the trajectory data in CSV format
        - Output: A dictionary of trajectories, where each key is a trajectory ID and each value is a list of points (x, y) in the trajectory
        - Description: Reads the input CSV file and builds a dictionary of trajectories.
    - evaluate_cost_optimized_PT2(trajectories)
        - Input: A dictionary of trajectories
        - Output: A list of average clustering costs for optimized seeding across multiple runs and iterations
        - Description: Evaluates the average clustering cost for optimized seeding across multiple runs and iterations.
    - evaluate_cost_random_PT2(trajectories)
        - Input: A dictionary of trajectories
        - Output: A list of average clustering costs for random seeding across multiple runs and iterations
        - Description: Evaluates the average clustering cost for random seeding across multiple runs and iterations.

#### Data Collection/Recreation for Task 5
- The code provided generates three visualizations and data collection techniques through the functions above
    - Average Cost of Clustering vs. k: This plot compares the average cost of clustering for random seeding and optimized seeding methods over different values of k (number of clusters). It uses the simplified trajectories obtained from the greedy algorithm to compute the costs. The x-axis represents the number of clusters (k), and the y-axis represents the average cost.
    - Average Cost of Clustering vs. Iteration: This plot shows the average cost of clustering for random seeding and optimized seeding methods over multiple iterations. The x-axis represents the iteration number, and the y-axis represents the average cost.
    - Center Trajectories for Optimized Seeding (k=10): This visualization displays the center trajectories for the optimized seeding method with k=10. The plot shows ten different trajectories in ten distinct colors, representing the center trajectories of the ten optimized clusters. The x-axis represents the X-axis, and the y-axis represents the Y-axis.
- Simply uncomment the section (separated by #'s). Keep the top most part of the main statement uncommented. Only switch out the sub-sections