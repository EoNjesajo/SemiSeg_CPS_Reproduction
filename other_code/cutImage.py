from skimage.io import imread
import cv2
import os
from PIL import Image

img_path = '/workspace/SemiSeg_CPS/DATA/Cloud_dataset/train/img_jpg' 
gt_path = '/workspace/SemiSeg_CPS/DATA/Cloud_dataset/train/gt'
save_img_path = '/workspace/SemiSeg_CPS/DATA/cloud/train/img'
save_gt_path = '/workspace/SemiSeg_CPS/DATA/cloud/train/gt'

file_list = sorted(os.listdir(img_path)) 

for i in file_list: 
     number = 0
     image = Image.open(os.path.join(img_path, i))
     label = Image.open(os.path.join(gt_path, i.split('.')[0] + '_label.png'))
     size = image.size
     weight = size[0]
     height = size[1]
     height = height-height%1203
     for h in range(0,height,1203):
         for w in range(0,weight,1203):
             box = (w, h, w+1203, h+1203)
             img = image.crop(box)
             gt = label.crop(box)
             file_name = i.split('.')[0] + '_'+str(number)
             print(file_name)
             img.save(os.path.join(save_img_path, file_name+'.jpg'))
             gt.save(os.path.join(save_gt_path, file_name+'.png'))
             number=number+1
