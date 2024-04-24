import matplotlib.pyplot as plt
import numpy as np

def test_visualize(image: np.ndarray):
    import cv2
    image = image * 255

    cv_image = np.asarray(image, dtype=np.uint8)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    cv_image = cv2.resize(cv_image, np.asarray(image.shape[:2]) * 6)
    cv2.imshow('Car Racing - Lane Detection', cv_image)
    cv2.waitKey(1)


def show_plt_img_grey(image: np.ndarray):
    plt.imshow(image, cmap="grey")
    plt.show()

def vector_length(vector: np.ndarray) -> float:
    return np.linalg.norm(vector)

def angle_of_vectors(a: np.ndarray, b: np.ndarray) -> float:
    """
    Raises:
        ValueError: some vector has 0 length 

    Returns:
        float: the angle (0-180 degrees) between 2 vectors
    """
    dot_product = np.dot(a, b)
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    
    if a_norm == 0 or b_norm == 0:
        raise ValueError("One or both vectors have zero length.")
    
    cos_theta = dot_product / (a_norm * b_norm)
    theta_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    theta_deg = np.degrees(theta_rad)
    
    return theta_deg