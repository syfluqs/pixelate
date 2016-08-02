import cv2
from cv2 import *
import numpy as np
import image_slicer as imslice
##cam=VideoCapture(0)
##s,img1=cam.read()
##if s:
	
img1=cv2.imread('C:\Users\Avi97\Pictures\pixelate arena.png')	
##cv2.imshow("original arena",img1)
blue_component=img1.copy()
green_component=img1.copy()
red_component=img1.copy()

no_rows=img1.shape[0]
no_cols=img1.shape[1]

for row in range(no_rows):
    for col in range(no_cols):
	red=red_component[row,col,0]
	red_component[row,col]=[0,0,red]
cv2.imwrite('red.png',red_component)
red=cv2.imread('red.png')
for row in range(no_rows):
    for col in range(no_cols):
	blue=blue_component[row,col,1]
	blue_component[row,col]=[blue,0,0]
cv2.imwrite('blue.png',blue_component)
blue=cv2.imread('blue.png')

for row in range(no_rows):
    for col in range(no_cols):
	green=green_component[row,col,2]
	green_component[row,col]=[0,green,0]
cv2.imwrite('green.png',green_component)
green=cv2.imread('green.png')


cv2.imshow ("original frame",img1)

cv2.imshow('red',red)

cv2.imshow('blue',blue)

cv2.imshow('green',green)
cv2.waitKey(0)

