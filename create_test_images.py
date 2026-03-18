import cv2
import numpy as np
import os

os.makedirs("data/input", exist_ok=True)

for i in range(10):
    img = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)

    for _ in range(np.random.randint(1, 4)):
        x = np.random.randint(50, 350)
        y = np.random.randint(50, 250)
        radius = np.random.randint(20, 40)
        color = (255, 200, 150)  # Skin tone
        cv2.circle(img, (x, y), radius, color, -1)
    
    cv2.imwrite(f"data/input/test_{i}.jpg", img)

print("Created 10 test images in data/input/")