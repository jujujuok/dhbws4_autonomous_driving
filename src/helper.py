import matplotlib.pyplot as plt
import numpy as np


def show_plt_img_grey(image: np.ndarray):
    plt.imshow(image, cmap="grey")
    plt.show()

import numpy as np

def find_clusters(array):
    clusters = []
    visited = np.zeros_like(array)

    def explore_cluster(row, col, cluster):
        if row < 0 or col < 0 or row >= array.shape[0] or col >= array.shape[1]:
            return
        if visited[row][col] or array[row][col] == 0:
            return
        visited[row][col] = 1
        cluster.append((row, col))

        explore_cluster(row + 1, col, cluster)
        explore_cluster(row - 1, col, cluster)
        explore_cluster(row, col + 1, cluster)
        explore_cluster(row, col - 1, cluster)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if not visited[i][j] and array[i][j] == 1:
                cluster = []
                explore_cluster(i, j, cluster)
                clusters.append(cluster)

    return clusters

# Example usage:
arr = np.array([[1, 0, 0, 1, 0],
                [1, 1, 0, 0, 1],
                [0, 0, 0, 1, 1],
                [0, 1, 0, 0, 0],
                [1, 1, 1, 0, 1]])

print(find_clusters(arr))
