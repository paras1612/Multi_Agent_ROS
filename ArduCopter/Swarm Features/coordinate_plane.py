#!/usr/bin/env python
import math
import time
import utm
import numpy as np
import matplotlib.pyplot as plt

test_cordinates = [(0, 0, 0), (1, 2 ,5), (1, -6, 12)]

def get_plane_eqn(point1, point2, point3): # Gives the eqn of plane passing through these points in ax + by + cz + d = 0 where d = 0
	a1 = point2[0] - point1[0] 
	b1 = point2[1] - point1[1] 
	c1 = point2[2] - point1[2] 
	a2 = point3[0] - point1[0] 
	b2 = point3[1] - point1[1] 
	c2 = point3[2] - point1[2] 
	a = b1 * c2 - b2 * c1 
	b = a2 * c1 - a1 * c2 
	c = a1 * b2 - b1 * a2 
	# d = (- a * point1[0] - b * point1[1] - c * point1[2]) Thiss must be zero
	return a,b,c


def noramlized_vector(vector): # Makes unit vector 
	denominator = math.sqrt(sum([x**2 for x in vector]))
	return vector[0]/denominator, vector[1]/denominator, vector[2]/denominator

def get_transformation_matrix(plane):
	'''
	Gives the tranfromattion matrix to take the standard basis to a basis where i and j land on the plane and z is perpendicular to it.
	Args: plane: The plane (a,b,c) for ax + by + cz = 0
	'''
	trans = [[]]*3
	trans[0] = [1, 0, plane[0]/plane[2]]
	trans[1] = [0, 1, plane[1]/plane[2]]
	trans[2] = [(-plane[0]/plane[2]), (-plane[1]/plane[2]), 1]
	return trans

def print_mat(mat):
	for row in mat:
		for col in row:
			print col,
		print('')


def cross_product(v1, v2):
  return np.cross(v1, v2)

def length(v):
	return math.sqrt(sum([x**2 for x in v]))

def angle(v1, v2):
  return math.asin(length(cross_product(v1, v2)) / (length(v1) * length(v2)))

trans_inverse = np.linalg.inv(get_transformation_matrix(get_plane_eqn(test_cordinates[0], test_cordinates[1], test_cordinates[2])))
print trans_inverse
plane_wp1 = np.matmul(trans_inverse, test_cordinates[0])
plane_wp2 = np.matmul(trans_inverse, test_cordinates[1])
plane_wp3 = np.matmul(trans_inverse, test_cordinates[2])
print plane_wp1, plane_wp2, plane_wp3
Line1 = plane_wp1 - plane_wp2
Line2 = plane_wp3 - plane_wp2
K = 1 # ratio(path travelled, angle turn)
print ''
print Line1, Line2
print ''
theta = angle(Line1, Line2)
print theta
turn_radius = K*theta/(math.pi - theta)
print turn_radius
#acute_angle_bisector =  

print(get_plane_eqn(test_cordinates[0], test_cordinates[1], test_cordinates[2]))
print_mat(get_transformation_matrix(get_plane_eqn(test_cordinates[0], test_cordinates[1], test_cordinates[2])))

#print noramlized_vector(test_cordinates[1])