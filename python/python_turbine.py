# https://discourse.paraview.org/t/transform-geometry-based-on-input-from-a-table-of-points/5816

# Paraview script to move (translation and rotation) a STL mesh following CSV files with 
# surge, sway, heave, roll, pitch, yaw

# In Paraview, Open STL file and group of CSV files
# Apply filter TableToPoints to CSV files
# TableToPoints should have Keep All Data Arrays ticked
# Select geometry and Ctrl+TabletoPoints
# Filters -> Alphabetical -> ProgrammableFilter

# Below there are 2 script thta need to be copied to Paraview in 
# Script and RequestInformation Script fields

# 1 - COPY THIS TO Script
# https://discourse.paraview.org/t/transform-geometry-based-on-input-from-a-table-of-points/5816
import numpy as np

# Quaternion is not used
def get_quaternion_from_euler(roll, pitch, yaw):
  """
  Convert an Euler angle to a quaternion.
   
  Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
  """
  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
  return [qx, qy, qz, qw]

scale0 = 50.0
theta0 = -30.0
zSWL = 20.0

# Set Bounds from input0
bounds=np.zeros(6)
inputs[0].GetBounds(bounds)
center = ((bounds[0] + bounds[1])/2,
          (bounds[2] + bounds[3])/2,
          (bounds[4] + bounds[5])/2)
# Translate points to center
pointsScaled0 = (inputs[0].Points + [-center[0],-center[1],-center[2]]).T
# Scale
pointsScaled0 = pointsScaled0/scale0
# Translate points from center
pointsScaled0 = (pointsScaled0.T + [+center[0]/scale0,+center[1]/scale0,+center[2]/scale0-zSWL/scale0]).T
# Rotate initial points
theta0 = float(theta0*np.pi/180.0)
R0 = numpy.array([ 
[cos(theta0) , - sin(theta0) , 0.0] , 
[sin(theta0) , cos(theta0) , 0.0] , 
[0.0 , 0.0 , 1.0] 
])
pointsScaled0 = R0.dot(pointsScaled0).T

#get cog and angles from the cvs file (TableToPoints)
input1=inputs[1]
x_cg=input1.PointData["surge [m]"]*1
y_cg=input1.PointData["sway [m]"]*1
z_cg=(input1.PointData["heave [m]"])*1

yaw=float(input1.PointData["yaw [deg]"]*np.pi/180)
pitch=float(-input1.PointData["pitch [deg]"]*np.pi/180)
roll=float(input1.PointData["roll [deg]"]*np.pi/180)

#initiliase the geometry class
pdi = self.GetPolyDataInput()
pdo =  self.GetPolyDataOutput()

#initialise time (file number actually)
executive = self.GetExecutive() 
outInfo = executive.GetOutputInformation(0)
ts= outInfo.Get(executive.UPDATE_TIME_STEP())
t=float(ts)

# Euler to quaternion
#[qx, qy, qz, qw] = get_quaternion_from_euler(roll, pitch, yaw)

# Rotate vectors
#vecsq_rotated = qrot * vecsq * qrot.conjugate()

# from body to inertial frame
R = numpy.array([ 
[cos(yaw)*cos(pitch) , cos(yaw)*sin(pitch)*sin(roll) - sin(yaw)*cos(roll) , cos(yaw)*sin(pitch)*cos(roll) + sin(yaw)*sin(roll)] , 
[sin(yaw)*cos(pitch) , sin(yaw)*sin(pitch)*sin(roll) + cos(yaw)*cos(roll) , sin(yaw)*sin(pitch)*cos(roll) - cos(yaw)*sin(roll)] , 
[-sin(pitch) , cos(pitch)*sin(roll) , cos(pitch)*cos(roll)] 
])
output.Points = R.dot(pointsScaled0.T).T
output.Points = (output.Points.T+[x_cg,y_cg,z_cg]).T

#print(pointsScaled0[0])
#print(type(pointsScaled0))
#newP = np.dot(inputs[0].Points, R.T).T
#output.Points = newP.T
#output.Points = (output.Points.T+[x_cg,y_cg,z_cg]).T



# 2 - COPY THIS TO RequestInformation Script
def setOutputTimesteps(algorithm , timesteps):
    "helper routine to set timestep information"
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
 
    outInfo.Remove(executive.TIME_STEPS())
    for timestep in timesteps:
        outInfo.Append(executive.TIME_STEPS(), timestep)

    outInfo.Remove(executive.TIME_RANGE())
    outInfo.Append(executive.TIME_RANGE(), timesteps[0])
    outInfo.Append(executive.TIME_RANGE(), timesteps[-1])

setOutputTimesteps(self,(0,0))