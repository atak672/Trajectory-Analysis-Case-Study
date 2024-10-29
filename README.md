# Trajectory Analysis Case Study
**Compiled results and analysis** are available in a PowerPoint file located under the Anlysis folder


## Project Overview
This project focuses on analyzing, simplifying, and clustering trajectory data to uncover patterns and optimize data processing. Using the GeoLife dataset, the project explores algorithms for identifying high-density hubs, simplifying trajectory paths, and clustering trajectories based on their similarity. Through these tasks, we aimed to balance **computational efficiency** and **accuracy**, experimenting with different techniques to find optimal solutions.


## **Project Structure**
- **Task 1: Hub Identification**
   - Developed an algorithm to identify high-traffic hubs from trajectory points.
   - Implemented a **density function** to calculate the concentration of data points and ensured hubs are separated by a minimum distance.

- **Task 2: Trajectory Simplification**
   - Implemented a **greedy algorithm** to reduce the number of points in each trajectory while keeping the shape within an acceptable error threshold.
   - Analyzed the trade-off between **simplification** and **accuracy**, reporting compression ratios for several paths.

- **Task 3: Comparing Trajectory**
   - Implemented **Dynamic Time Warping (DTW)** and **Frechet distance** algorithms to compare trajectories.
   - Visualized similarity scores between trajectory pairs to better understand alignment and deviation patterns.

- **Task 4: Center Trajectories**
   - Developed two approaches to compute a representative center trajectory:
     1. **Approach I**: Selected an input trajectory that minimized the sum of DTW distances to all other trajectories.
     2. **Approach II**: Proposed a novel algorithm to compute an average trajectory as a function of time.
   - Visualized and compared the results of both methods to determine which produced better central representations.

- **Task 5: Clustering Trajectories**
   - Implemented **Lloyd’s algorithm** to partition trajectories into clusters, each with a representative center trajectory.
   - Designed two seeding strategies—**random** and **custom seeding**—to initialize clusters and evaluated their performance.
   - Visualized clustering results and monitored performance over multiple iterations to recommend the optimal number of clusters.


## **Technologies and Dataset**
- **Programming Language:** Python
- **Dataset:** [Microsoft GeoLife Trajectory Data](https://www.microsoft.com/en-us/download/details.aspx?id=52367)


## **Recreation Steps**  
- **Function Documentation:** Key functions in each file are described below.  
- **Execution Instructions:** Detailed instructions are provided within the code comments in each respective file.  
- **Path Corrections:** Update file paths as needed to align with local directory structure.  

### **Task One: `density.py`**  
- **Global Variables:**
  - `p`: List of tuples representing coordinates from CSV data.
  - `r_c`: Grid cell size for 2D space.
  - `grid`: Preprocessed 2D list of point data.
- **Key Functions:**
  - `read_csv`: Loads CSV data based on user input ('ten', 'thirty', 'sixty', or 'full').
  - `Density(grid, x, y)`: Calculates the density at a given (x, y) point.
  - `validCenter()`: Validates that hubs are spaced at least `r` units apart.
  - `Hubs(p, k, r)`: Identifies the top `k` dense hubs with at least `r` distance between them.
  - `Distance(p, q)`: Computes Euclidean distance between two points.
  - `preprocess_grid()`: Creates a 2D grid for efficient density computation.
- **Main Execution:**  
  - Modify `r` and `k` values on lines 175–176 to adjust radius and number of hubs.  
  - Visualizations auto-generate after execution.

--- 

### **Task Two: `greedy.py`**  
- **Functions:**
  - `TS_greedy(T, my_epsilon)`: Simplifies trajectory points within error `my_epsilon`.
  - `read_pairs(pairId1)`: Extracts trajectory points from CSV based on ID.
  - `multipleEpsilons()` & `multipleTrej()`: Run simplifications with multiple settings and IDs.
- **Additional File:** `segment.py`
  - `init()`: Initializes a line segment.
  - `minDistanceFromPoint()`: Calculates minimum distance from a point to the segment.

---

### **Task Three: `task3.py`**  
- **Key Functions:**
  - `calculate_distance(A, B)`: Computes Euclidean distance between two points.
  - `fd(P, Q)` & `dtw(P, Q)`: Calculate Frechet and DTW distances for trajectory comparison.
  - `make_histogram()`: Visualizes edge weights from optimal trajectory alignments.
- **Main Execution:**  
  - Runs distance calculations and generates histograms. Close one plot to see the next.

---

### **Task Four: `task_4.py`**  
- **Key Functions:**
  - `center_approach_one()` & `center_approach_two()`: Implement different algorithms to find a center trajectory.
  - `TS_greedy()` (adapted from Task 2): Used for simplified trajectory calculations.
  - `read_trajectory_csv()` & `read_trajectory_ids()`: Load trajectory data and IDs.
- **Data Handling:**  
  - **Section 1:** Works with raw trajectory data.  
  - **Section 2:** Simplifies trajectories based on epsilon values (0.03, 0.1, or 0.3) and re-evaluates results.  
  - Switch between sections by commenting/uncommenting relevant code.

---

### **Task Five: `task_5.py`**  
- **Functions:**
  - `random_lloyds()` & `optimized_lloyds()`: Implement k-means clustering with different seeding strategies.
  - `evaluate_cost_random()` & `evaluate_cost_optimized()`: Compare clustering costs across different `k` values and iterations.
- **Visualization:**  
  - Plots average clustering costs vs. `k` and vs. iterations.
  - Displays center trajectories for optimized clusters with `k = 10`.
  - Plots ten different trajectories in ten distinct colors, representing the center trajectories of the ten optimized clusters