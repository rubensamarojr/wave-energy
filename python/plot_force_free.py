# Plot wavestar cylinder force
# E. J. Ransley, 2017. RANS-VOF modelling of the Wavestar point absorber
# Figure 14

# importing the required modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
xmin = -400.0
xmax = +400.0
zmin = 0.0
zmax = 3000.0
cylinder_length = 1.87
# Force shift
fxS = 0.0
fzS = 400


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
dataEXP_NUMx = np.genfromtxt("force_X.tsv")
tENx = dataEXP_NUMx[:,0]
xEXP = dataEXP_NUMx[:,1]
xNUM = dataEXP_NUMx[:,2]
dataEXP_NUMz = np.genfromtxt("force_Z.tsv")
tENz = dataEXP_NUMz[:,0]
zEXP = dataEXP_NUMz[:,1]
zNUM = dataEXP_NUMz[:,2]

# remove nan
tENx = tENx[np.logical_not(np.isnan(tENx))]
xEXP = xEXP[np.logical_not(np.isnan(xEXP))]
xNUM = xNUM[np.logical_not(np.isnan(xNUM))]
tENz = tENz[np.logical_not(np.isnan(tENz))]
zEXP = zEXP[np.logical_not(np.isnan(zEXP))]
zNUM = zNUM[np.logical_not(np.isnan(zNUM))]

# csv file name
filenameSPH = "_AbsorberForce.csv"
tSPH = []
xSPHF = []
zSPHF = []
xSPHT = []
zSPHT = []
mSPH = []

with open(filenameSPH) as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        tSPH.append(row['Time [s]'])
        xSPHF.append(row['ForceFluid.x [N]'])
        zSPHF.append(row['ForceFluid.z [N]'])
        xSPHT.append(row['ForceTotal.x [N]'])
        zSPHT.append(row['ForceTotal.z [N]'])
        mSPH.append(row['Moment [Nm]'])

# Convert list to array
tSPHa = np.array(tSPH)
xSPHFa = np.array(xSPHF)
zSPHFa = np.array(zSPHF)
xSPHTa = np.array(xSPHT)
zSPHTa = np.array(zSPHT)
mSPHa = np.array(mSPH)
# Convert to float
tSPH  = tSPHa.astype( np.float64)
xSPHF = xSPHFa.astype(np.float64)
zSPHF = zSPHFa.astype(np.float64)
xSPHT = xSPHTa.astype(np.float64)
zSPHT = zSPHTa.astype(np.float64)
mSPH  = mSPHa.astype( np.float64)

# Smooth data
# Np represents number of points to make between T.min and T.max
Np = 300
tENxsmooth = np.linspace(tENx.min(), tENx.max(), Np)
splE = make_interp_spline(tENx, xEXP, k=3)  # type: BSpline
xEXPsmooth = splE(tENxsmooth)
splN = make_interp_spline(tENx, xNUM, k=3)  # type: BSpline
xNUMsmooth = splN(tENxsmooth)
tENzsmooth = np.linspace(tENz.min(), tENz.max(), Np)
splE = make_interp_spline(tENz, zEXP, k=3)  # type: BSpline
zEXPsmooth = splE(tENzsmooth)
splN = make_interp_spline(tENz, zNUM, k=3)  # type: BSpline
zNUMsmooth = splN(tENzsmooth)

tSPHsmooth = np.linspace(tSPH.min(), tSPH.max(), Np)
spl = make_interp_spline(tSPH, xSPHF, k=3)  # type: BSpline
xSPHFsmooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, zSPHF, k=3)  # type: BSpline
zSPHFsmooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, xSPHT, k=3)  # type: BSpline
xSPHTsmooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, zSPHT, k=3)  # type: BSpline
zSPHTsmooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, mSPH, k=3)  # type: BSpline
mSPHsmooth = spl(tSPHsmooth)

# Plotting Force Fx
plt.plot(tENxsmooth, xEXPsmooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
plt.plot(tENxsmooth, xNUMsmooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
plt.plot(tSPHsmooth, xSPHFsmooth-fxS, color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH-DVI')
#plt.plot(tSPHsmooth, xSPHTsmooth, color='C3', linestyle=':', marker='', linewidth=SPH_LINE, label='SPH-DVI-T')
plt.xlim([tmin, tmax])
plt.ylim([xmin, xmax])
plt.xlabel('Time (s)')
plt.ylabel('Horizontal Force Fx (N)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('x-force-T02p80-A00p25-lo03p125e-3.png')
plt.show()

# Plotting Force Fz
plt.plot(tENzsmooth, zEXPsmooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
#plt.plot(tENzsmooth, zNUMsmooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
plt.plot(tENz, zNUM, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
plt.plot(tSPHsmooth, zSPHFsmooth-fzS, color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH-DVI')
#plt.plot(tSPHsmooth, zSPHTsmooth, color='C3', linestyle=':', marker='', linewidth=SPH_LINE, label='SPH-DVI-T')
plt.xlim([tmin, tmax])
plt.ylim([zmin, zmax])
plt.xlabel('Time (s)')
plt.ylabel('Vertical Force Fz (N)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('z-force-T02p80-A00p25-lo03p125e-3.png')
plt.show()

# Plotting Moment
#plt.plot(tENxsmooth, xEXPsmooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
#plt.plot(tENxsmooth, xNUMsmooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tSPHsmooth, mSPHsmooth, color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH-DVI')
#plt.xlim([tmin, tmax])
#plt.ylim([xmin, xmax])
#plt.xlabel('Time (s)')
#plt.ylabel('Moment M (Nm)')
#legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
#legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
#fig = plt.gcf() # get current figure
#fig.savefig('y-moment-T02p80-A00p25-lo03p125e-3.png')
#plt.show()

# Write txt file
data = np.column_stack([tSPHsmooth, xSPHFsmooth-fxS, zSPHFsmooth-fzS])
datafile_path = "./force_sph.txt"
np.savetxt(datafile_path, data, fmt=['%1.4e','%1.4e', '%1.4e'], delimiter=',', header='Time (s), Fx (N), Fz (N)')