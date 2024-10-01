import cv2
import numpy as np

# 读取图像
image = cv2.imread('results/mask_level_0_with_area_18540.740247363497.png', cv2.IMREAD_GRAYSCALE)

# 计算新的尺寸
height, width = image.shape
new_size = (int(width * 1.8), int(height * 1.6))

# 进行缩放
resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)

# 将白色像素点二值化
_, binary = cv2.threshold(resized_image, 240, 255, cv2.THRESH_BINARY)

# 找到轮廓
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 计算周长
perimeter = sum(cv2.arcLength(cnt, True) for cnt in contours)

print(f"白色像素点的周长: {perimeter}")
