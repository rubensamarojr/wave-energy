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
import numpy as np

# Model scale (reduction)
scale0 = 5.0
# Initial rotation
thetaX0 = 90.0
thetaY0 = 0.0
thetaZ0 = -90.0
# Initial translation in z
zSWL = 1.0
# Forced velocities (NOT WORKING!)
xVel = 0.0
yVel = 0.0
zVel = 10.0

# Initialise time (file number actually)
executive = self.GetExecutive() 
outInfo = executive.GetOutputInformation(0)
ts= outInfo.Get(executive.UPDATE_TIME_STEP())
t=float(ts)

pointsScaled0 = inputs[0].Points

# Set Bounds from input0
bounds=np.zeros(6)
inputs[0].GetBounds(bounds)
center = ((bounds[0] + bounds[1])/2,
          (bounds[2] + bounds[3])/2,
          (bounds[4] + bounds[5])/2)

# Translate points to center
#pointsScaled0 = (pointsScaled0 + [-center[0],-center[1],-center[2]])
# Impose motion
R2 = numpy.array([ 
[cos(zVel*t)*cos(yVel*t) , cos(zVel*t)*sin(yVel*t)*sin(xVel*t) - sin(zVel*t)*cos(xVel*t) , cos(zVel*t)*sin(yVel*t)*cos(xVel*t) + sin(zVel*t)*sin(xVel*t)] , 
[sin(zVel*t)*cos(yVel*t) , sin(zVel*t)*sin(yVel*t)*sin(xVel*t) + cos(zVel*t)*cos(xVel*t) , sin(zVel*t)*sin(yVel*t)*cos(xVel*t) - cos(zVel*t)*sin(xVel*t)] , 
[-sin(yVel*t) , cos(yVel*t)*sin(xVel*t) , cos(yVel*t)*cos(xVel*t)] 
])
#pointsScaled0 = R2.dot(pointsScaled0.T).T
# Translate points to original position
#pointsScaled0 = (pointsScaled0 + [+center[0],+center[1],+center[2]])


# Set Bounds from input0
bounds=np.zeros(6)
inputs[0].GetBounds(bounds)
center = ((bounds[0] + bounds[1])/2,
          (bounds[2] + bounds[3])/2,
          (bounds[4] + bounds[5])/2)

# Translate points to center
pointsScaled0 = (pointsScaled0 + [-center[0],-center[1],-center[2]]).T
# Scale
pointsScaled0 = pointsScaled0/scale0
# Translate points to original position
pointsScaled0 = (pointsScaled0.T + [+center[0]/scale0,+center[1]/scale0,+center[2]/scale0]).T
# Rotate initial points
thetaX0 = float(thetaX0*np.pi/180.0)
thetaY0 = float(thetaY0*np.pi/180.0)
thetaZ0 = float(thetaZ0*np.pi/180.0)
R0 = numpy.array([ 
[cos(thetaZ0)*cos(thetaY0) , cos(thetaZ0)*sin(thetaY0)*sin(thetaX0) - sin(thetaZ0)*cos(thetaX0) , cos(thetaZ0)*sin(thetaY0)*cos(thetaX0) + sin(thetaZ0)*sin(thetaX0)] , 
[sin(thetaZ0)*cos(thetaY0) , sin(thetaZ0)*sin(thetaY0)*sin(thetaX0) + cos(thetaZ0)*cos(thetaX0) , sin(thetaZ0)*sin(thetaY0)*cos(thetaX0) - cos(thetaZ0)*sin(thetaX0)] , 
[-sin(thetaY0) , cos(thetaY0)*sin(thetaX0) , cos(thetaY0)*cos(thetaX0)] 
])
pointsScaled0 = R0.dot(pointsScaled0).T
# Translate points
pointsScaled0 = (pointsScaled0 + [0,0,zSWL/scale0])

# Translate points to center
#pointsScaled0 = (pointsScaled0 + [-center[0]/scale0,-center[1]/scale0,-center[2]/scale0])

# Translate points to original position
#pointsScaled0 = (pointsScaled0 + [+center[0]/scale0,+center[1]/scale0,+center[2]/scale0])

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

# from body to inertial frame
R1 = numpy.array([ 
[cos(yaw)*cos(pitch) , cos(yaw)*sin(pitch)*sin(roll) - sin(yaw)*cos(roll) , cos(yaw)*sin(pitch)*cos(roll) + sin(yaw)*sin(roll)] , 
[sin(yaw)*cos(pitch) , sin(yaw)*sin(pitch)*sin(roll) + cos(yaw)*cos(roll) , sin(yaw)*sin(pitch)*cos(roll) - cos(yaw)*sin(roll)] , 
[-sin(pitch) , cos(pitch)*sin(roll) , cos(pitch)*cos(roll)] 
])

# Output points
output.Points = R1.dot(pointsScaled0.T).T
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