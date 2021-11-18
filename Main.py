"""
Author :- Vishwash Thakur
Date:- 08/Nov/2021
"""



import os
import random
import Dataset
import Mosaic
import argparse
from PIL import Image
from datetime import datetime
import cv2


if os.path.isdir(os.getcwd() + "/Images"):
    pass
else:
    os.mkdir(os.getcwd() + "/Images")

if os.path.isdir(os.getcwd() + "/Annotations"):
    pass
else:
    os.mkdir(os.getcwd() + "/Annotations")

parser = argparse.ArgumentParser()
parser.add_argument("-Number", type = int, default = 10, help = "Number of Mosaic Augmented Images you Want")
parser.add_argument("-ImageDir",required = True, help = "Path of Base Image Directory")
parser.add_argument("-AnnotationDir",required = True, help = 'Path of Base Annotation Directory')
args = parser.parse_args()


OutputSize = (600,600)
ScaleRange = (0.3, 0.7)
FilterScale = 1/50

OutputName = "Output"

OutputImageSavedPath = os.getcwd() + "/Images"
OutputLabelSavedPath = os.getcwd() + "/Annotations"

ImageNameList = Dataset.DataList(ImageDir = args.ImageDir)


def Main():

    Idxs = random.sample(range(len(ImageNameList)), 4)

    ImagePath, AnnotationPath = Dataset.DataLoader(ImageDir = args.ImageDir, AnnotationDir = args.AnnotationDir,Idxs = Idxs, NameList = ImageNameList)

    
    OutputArray, OutputAnnotation = Mosaic.MosaicAugmentation(ImageList = ImagePath, AnnotationList = AnnotationPath, 
                                                              OutputSize = OutputSize, ScaleRange = ScaleRange,
                                                              FilterScale = FilterScale)
    
     
    DateTime = datetime.now()
    OutputImageFile = "%s.jpeg" % (OutputName + str(DateTime)) 
    OutputImage = Image.fromarray(OutputArray)
    OutputImage.save(fp = os.path.join(OutputImageSavedPath,OutputImageFile))

    for anno in OutputAnnotation:
        start_point = (int(anno[1] * OutputSize[1]), int(anno[2] * OutputSize[0]))
        end_point = (int(anno[3] * OutputSize[1]), int(anno[4] * OutputSize[0]))
        cv2.rectangle(OutputArray, start_point, end_point, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imwrite('output_box5.jpg', OutputArray)
    
    
    YoloAnnotations = []

    for i in OutputAnnotation:
        arg = []
        arg.append(i[0])
        arg.append((i[3] + i[1]) / 2)
        arg.append((i[4] + i[2]) / 2)
        arg.append(i[3] - i[1])
        arg.append(i[4] - i[2])
        YoloAnnotations.append(arg)


    OutputTxtFile = "%s.txt" % (OutputName + str(DateTime))
    with open(os.path.join(OutputLabelSavedPath,OutputTxtFile),"w") as file:
        for line in YoloAnnotations:
            file.write((' ').join([str(x) for x in line]) + '\n')



if __name__ == "__main__":
    for _ in range(args.Number):
        Main()
   

        
