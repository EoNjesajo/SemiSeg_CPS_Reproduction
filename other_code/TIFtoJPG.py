import os
import cv2
from skimage.io import imread

file_path = "path to tif data dir"
save_path = "path to save dir"

for file_name in os.listdir(file_path):
    print(file_name)
    image = imread(file_path+file_name)
    image = image / (2**14-1, 2**14-1, 2**14-1, 2**14-1) *255
    image = image[...,:3]
    name = file_name.split('.')[0] + '.jpg'
    cv2.imwrite(os.path.join(save_path,name),image,[int(cv2.IMWRITE_JPEG_QUALITY), 200])
