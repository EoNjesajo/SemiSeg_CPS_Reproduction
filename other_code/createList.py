import os
import cv2
import random
from skimage.io import imread
test_file_path = "/workspace/SemiSeg_CPS/DATA/cloud/val/img"
train_file_path = "/workspace/SemiSeg_CPS/DATA/cloud/train/img"
save_path = ["/workspace/SemiSeg_CPS/DATA/cloud/subset_train", "/workspace/SemiSeg_CPS/DATA/cloud"]


unlabeled_number = 2452 

file_list = sorted(os.listdir(train_file_path))
list_unlabeled = random.sample(file_list, unlabeled_number) 
list_labeled = list(set(file_list) - set(list_unlabeled))
name_unlabeled = 'train_unlabeled'
name_labeled = 'train_labeled'
print(len(list_unlabeled))
with open(os.path.join(save_path[0], name_unlabeled+".txt"),'w') as f:
    for filename in list_unlabeled:
        if filename.endswith(".jpg"):
            f.write(filename[:-4]+"\n")
print(len(list_labeled))
with open(os.path.join(save_path[0], name_labeled+".txt"),'w') as f:
    for filename in list_labeled:
        if filename.endswith(".jpg"):
            f.write(filename[:-4]+"\n")


name = "val"
file_list = sorted(os.listdir(test_file_path))
print(len(file_list))
with open(os.path.join(save_path[1], name+".txt"),'w') as f:
    for filename in file_list:
        if filename.endswith(".jpg"):
            f.write(filename[:-4]+"\n")
