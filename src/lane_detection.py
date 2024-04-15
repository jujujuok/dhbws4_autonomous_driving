from __future__ import annotations

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from structs_and_configs import ConfigLaneDetection, CarConst

from helper import show_plt_img_grey

from lane_detection_helper import detect_green_pixels, edge_detect_scipy, edge_detection

class LaneDetection:

    def __init__(self):
        self.evaluate = False #ConfigLaneDetection.evaluate
        
    def evaluation_detect(self, image):
        images = {
            "green": detect_green_pixels(image, threshold=50),
            "edge detect": edge_detection(image),
            "scipy": edge_detect_scipy(image),
        }

        plt.figure(figsize=(12, 6))

        for i, (title, img) in enumerate(images.items()):
            plt.subplot(1, len(images), i + 1)
            plt.imshow(img, cmap="gray")
            plt.title(title)

        plt.show()
        
        return images["scipy"]
        
    def detect(self, image: np.ndarray):
        print(image.shape)
        
        image = image[:,:,:3]
        
        # crop info display
        image = image[:image.shape[0]-ConfigLaneDetection.displaycrop, :, :]
        
        # mask the car
        image[CarConst.start_h:CarConst.end_h, 
              CarConst.start_w:CarConst.end_w, 
              :] = np.zeros((102, 68, 3))
        
        image = edge_detect_scipy(image) if not self.evaluate else self.evaluation_detect(image)
        
        show_plt_img_grey(image=image)
        
        # image = (image > 40).astype(np.uint8)
        
        # segment left/right lane 
        # image = self.lane_clustering(image, 50)
        
        # plt.imshow(image, cmap='viridis')  
        # plt.colorbar() 
        # plt.title('Lane Clusters')
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # plt.show()
        
        return image

    def lane_clustering(self, image: np.ndarray, min_points: int) -> np.ndarray:
        """
        todo this doesnt work recursively because the stack is too small
        
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
        def find_neighbors(image: np.ndarray, x: int, y: int, cluster_coords: set[tuple[int, int]]) -> set[tuple[int, int]]:
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
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

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
                        for i, j  in cluster_coords:
                            image[i,j] = current_cluster 
                        current_cluster += 1  
        return image
        



if __name__ == "__main__":
    ld = LaneDetection()
    i = Image.open("/home/juju/dev/dhbws4_autonomous_driving/src/img/image.jpg")
    ld.detect(np.array(i))



"""
def cv2_sobel(grey_img: np.ndarray):
    # --- Edge detection ---
    import cv2

    # Apply Sobel operator in x and y directions
    sobel_x = cv2.Sobel(grey_img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(grey_img, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate magnitude of gradients
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # Normalize gradient magnitude to range [0, 255]
    gradient_magnitude *= 255.0 / gradient_magnitude.max()

    return gradient_magnitude.astype(np.uint8)
"""
