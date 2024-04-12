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
        
        # segment left/right lane 
        # image = self.left_right_lane_detection(image)
        
        return image
        
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
