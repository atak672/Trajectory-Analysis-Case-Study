import math

def euclidean_distance(p, q):
    x_diff = p[0] - q[0]
    y_diff = p[1] - q[1]
    return math.sqrt(x_diff * x_diff + y_diff * y_diff)

def squared_euclidean_distance(p, q):
    return euclidean_distance(p, q) ** 2

def delta(Ti, Tj):
    r = len(Ti)
    s = len(Tj)
    C = [[0 for _ in range(s)] for _ in range(r)]

    for a in range(r):
        for b in range(s):
            d_sq = squared_euclidean_distance(Ti[a], Tj[b])
            if a == 0 and b == 0:
                C[a][b] = d_sq
            elif a == 0:
                C[a][b] = d_sq + C[a][b - 1]
            elif b == 0:
                C[a][b] = d_sq + C[a - 1][b]
            else:
                C[a][b] = d_sq + min(C[a - 1][b], C[a - 1][b - 1], C[a][b - 1])

    A_size = r + s - 1  # The number of edges in the assignment
    return math.sqrt(C[-1][-1] / A_size)


if __name__ == "__main__":
    T1 = [(17.544962, 0.525958), (15.943268, 0.397717), (16.010932, 0.043383), (6.667294, -0.015005), (6.391936, 5.397419), (2.199832, 8.860763), (-6.763538, 8.571656), (-6.755716, 7.52013), (-6.354548, 7.497146)]        
    T2 = [(14.603855, 0.121587), (6.651804, -0.013704), (6.394069, 5.39018), (2.248305, 8.849644), (-6.768801, 8.567397), (-6.760697, 7.509011), (-6.335638, 7.497891)]
    print(delta(T1, T2))