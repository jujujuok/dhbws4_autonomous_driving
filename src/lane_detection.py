from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from pathlib import Path

CROP_CONST = 100

class LaneDetection:

    def __init__(self):
        pass

    def detect(self):
        pass



    def identify_road(self, input_image_path: Path):

        def detect_green_pixels(img: np.ndarray, threshold: int) -> np.ndarray:
            """
            Detects greenish pixels in an image.

            Parameters:
                img (np.ndarray): The image as a numpy array.
                threshold (int): Threshold value for green detection.

            Returns:
                np.ndarray: Array indicating greenish pixels (1) and non-greenish pixels (0).
            """
            h, w, _ = img.shape
            green_filter = np.zeros((h, w))

            # Loop through each pixel in the image
            for y in range(h):
                for x in range(w):
                    # Get the RGB values of the pixel
                    r, g, b = img[y][x]
                    # Check if the pixel is greenish
                    if g > r + threshold and g > b + threshold:
                        # If so, set the corresponding value in the green_filter array to 1
                        green_filter[y][x] = 1
            
            plt.imshow(green_filter)

            return green_filter
        
        def edge_detection(img: np.ndarray)-> np.ndarray:

            def cv2_sobel(grey_img: np.ndarray):
                # --- Edge detection ---
                import cv2  # todo: no cv2!

                # Apply Sobel operator in x and y directions
                sobel_x = cv2.Sobel(grey_img, cv2.CV_64F, 1, 0, ksize=3)
                sobel_y = cv2.Sobel(grey_img, cv2.CV_64F, 0, 1, ksize=3)

                # Calculate magnitude of gradients
                gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

                # Normalize gradient magnitude to range [0, 255]
                gradient_magnitude *= 255.0 / gradient_magnitude.max()

                return gradient_magnitude.astype(np.uint8)

            h, w, _ = img.shape
            img = img[:w][:h-CROP_CONST]
            
            grey_img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])

            # img = cv2_sobel(grey_img)


            

            # todo: set car to no edges

            plt.imshow(img, cmap="grey")
            plt.show()

        image = plt.imread(input_image_path)

        # green_filter = detect_green_pixels(np.array(image), 50)

        edge_detection(image)
        
        return image


if __name__ == "__main__":    # Example usage:
    input_image_path = Path("src/img/image2.png")  # Provide the path to your input image
    ld = LaneDetection()
    ld.identify_road(input_image_path)
    

# Image.fromarray(img)
# np.array(PILImage)
