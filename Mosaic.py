"""
Author :- Vishwash Thakur
Date:- 08/Nov/2021
"""



import random
import numpy as np
from PIL import Image






def MosaicAugmentation(ImageList, AnnotationList, OutputSize, ScaleRange, FilterScale):
    OutputImage = np.zeros([OutputSize[0], OutputSize[1], 3], dtype = np.uint8)
    ScaleX= ScaleRange[0] + random.random() * (ScaleRange[1] - ScaleRange[0])
    ScaleY = ScaleRange[0] + random.random() * (ScaleRange[1] - ScaleRange[0])
    DividePointX = int(ScaleX * OutputSize[1])
    DividePointY = int(ScaleY * OutputSize[0])

    
    NewAnnotations = []
    
    for i in range(4):
        ImgPath = ImageList[i]
        AnnotationPath = AnnotationList[i]
        
        Images = Image.open(ImgPath)
        if i == 0:                # Top-Left
            ImageResize = Images.resize(size = (DividePointX,DividePointY))
            OutputImage[:DividePointY, :DividePointX, :] = ImageResize
            # imag = Image.fromarray(OutputImage)
            # imag.show()
            for bBox in AnnotationPath:
                xmin = bBox[1] - bBox[3] * 0.5
                ymin = bBox[2] - bBox[4] * 0.5
                xmax = bBox[1] + bBox[3] * 0.5
                ymax = bBox[2] + bBox[4] * 0.5


                xmin *= ScaleX
                ymin *= ScaleY
                xmax *= ScaleX
                ymax *= ScaleY

                # xmin = bBox[1] * ScaleX
                # ymin = bBox[2] * ScaleY
                # xmax = bBox[3] * ScaleX
                # ymax = bBox[4] * ScaleY


                NewAnnotations.append([bBox[0], xmin, ymin, xmax, ymax])
        elif i == 1:                # Top-Right
            ImageResize = Images.resize(size = (OutputSize[1] - DividePointX, DividePointY))
            OutputImage[:DividePointY, DividePointX:OutputSize[1], :] = ImageResize
            # imag2 = Image.fromarray(OutputImage)
            # imag2.show()
            for bBox in AnnotationPath:
                xmin = bBox[1] - bBox[3] * 0.5
                ymin = bBox[2] - bBox[4] * 0.5
                xmax = bBox[1] + bBox[3] * 0.5
                ymax = bBox[2] + bBox[4] * 0.5


                xmin  = ScaleX + xmin * (1 - ScaleX)
                ymin *= ScaleY
                xmax  = ScaleX + xmax * (1 - ScaleX)
                ymax *= ScaleY

                # xmin = ScaleX + bBox[1] * (1 - ScaleX)
                # ymin = bBox[2] * ScaleY
                # xmax = ScaleX + bBox[3] * (1 - ScaleX)
                # ymax = bBox[4] * ScaleY

                NewAnnotations.append([bBox[0], xmin, ymin, xmax, ymax])

        elif i == 2:
            ImageResize = Images.resize(size = (DividePointX,OutputSize[0] - DividePointY))
            OutputImage[DividePointY:OutputSize[0], :DividePointX, :] = ImageResize
            # imag3 = Image.fromarray(OutputImage)
            # imag3.show()
            for bBox in AnnotationPath:
                xmin = bBox[1] - bBox[3] * 0.5
                ymin = bBox[2] - bBox[4] * 0.5
                xmax = bBox[1] + bBox[3] * 0.5
                ymax = bBox[2] + bBox[4] * 0.5


                xmin *= ScaleX
                ymin  = ScaleY + ymin * (1 - ScaleY)
                xmax *= ScaleX
                ymax  = ScaleY + ymax * (1 - ScaleY)

                # xmin = bBox[1] * ScaleX
                # ymin = ScaleY + bBox[2] * (1 - ScaleY)
                # xmax = bBox[3] * ScaleX
                # ymax = ScaleY + bBox[4] * (1 - ScaleY)

                NewAnnotations.append([bBox[0], xmin, ymin, xmax, ymax])

        else:
            ImageResize = Images.resize(size = (OutputSize[1] - DividePointX, OutputSize[0] - DividePointY))
            OutputImage[DividePointY : OutputSize[0], DividePointX : OutputSize[1], :] = ImageResize
            # imag4 = Image.fromarray(OutputImage)
            # imag4.show()
            for bBox in AnnotationPath:
                xmin = bBox[1] - bBox[3] * 0.5
                ymin = bBox[2] - bBox[4] * 0.5
                xmax = bBox[1] + bBox[3] * 0.5
                ymax = bBox[2] + bBox[4] * 0.5

                xmin = ScaleX + xmin * (1 - ScaleX)
                ymin = ScaleY + ymin * (1 - ScaleY)
                xmax = ScaleX + xmax * (1 - ScaleX)                
                ymax = ScaleY + ymax * (1 - ScaleY)

                # xmin = ScaleX + bBox[1] * (1 - ScaleX)
                # ymin = ScaleY + bBox[2] * (1 - ScaleY)
                # xmax = ScaleX + bBox[3] * (1 - ScaleX)
                # ymax = ScaleY + bBox[4] * (1 - ScaleY)


                NewAnnotations.append([bBox[0], xmin, ymin, xmax, ymax])

    if 0 < FilterScale:
        NewAnnotations = [Annotations for Annotations in NewAnnotations if FilterScale < (Annotations[3] - Annotations[1]) and FilterScale < (Annotations[4] - Annotations[2])]

    return OutputImage, NewAnnotations