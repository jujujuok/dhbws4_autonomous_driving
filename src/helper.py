import matplotlib.pyplot as plt
import numpy as np


def show_plt_img_grey(image: np.ndarray):
    plt.imshow(image, cmap="grey")
    plt.show()
