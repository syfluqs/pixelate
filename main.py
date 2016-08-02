#!/usr/bin/env python2

from cv2 import *
from math import *
import sys
import functions
import numpy as np
import serial
import time
from astar3 import *

#######################################
#              Variables              #
#    Check before running the code    #
#######################################
debug = 1
manual = 1
manual_single_iteration = 1
manual_img = 's.png'
showgrid = 1
serial_on = 0
coordinate_on = 0
# The camera device number
cameraDevice = 1
# The arena is being
# cropped from the rest of the image 
# by using slicling. arenaTopCorner
# defines the top left corner of arena
# as the origin and arenaHeight defines
# the width of face
arenaTopCorner = [14,48]
arenaHeight = 525
arenaLength = 450
# Arena is divided in rows and Cols
arenaRows = 8
arenaCols = 7
#slicing tolerance
tolerance = 1
#######################################
#######################################
#Natural number representation
start = 1
stop = 4
critical = [10,11,17,18]
blue = [15,22,27]
red = [29,36,38]
green = [43,50,48]
criticalOnOff = [4,3]
redOnOff = [47,49]
greenOnOff = [49,47]
blueOnOff = [20,34]
path = []
	
	
def coordinate(actions):
	for i in xrange(len(actions)):		
		arduino.write(actions[i])
		while arduino.read()!='K':
			pass
	
if (not manual):
	cam = VideoCapture(cameraDevice)
	frameHeight = int(cam.get(4))
	frameWidth = int(cam.get(3))
else:
	overlay = imread(manual_img)
	frameHeight = overlay.shape[0]
	frameWidth = overlay.shape[1]
	
"""if (manual):
	frameHeight = 484
	frameWidth = 642"""
gridSize = functions.gridSize(arenaHeight, arenaLength, arenaRows, arenaCols)
gridVertices = functions.gridVertices(arenaTopCorner, arenaHeight, arenaLength, arenaRows, arenaCols, tolerance)
if (debug):
	print "frameHeight = "+str(frameHeight)
	print "frameWidth = "+str(frameWidth)
	print "gridSize = "+str(gridSize)
	print "gridVertices = "+str(gridVertices)

#check video dimensions
if (arenaTopCorner[1]+arenaHeight>frameHeight or arenaTopCorner[0]+arenaLength>frameWidth):
	sys.exit("Frame size Mismatch, check arenaHeight and arenaLength")
	
if (serial_on):
	print "Initialising Serial"
	arduino = serial.Serial("COM10", 9600, timeout=1)
	
while(1):
	if (manual):
		s = overlay
	else:
		ret, s = cam.read()
	
	hsv = cvtColor(s, COLOR_BGR2HSV)
	"""
	if (manual):
		for i in xrange(0, overlay.shape[0]):
			for j in xrange(0, overlay.shape[1]):
				img[arenaTopCorner[1]+i, arenaTopCorner[0]+j] = overlay[i, j]
		"""
	#crop = s[arenaTopCorner[0]:arenaTopCorner[0]+arenaHeight, arenaTopCorner[0]:arenaTopCorner[0]+arenaLength]
	if (showgrid):
		for i in xrange(arenaRows):
			for j in xrange(arenaCols):
				rectangle(s, (gridVertices[i][j][0], gridVertices[i][j][1]), (gridVertices[i][j][2], gridVertices[i][j][3]), (0,0,255), 1)
		
	# examining the grid
	# grid numbering starts from bottom left corner and moves right and up
	grid = []
	for i in xrange(arenaRows-1, -1, -1):
		for j in xrange(arenaCols):
			grid.append(hsv[gridVertices[i][j][1]:gridVertices[i][j][3], gridVertices[i][j][0]:gridVertices[i][j][2]])
	# calculating average color of every box
	avg_arr = []
	color = []
	for i in xrange(len(grid)):
		temp,std = meanStdDev(grid[i])
		#temp = np.concatenate([temp,std])
		t = [int(floor(temp[0]*240/180)),int(floor(temp[1]*240/255)),int(floor(temp[2]*240/255))]
		avg_arr.append(t)
		color.append(functions.identify_color(t))
		#if (functions.check_if_path(t)):
		#	path.append(i+1)
	
	#if (debug):
	#	print "path = "+str(path)
		
	imshow("img",s)
	#waitKey(0)
	
	if manual or manual_single_iteration:
		waitKey(0)
		
		#find path
		o = AStar()
		walls = functions.find_walls(color,arenaRows,arenaCols)
		walls = functions.remove_wall(criticalOnOff[0],walls,arenaRows,arenaCols)
		walls = functions.remove_wall(redOnOff,walls,arenaRows,arenaCols)
		walls = functions.remove_wall(blueOnOff,walls,arenaRows,arenaCols)
		walls = functions.remove_wall(greenOnOff,walls,arenaRows,arenaCols)
		o.init_grid(arenaCols, arenaRows, walls, functions.gridNumber(start,arenaRows,arenaCols), functions.gridNumber(stop,arenaRows,arenaCols))
		way = o.solve()
		way = functions.convert_xy_to_no(way,arenaRows,arenaCols)
		actions = functions.actions(way,arenaRows,arenaCols);
		if (debug):
			print "walls:",walls
			print "way:",way
			print "actions:",actions
		
		if coordinate_on and serial_on:
			coordinate(actions)
		
		break
	if waitKey(1) & 0xFF == ord('q'):
		break

if (not manual):
	cam.release()
	
destroyAllWindows()

def check_data():
	print "Total elements = "+str(len(path)+len(critical)+len(blue)+len(red)+len(green)+len(redOnOff)+len(greenOnOff)+len(blueOnOff)+len(criticalOnOff))