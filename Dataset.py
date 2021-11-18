"""
Author :- Vishwash Thakur
Date:- 08/Nov/2021
"""

import os
import glob
from PIL import Image


def DataList(ImageDir):
    ImageNameList = []

    for imageFile in glob.glob(os.path.join(ImageDir,'*.jpeg')):
        imageName = imageFile.split('/')[-1].split('.')[0].split('\\')[-1]
        ImageNameList.append(imageName)
    return ImageNameList




def FileLength(fname):
    global i
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1




def DataLoader(ImageDir,AnnotationDir, NameList, Idxs):
    ImagePathList = []
    AnnotationPathList = []
    for i in Idxs:
        ImagePath = ImageDir + NameList[i] + ".jpeg"
        AnnotationPath = AnnotationDir + NameList[i] + ".txt"
        with open(AnnotationPath,"r") as f:
            num_of_objs = int(FileLength(f.name))
            image = Image.open(fp = ImagePath)
            ImageHeight, ImageWidth = image.size
            del image

            Boxes = []
            for _ in range(num_of_objs):
                for line in f.readlines():
                    obj = line.rstrip().split(" ")
                    obj = [float(j) for j in obj]
                    obj[0] = int(obj[0])

                    xmin = max(obj[1], 0) 
                    ymin = max(obj[2], 0) 
                    xmax = min(obj[3], ImageWidth) 
                    ymax = min(obj[4], ImageHeight) 

                    Boxes.append([obj[0], xmin, ymin, xmax, ymax])

            if not Boxes:
                continue

            ImagePathList.append(ImagePath)
            AnnotationPathList.append(Boxes)
    return ImagePathList, AnnotationPathList

        
            