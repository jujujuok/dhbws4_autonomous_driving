from __future__ import annotations

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from time import time

from structs_and_configs import CarConst, ImageConfig

from lane_detection_helper import detect_green_pixels, edge_detect_scipy, edge_detection


class LaneDetection:

    def evaluation_detect(self, image):
        """
        for evaluation of the different edge
        detection functions that are implemented

        Args:
            image (np.ndarray): image input from which
                                the edges should be detected
        """
        t = time()
        g = detect_green_pixels(image, threshold=50)
        dt_g = time()
        e = edge_detection(image)
        dt_e = time()
        s = edge_detect_scipy(image)
        dt_s = time()

        images = {
            # [image with applied detection, time to calculate]
            "green": [g, dt_g - t],
            "edge detect": [e, dt_e - dt_g],
            "scipy": [s, dt_s - dt_e],
        }

        plt.figure(figsize=(12, 6))

        for i, (title, img_time) in enumerate(images.items()):
            plt.subplot(1, len(images), i + 1)
            plt.imshow(img_time[0], cmap="gray")
            plt.title(f"{title}\ntime to detect: {str(img_time[1])}")

        plt.show()

    def detect_lanes(self, image: np.ndarray) -> np.ndarray:
        """
        1) crops the image
        2) applies the detection
        3) masks the car

        Args:
            image (np.ndarray): raw image

        Returns:
            np.ndarray: image with
                        - 1 for the lane,
                        - 0 for offset and road
        """

        image = image[: image.shape[0] - ImageConfig.displaycrop, :, :]

        image = edge_detect_scipy(image)

        image = (image > 70).astype(np.uint8)

        image[CarConst.start_h : CarConst.end_h, CarConst.start_w : CarConst.end_w] = 0

        return image

    def detect(self, image: np.ndarray) -> np.ndarray:
        """
        public method for the detection
        1) detect_lanes
        (2) cluster the lanes to right and left, currently not used)

        Args:
            image (np.ndarray): raw image

        Returns:
            np.ndarray: image with
                        - 1 for the lane,
                        - 0 for offset and road
        """

        image = self.detect_lanes(image=image)

        # segment left/right lane
        # image = self.lane_clustering(image, 50)

        return image

    def lane_clustering(self, image: np.ndarray, min_points: int) -> np.ndarray:
        # ! this function is currently not part of the pipeline but could possibly
        # ! provide further information
        """
        - map all values to a 2d numpy array with either ones or zeros.
        - minimal threshold and start with a random 1
        - Detect all the neighbour 1s and append to cluster.
        - Safe the cluster if enough points are in the cluster.

        Clusters are enumerated, so all pixels with the same value are from one cluster.
        Cluster enumeration start with 2

        in the end, the returning array consists of the background (0) all clusters starting at 2

        Uses:
            find_neighbors -> returns a list of all coordinates of a cluster.

        Args:
            image (np.ndarray): grey rgb image of shape (h, w, 3)

        Returns:
            np.ndarray: array with the clusters.
        """

        def find_neighbors(
            image: np.ndarray, x: int, y: int, cluster_coords: set[tuple[int, int]]
        ) -> set[tuple[int, int]]:
            """
            recursive function that counts the neighbor 1s and appends the coordinates to an array.

            Args:
                image (np.ndarray): _description_
                x (int): _description_
                y (int): _description_

            Returns:
                Tuple[np.ndarray, List[Tuple[int, int]]]: Updated image and list of neighbor coordinates.
            """
            h, w = image.shape
            image[y][x] = 0
            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
            ]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and image[ny, nx] == 1:
                    cluster_coords.add((nx, ny))
                    find_neighbors(image, nx, ny, cluster_coords)

        h, w = image.shape
        current_cluster = 2

        for y in range(h):
            for x in range(w):
                if image[y, x] == 1:
                    cluster_coords = set()
                    find_neighbors(image, x, y, cluster_coords)
                    if len(cluster_coords) > min_points:
                        for i, j in cluster_coords:
                            image[i, j] = current_cluster
                        current_cluster += 1
        return image


if __name__ == "__main__":
    """for evaluation run this file"""

    ld = LaneDetection()

    i = Image.open("src/lane_detection_example.png")

    lanes = ld.evaluation_detect(np.array(i))
    from utils import test_visualize

    test_visualize(lanes)
