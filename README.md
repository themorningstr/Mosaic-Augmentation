# Mosaic-Augmentation

Mosaic Augmentation technique is a kind of Data augmention technique introduce in YoloV5.

To Run the Main.py it require 3 command line argument

1.  Number of Images you want
2.  Path of Base image directory
3.  Path of Base label directory

Run this Code on your terminal 
python Main.py -Number X -ImageDir /path/of/iamge/directory -AnnotationDir path/of/annotation/directory

Default image format is "jpeg"
if you have "jpg", "png" then do the change in Dataset.py & Main.py to get the desired image format
