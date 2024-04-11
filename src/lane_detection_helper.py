import numpy as np
import matplotlib.pyplot as plt
from time import time
from scipy.signal import convolve2d

from structs_and_configs import DEBUG, ConfigLaneDetection

def detect_green_pixels(img, threshold: int, debug: bool = False) -> np.ndarray:
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

    if debug:
        print(f"green_filter calculation time: {time() - t} ms")
        plt.imshow(green_filter)

    return green_filter


@staticmethod
def edge_detection(img: np.ndarray, debug: bool = False) -> np.ndarray:
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

    if debug:
        # -------- Display the result ---------
        print(f"edge detection calculation time: {time() - t} ms")

        plt.imshow(sobel_result, cmap="gray")
        plt.show()

    return sobel_result


@staticmethod
def edge_detect_scipy(img: np.ndarray, debug: bool = False) -> np.ndarray:
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
    magnitude *= 255.0 / np.max(magnitude)

    if debug:
        print(f"scipy calculation time: {time() - t} ms")

        # -------- Display the result ---------
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.imshow(grey_img, cmap="gray")
        plt.title("Original Image")

        plt.subplot(1, 2, 2)
        plt.imshow(magnitude, cmap="gray")
        # plt.colorbar(label='Magnitude')  # todo
        plt.title("Magnitude")

        plt.show()
    return magnitude

