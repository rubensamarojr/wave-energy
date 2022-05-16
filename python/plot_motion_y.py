# Plot wavestar cylinder displacements
# E. J. Ransley, 2017. RANS-VOF modelling of the Wavestar point absorber
# Figure 14

# importing the required modules
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
import math
import csv

plt.style.use('seaborn-whitegrid')
# seaborn-whitegrid
# seaborn-deep
# seaborn-dark-palette
# seaborn-colorblind
# fivethirtyeight
# ggplot
# seaborn
# seaborn-pastel
# seaborn-white
# tableau-colorblind10
# Solarize_Light2

# User set
tmin = 0.0
tmax = 16.0
ymin = -15.0
ymax = +15.0
cylinder_length = 1.87
# Rotation point
Ox = 6.402
Oz = 4.694
# Piston point
Px = 7.143
Pz = 4.188

# Font sizes
SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 14
SPH_LINE = 1.5

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# Read files data
dataEXP_NUM = np.genfromtxt("floating_motion_EXP_NUM.tsv")
tEN = dataEXP_NUM[:,0]
xEXP = dataEXP_NUM[:,1]
xNUM = dataEXP_NUM[:,2]

# remove nan
tEN = tEN[np.logical_not(np.isnan(tEN))]
xEXP = xEXP[np.logical_not(np.isnan(xEXP))]
xNUM = xNUM[np.logical_not(np.isnan(xNUM))]

# csv file name
filenameSPH = "AbsorberMotion_mk10.csv"
tSPH = []
xSPH = []
zSPH = []

with open(filenameSPH) as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        tSPH.append(row['time [s]'])
        xSPH.append(row['center.x [m]'])
        zSPH.append(row['center.z [m]'])

# Convert list to array
tSPHa = np.array(tSPH)
xSPHa = np.array(xSPH)
zSPHa = np.array(zSPH)
# Convert to float
tSPH = tSPHa.astype(np.float64)
xSPH = xSPHa.astype(np.float64)
zSPH = zSPHa.astype(np.float64)

# Windt et al., 2020 Validation of a CFD-based numerical wave tank model for the power
# production assessment of the wavestar ocean wave energy converter
# Eqs. 6, 7, 8
thetaExt = np.arctan(1.597 / 1.250)
thetaInt = np.arctan((xSPH[0] - Ox) / (Oz - zSPH[0]))
theta = thetaExt - thetaInt
beta = np.arctan((Oz - zSPH) / (xSPH - Ox))
gamma = beta - theta
alpha = 1.24 + gamma
Xc = -np.sqrt(-np.cos(alpha) * 2.0 * 0.8973 * 1.38 + 0.8973 * 0.8973 + 1.38 * 1.38)
xSPH = Xc - Xc[0]

# Meters -> Centimeters
xSPH = xSPH*100
zSPH = zSPH*100

#print(tEN)
#print(xEXP)
#print(xNUM)

# Smooth data
# 300 represents number of points to make between T.min and T.max
tENsmooth = np.linspace(tEN.min(), tEN.max(), 300)
splE = make_interp_spline(tEN, xEXP, k=3)  # type: BSpline
xEXPsmooth = splE(tENsmooth)
splN = make_interp_spline(tEN, xNUM, k=3)  # type: BSpline
xNUMsmooth = splN(tENsmooth)
tSPHsmooth = np.linspace(tSPH.min(), tSPH.max(), 300)
spl = make_interp_spline(tSPH, xSPH, k=3)  # type: BSpline
xSPHsmooth = spl(tSPHsmooth)

# Plotting the Xc displacement
plt.plot(tENsmooth, xEXPsmooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
plt.plot(tENsmooth, xNUMsmooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
plt.plot(tSPHsmooth, xSPHsmooth, color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH-DVI')
plt.xlim([tmin, tmax])
plt.ylim([ymin, ymax])
plt.xlabel('Time (s)')
plt.ylabel('Displacement Xc (cm)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('xc-disp-T02p80-A00p25-lo03p125e-3.png')
plt.show()