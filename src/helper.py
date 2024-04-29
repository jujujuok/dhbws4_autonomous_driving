import matplotlib.pyplot as plt
import numpy as np


def show_plt_img_grey(image: np.ndarray):
    """
    Zeigt ein Bild in Graustufen mit Matplotlib an.
    Args:
        image (np.ndarray): Das Bild, das angezeigt werden soll.
    """
    plt.imshow(image, cmap="grey")
    plt.show()


def vector_length(vector: np.ndarray) -> float:
    """
    Berechnet die Länge eines Vektors.
    Args:
        vector (np.ndarray): Der Vektor, dessen Länge berechnet werden soll.
    Returns:
        float: Die Länge des Vektors.
    """
    return np.linalg.norm(vector)


def angle_of_vectors(a: np.ndarray, b: np.ndarray) -> float:
    """
    Berechnet den Winkel zwischen zwei Vektoren.
    Args:
        a (np.ndarray): Der erste Vektor.
        b (np.ndarray): Der zweite Vektor.
    Raises:
        ValueError: Einer oder beide Vektoren haben eine Länge von 0.
    Returns:
        float: Der Winkel (0-180 Grad) zwischen den beiden Vektoren.
    """
    dot_product = np.dot(a, b)
    print("dot ", dot_product)
    a_norm = np.linalg.norm(a)

    b_norm = np.linalg.norm(b)

    # Überprüfen, ob einer oder beide Vektoren eine Länge von 0 haben
    if a_norm == 0 or b_norm == 0:
        raise ValueError("One or both vectors have zero length.")

    cos_theta = dot_product / (a_norm * b_norm)
    print("cos ", cos_theta)
    theta_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    theta_deg = np.degrees(theta_rad)

    return theta_deg
