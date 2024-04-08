from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from pathlib import Path
from time import time
from scipy.signal import convolve2d


CROP_CONST = 100


class LaneDetection:

    def __init__(self):
        pass

    def detect(self):
        pass

    def identify_road(self, input_image_path: Path):
        
        def detect_green_pixels(img: np.ndarray, threshold: int) -> np.ndarray:
            """ Detects greenish pixels in an image. 
            Only works with default image input, not changed color. 

            Args:
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

        def edge_detection(img: np.ndarray) -> np.ndarray:
            """Best one but slow

            Args:
                img (np.ndarray): input image

            Returns:
                np.ndarray: output edge detection
            """

            def sobel_edge_detection(image: np.ndarray):
                # Convert the image to grayscale
                grey_img = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
                
                # Sobel operator kernels
                kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
                kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
                
                # Perform convolution
                gradient_x = convolve(grey_img, kernel_x)
                gradient_y = convolve(grey_img, kernel_y)
                
                # Compute magnitude of gradients
                sobel_mag = np.sqrt(gradient_x**2 + gradient_y**2)
                
                return sobel_mag

            def convolve(image: np.ndarray, kernel: np.ndarray):
                # Get dimensions of the image and kernel
                image_height, image_width = image.shape
                kernel_height, kernel_width = kernel.shape
                
                # Calculate padding
                pad_height = kernel_height // 2
                pad_width = kernel_width // 2
                
                # Pad the image
                padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)), mode='edge')
                
                # Perform convolution using numpy
                output_image = np.zeros_like(image)
                for i in range(image_height):
                    for j in range(image_width):
                        output_image[i, j] = np.sum(padded_image[i:i+kernel_height, j:j+kernel_width] * kernel)
                
                return output_image
            
            # todo: set car to no edges

            h, w, _ = img.shape
            img = img[:w][: h - CROP_CONST]
            sobel_result = sobel_edge_detection(img)

            # Display the result
            plt.imshow(sobel_result, cmap='gray')
            plt.show()

        def edge_detect_scipy(img: np.ndarray) -> np.ndarray:
            """ Fast, but not optimal output so far. 

            Args:
                img (np.ndarray): input image frame

            Returns:
                np.ndarray: detected edges
            """
            
            grey_img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])
            
            # Sobel operator kernels
            kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

            # Perform convolution
            result_x = convolve2d(grey_img, kernel_x, mode="same", boundary="symm")
            result_y = convolve2d(grey_img, kernel_y, mode="same", boundary="symm")

            # Compute magnitude of the gradient
            magnitude = np.sqrt(result_x**2 + result_y**2)

            # Compute orientation of the gradient (in radians)
            orientation = np.arctan2(result_y, result_x)

            # Combine magnitude and orientation into a single numpy array
            edge_combined = np.stack((magnitude, orientation), axis=-1)

            print(f"calculation time: {time() - t} ms")

            # sobel_result = sobel_edge_detection(img)

            # Display the result
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 4, 1)
            plt.imshow(grey_img, cmap="gray")
            plt.title("Original Image")

            plt.subplot(1, 4, 2)
            plt.imshow(result_x, cmap="gray")
            plt.title("Convolved x_kernel")

            plt.subplot(1, 4, 3)
            plt.imshow(result_y, cmap="gray")
            plt.title("Convolved y_kernel")

            plt.subplot(1, 4, 4)
            plt.imshow(edge_combined, cmap="gray")
            plt.title("Combined Edge Detection")

            plt.show()
            
            
            
        image = plt.imread(input_image_path)
        
        # green_filter = detect_green_pixels(np.array(image), 50)

        edge_detection(image)

        return image


if __name__ == "__main__":  # Example usage:
    input_image_path = Path(
        "src/img/image2.png"
    )  # Provide the path to your input image
    ld = LaneDetection()
    ld.identify_road(input_image_path)


# Image.fromarray(img)
# np.array(PILImage)
"""
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

    return gradient_magnitude.astype(np.uint8)"""
    
    
    
"""
        

"""