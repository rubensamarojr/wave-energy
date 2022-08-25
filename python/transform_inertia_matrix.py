# Plot DeepCwind displacements (Surge, Heave, Pitch)

# importing the required modules
import numpy as np
import math

#####################################
def rotate_inertia_about_x(I, angle):
	"""
	Returns inertia tensor rotated through angle about the X axis.
	Parameters
	----------
	I : ndarray, shape(3,)
		An inertia tensor.
	angle : float
		Angle in radians about the positive X axis of which to rotate the
		inertia tensor.
	"""
	ca = np.cos(angle)
	sa = np.sin(angle)
	Rx = np.matrix([[1., 0. , 0.],
					[0., ca, sa],
					[0., -sa, ca]])
	Irot = Rx * I * Rx.T
	return np.array(Irot)

#####################################
def rotate_inertia_about_y(I, angle):
	"""
	Returns inertia tensor rotated through angle about the Y axis.
	Parameters
	----------
	I : ndarray, shape(3,)
		An inertia tensor.
	angle : float
		Angle in radians about the positive Y axis of which to rotate the
		inertia tensor.
	"""
	ca = np.cos(angle)
	sa = np.sin(angle)
	Ry = np.matrix([[ca, 0., -sa],
					[0., 1., 0.],
					[sa, 0., ca]])
	Irot = Ry * I * Ry.T
	return np.array(Irot)

#####################################
def rotate_inertia_about_z(I, angle):
	"""
	Returns inertia tensor rotated through angle about the Z axis.
	Parameters
	----------
	I : ndarray, shape(3,)
		An inertia tensor.
	angle : float
		Angle in radians about the positive Z axis of which to rotate the
		inertia tensor.
	"""
	ca = np.cos(angle)
	sa = np.sin(angle)
	Rz = np.matrix([[ca, sa , 0.],
					[-sa, ca, 0.],
					[0., 0., 1.]])
	Irot = Rz * I * Rz.T
	return np.array(Irot)


# Principal Inertia matrix
Ixx = 0.0
Iyy = 124.26
Izz = 1.0
# Angle in degrees
theta = 135.0

theta = theta * np.pi / 180.0

Io = np.matrix([[Ixx, 0. , 0.],
				[0., Iyy, 0.],
				[0., 0., Izz]])

Ir = rotate_inertia_about_z(Io, theta)

print(Ir)