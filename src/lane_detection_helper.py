import numpy as np
import matplotlib.pyplot as plt
from time import time
from scipy.signal import convolve2d

from structs_and_configs import ConfigLaneDetection


def detect_green_pixels(img, threshold: int) -> np.ndarray:
    """Detects greenish pixels in an image.
    Only works with default image input, not changed color.

    Args:
        img (np.ndarray): The image as a numpy array.
        threshold (int): Threshold value for green detection.

    Returns:
        np.ndarray: Array indicating greenish pixels (1) and non-greenish pixels (0).
    """
    t = time()

    img = np.array(img)

    # Extract RGB channels
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    # Check condition for greenish pixels
    green_mask = (g > r + threshold) & (g > b + threshold)

    green_mask = green_mask.astype(int)

    if ConfigLaneDetection.debug:
        print(f"green_filter calculation time: {time() - t} ms")
        plt.imshow(green_mask)

    return green_mask


def edge_detection(img: np.ndarray) -> np.ndarray:
    """Best one but slow

    Args:
        img (np.ndarray): input image

    Returns:
        np.ndarray: output edge detection
    """

    def sobel_edge_detection(image: np.ndarray):
        # grayscale
        grey_img = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])

        kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

        gradient_x = convolve(grey_img, kernel_x)
        gradient_y = convolve(grey_img, kernel_y)

        # magnitude of gradients
        sobel_mag = np.sqrt(gradient_x**2 + gradient_y**2)

        return sobel_mag

    def convolve(image: np.ndarray, kernel: np.ndarray):
        image_height, image_width = image.shape
        kernel_height, kernel_width = kernel.shape

        # padding
        pad_height = kernel_height // 2
        pad_width = kernel_width // 2

        padded_image = np.pad(
            image,
            ((pad_height, pad_height), (pad_width, pad_width)),
            mode="edge",
        )

        output_image = np.zeros_like(image)
        for i in range(image_height):
            for j in range(image_width):
                output_image[i, j] = np.sum(
                    padded_image[i : i + kernel_height, j : j + kernel_width] * kernel
                )

        return output_image

    t = time()

    sobel_result = sobel_edge_detection(img)

    if ConfigLaneDetection.debug:
        # -------- Display the result ---------
        print(f"edge detection calculation time: {time() - t} ms")

        plt.imshow(sobel_result, cmap="gray")
        plt.show()

    return sobel_result


def edge_detect_scipy(img: np.ndarray) -> np.ndarray:
    """Fast, but not optimal output so far.

    Args:
        img (np.ndarray): input image frame

    Returns:
        np.ndarray: detected edges
    """
    t = time()

    grey_img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])

    # Sobel operator kernels
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # Perform convolution
    result_x = convolve2d(grey_img, kernel_x, mode="same", boundary="symm")
    result_y = convolve2d(grey_img, kernel_y, mode="same", boundary="symm")

    # Compute magnitude of the gradient
    magnitude = np.sqrt(result_x**2 + result_y**2)

    # Normalize magnitude to lie between 0 and 255
    # magnitude *= 255.0 / np.max(magnitude)
    
    threshold = 70
    magnitude = (magnitude > threshold) * 255

    if ConfigLaneDetection.debug:
        print(f"scipy calculation time: {time() - t} ms")

        # -------- Display the result ---------
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.imshow(grey_img, cmap="gray")
        plt.title("Original Image")

        plt.subplot(1, 2, 2)
        plt.imshow(magnitude, cmap="gray")
        
        plt.title("Raw output of edge detection with scipy")

        plt.show()
    return magnitude
