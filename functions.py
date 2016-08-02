"""
    ********************************************************           
    * A module for dividing image into grids               *   
    *                                                      *   
    * Author:  Subham Roy                                  *   
    *                                                      *   
    * Originally developed for Pixelate, IIT-BHU Fest '16  *   
    *                                                      *   
    ******************************************************** 
 """

import numpy as np
import sys
from cv2 import *


def gridSize(arenaHeight, arenaLength, rows, cols):
	return [arenaHeight/rows, arenaLength/cols]

def gridVertices(arenaTopCorner, arenaHeight, arenaLength, rows, cols, tolerance):
	gridHeight, gridLength = gridSize(arenaHeight, arenaLength, rows, cols)
	arr = []
	temp = []
	for i in xrange(rows):
		for j in xrange(cols):
			temp.append([arenaTopCorner[0]+(j)*gridLength+tolerance, arenaTopCorner[1]+(i)*gridHeight+tolerance, arenaTopCorner[0]+(j+1)*gridLength-tolerance, arenaTopCorner[1]+(i+1)*gridHeight-tolerance])
		arr.append(temp)
		temp = []
	return arr
	
def flipHorizontal(img):
	#img = img[]
	print "not implemented yet"
	
def flipVertical(img):
	print "not implemented yet"
	
def gridNumber(n, rows, cols):
	if (type(n)==tuple):
		x = n[0]
		y = n[1]
#		x = rows-1-x
		return y*cols+x+1
	elif (type(n)==int):
		n=n-1
		return ((n)%cols,n/cols)
	else:
		sys.exit("Invalid values supplied")
	
def print_arr(arr): 
	for i in xrange(len(arr)):
		print str(i+1)+".) "+str(arr[i])
		
def identify_color(c):
	black_threshold = 115
	colorranges = [[0,255],[0,0],[35,50],[135,160],[180,255],[70,125]]
	#colors colorrange[i]
	#i=0 color not recognised
	#i=1 black
	#i=2 yellow
	#i=3 blue
	#i=4 red
	#i=5 green
	#######################
	h = c[0]
	s = c[1]
	l = c[2]
	if (l<black_threshold):
		return 1
	else:
		j=0
		for i in xrange(len(colorranges)-1,-1,-1):
			if (h>colorranges[i][0] and h<=colorranges[i][1]):
				return i
		
def check_if_path(c):
	black_threshold = 30
	if (c[2]<black_threshold):
		return True
	else:
		return False
			
def hue(rgb):
	hue = 0.0
	R = rgb[0]/255.0
	G = rgb[1]/255.0
	B = rgb[2]/255.0
	MAX = max(R,G,B)
	MIN = min(R,G,B)
	if (R==MAX):
		hue = (G-B)/(MAX-MIN)
	elif (G==MAX):
		hue = 2.0+(B-R)/(MAX-MIN)
	elif (B==MAX):
		hue = 4.0+(R-G)/(MAX-MIN)
	else:
		sys.exit("Undeterminable Maximum value of channels")
	hue = hue*42
	if (hue<0):
		hue+=255
	return int(hue)
	
def find_walls(arr,r,c):
	#takes color array as input
	walls = []
	for i in xrange(len(arr)):
		if (arr[i]==0):
			sys.exit("Unrecognised colors in array provided")
		elif (arr[i]!=1):
			walls.append(gridNumber(i+1,r,c))
		else:
			pass
	return walls
	
def remove_wall(arr,walls,r,c):
	if (type(arr)==list):
		for i in xrange(len(arr)):
			wall_xy = gridNumber(arr[i],r,c)
			if (wall_xy in walls):
				walls.remove(wall_xy)
		return walls
	elif (type(arr)==int):
		wall_xy = gridNumber(arr,r,c)
		if (wall_xy in walls):
			walls.remove(wall_xy)
		return walls
	else:
		sys.exit("no recognizable type")
		
def convert_xy_to_no(arr,r,c):
	ans = []
	for i in xrange(len(arr)):
		ans.append(gridNumber(arr[i],r,c))
	return ans
	
	
criticalOnOff = [4,3]
redOnOff = [13,27]
greenOnOff = [49,47]
blueOnOff = [32,30]

def actions(l,r,c):
	#f forward one block, l, r, b
	actions = []
	for i in range(len(l)-1):
		if i==0:
			actions.append('f')
		else:
			if l[i+1]-l[i]==1 and l[i]-l[i-1]==1 or l[i+1]-l[i]==7 and l[i]-l[i-1]==7:
				actions.append('f')
			elif l[i+1]-l[i]==7 and l[i]-l[i-1]==1 or l[i+1]-l[i]==1 and l[i]-l[i-1]==-7:
				actions.append('l')
				actions.append('f')
			elif l[i+1]-l[i]==1 and l[i]-l[i-1]==7 or l[i+1]-l[i]==-7 and l[i]-l[i-1]==1:
				actions.append('r')
				actions.append('f')
			elif l[i+1]-l[i]==-7 and l[i]-l[i-1]==-7:
				actions.append('f')
			elif l[i+1]-l[i]==-1 and l[i]-l[i-1]==-7:
				actions.append('r')
				actions.append('f')
			elif l[i+1]-l[i]==1  and l[i]-l[i-1]==-7:
				actions.append('l')
				actions.append('f')
			elif l[i+1]-l[i]==-1 and l[i]-l[i-1]==-1:
				actions.append('f')
			elif l[i+1]-l[i]==-1 and l[i]-l[i-1]==1:
				actions.append('b')
			elif l[i+1]-l[i]==7 and l[i]-l[i-1]==-1:
				actions.append('r')
				actions.append('f')
			elif l[i+1]-l[i]==-7 and l[i]-l[i-1]==-1:
				actions.append('l')
				actions.append('f')
	return actions
	
	
def largest_contour(img,l,h):
	if img.shape[2]==3:
		img = cvtColor(img, COLOR_BGR2GRAY)
	elif img.shape[2]==1:
		pass
	else:
		sys.exit("invalid image")
		
	mask = inRange(img,l,h)
	cnts = findContours(mask.copy(), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)[-2]
	return sorted(cnts, key=contourArea, reverse=True)[0]
	
	
class blueonoff(object):
	def __init__(self, grid):
		self.grid=grid
		self.calculategrid = 1
		
class redonoff(object):
	def __init__(self, grid):
		self.grid=grid
		self.calculategrid = 1
		
class greenonoff(object):
	def __init__(self, grid):
		self.grid=grid
		self.calculategrid = 1