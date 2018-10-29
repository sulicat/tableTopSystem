import cv2 as cv
import numpy as np
import math
import sys


# goal:
#  given an image, and a stampMap, look at every stamp in stampMap
#  find the position of the stamo in image, return an array with positions/sizex of
#  each stamp in that image
