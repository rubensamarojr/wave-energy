# Plot wavestar wave motion
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
zmin = -0.2
zmax = +0.2
cylinder_length = 1.87

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
dataEXP_NUM_2 = np.genfromtxt("surface_2.tsv")
dataEXP_NUM_11 = np.genfromtxt("surface_11.tsv")
dataEXP_NUM_13 = np.genfromtxt("surface_13.tsv")
dataEXP_NUM_14 = np.genfromtxt("surface_14.tsv")
dataEXP_NUM_16 = np.genfromtxt("surface_16.tsv")
tEN_2 = dataEXP_NUM_2[:,0]
EXP_2 = dataEXP_NUM_2[:,1]
NUM_2 = dataEXP_NUM_2[:,2]
tEN_11 = dataEXP_NUM_11[:,0]
EXP_11 = dataEXP_NUM_11[:,1]
NUM_11 = dataEXP_NUM_11[:,2]
tEN_13 = dataEXP_NUM_13[:,0]
EXP_13 = dataEXP_NUM_13[:,1]
NUM_13 = dataEXP_NUM_13[:,2]
tEN_14 = dataEXP_NUM_14[:,0]
EXP_14 = dataEXP_NUM_14[:,1]
NUM_14 = dataEXP_NUM_14[:,2]
tEN_16 = dataEXP_NUM_16[:,0]
EXP_16 = dataEXP_NUM_16[:,1]
NUM_16 = dataEXP_NUM_16[:,2]

# remove nan
tEN_2 = tEN_2[np.logical_not(np.isnan(tEN_2))]
EXP_2 = EXP_2[np.logical_not(np.isnan(EXP_2))]
NUM_2 = NUM_2[np.logical_not(np.isnan(NUM_2))]
tEN_11 = tEN_11[np.logical_not(np.isnan(tEN_11))]
EXP_11 = EXP_11[np.logical_not(np.isnan(EXP_11))]
NUM_11 = NUM_11[np.logical_not(np.isnan(NUM_11))]
tEN_13 = tEN_13[np.logical_not(np.isnan(tEN_13))]
EXP_13 = EXP_13[np.logical_not(np.isnan(EXP_13))]
NUM_13 = NUM_13[np.logical_not(np.isnan(NUM_13))]
tEN_14 = tEN_14[np.logical_not(np.isnan(tEN_14))]
EXP_14 = EXP_14[np.logical_not(np.isnan(EXP_14))]
NUM_14 = NUM_14[np.logical_not(np.isnan(NUM_14))]
tEN_16 = tEN_16[np.logical_not(np.isnan(tEN_16))]
EXP_16 = EXP_16[np.logical_not(np.isnan(EXP_16))]
NUM_16 = NUM_16[np.logical_not(np.isnan(NUM_16))]

# csv file name
filenameSPH = "_elevation_Elevation.csv"
tSPH = []
SPH_0 = []
SPH_1 = []
SPH_2 = []
SPH_3 = []
SPH_4 = []

with open(filenameSPH, 'r+') as f:
    # Skip first 3 rows
    for i in range(3):
        f.readline()
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        tSPH.append(row['Time [s]'])
        SPH_0.append(row['Elevation_0 [m]'])
        SPH_1.append(row['Elevation_1 [m]'])
        SPH_2.append(row['Elevation_2 [m]'])
        SPH_3.append(row['Elevation_3 [m]'])
        SPH_4.append(row['Elevation_4 [m]'])

# Convert list to array
tSPHa = np.array(tSPH)
SPH_0a = np.array(SPH_0)
SPH_1a = np.array(SPH_1)
SPH_2a = np.array(SPH_2)
SPH_3a = np.array(SPH_3)
SPH_4a = np.array(SPH_4)
# Convert to float
tSPH  = tSPHa.astype( np.float64)
SPH_0 = SPH_0a.astype(np.float64)
SPH_1 = SPH_1a.astype(np.float64)
SPH_2 = SPH_2a.astype(np.float64)
SPH_3 = SPH_3a.astype(np.float64)
SPH_4 = SPH_4a.astype( np.float64)

#print(tEN_2)
#print(EXP_2)
#print(NUM_2)


# Smooth data
# Np represents number of points to make between T.min and T.max
Np = 300
tEN_2smooth = np.linspace(tEN_2.min(), tEN_2.max(), Np)
splE = make_interp_spline(tEN_2, EXP_2, k=3)  # type: BSpline
EXP_2smooth = splE(tEN_2smooth)
splN = make_interp_spline(tEN_2, NUM_2, k=3)  # type: BSpline
NUM_2smooth = splN(tEN_2smooth)
tEN_11smooth = np.linspace(tEN_11.min(), tEN_11.max(), Np)
splE = make_interp_spline(tEN_11, EXP_11, k=3)  # type: BSpline
EXP_11smooth = splE(tEN_11smooth)
splN = make_interp_spline(tEN_11, NUM_11, k=3)  # type: BSpline
NUM_11smooth = splN(tEN_11smooth)
tEN_13smooth = np.linspace(tEN_13.min(), tEN_13.max(), Np)
splE = make_interp_spline(tEN_13, EXP_13, k=3)  # type: BSpline
EXP_13smooth = splE(tEN_13smooth)
splN = make_interp_spline(tEN_13, NUM_13, k=3)  # type: BSpline
NUM_13smooth = splN(tEN_13smooth)
tEN_14smooth = np.linspace(tEN_14.min(), tEN_14.max(), Np)
splE = make_interp_spline(tEN_14, EXP_14, k=3)  # type: BSpline
EXP_14smooth = splE(tEN_14smooth)
splN = make_interp_spline(tEN_14, NUM_14, k=3)  # type: BSpline
NUM_14smooth = splN(tEN_14smooth)
tEN_16smooth = np.linspace(tEN_16.min(), tEN_16.max(), Np)
splE = make_interp_spline(tEN_16, EXP_16, k=3)  # type: BSpline
EXP_16smooth = splE(tEN_16smooth)
splN = make_interp_spline(tEN_16, NUM_16, k=3)  # type: BSpline
NUM_16smooth = splN(tEN_16smooth)

tSPHsmooth = np.linspace(tSPH.min(), tSPH.max(), Np)
spl = make_interp_spline(tSPH, SPH_0, k=3)  # type: BSpline
SPH_0smooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, SPH_1, k=3)  # type: BSpline
SPH_1smooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, SPH_2, k=3)  # type: BSpline
SPH_2smooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, SPH_3, k=3)  # type: BSpline
SPH_3smooth = spl(tSPHsmooth)
spl = make_interp_spline(tSPH, SPH_4, k=3)  # type: BSpline
SPH_4smooth = spl(tSPHsmooth)

# Plotting Surface 2
plt.plot(tEN_2, EXP_2, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
plt.plot(tEN_2, NUM_2, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tEN_2smooth, EXP_2smooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
#plt.plot(tEN_2smooth, NUM_2smooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tSPH, SPH_0 - SPH_0[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.plot(tSPHsmooth, SPH_0smooth - SPH_0smooth[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.xlim([tmin, tmax])
plt.ylim([zmin, zmax])
plt.xlabel('Time (s)')
plt.ylabel('Surface elevation WP2 (m)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('z2-wave-T02p80-A00p25-lo03p125e-3.png')
plt.show()

# Plotting Surface 11
plt.plot(tEN_11, EXP_11, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
plt.plot(tEN_11, NUM_11, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tEN_11smooth, EXP_11smooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
#plt.plot(tEN_11smooth, NUM_11smooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tSPH, SPH_1 - SPH_1[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.plot(tSPHsmooth, SPH_1smooth - SPH_1smooth[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.xlim([tmin, tmax])
plt.ylim([zmin, zmax])
plt.xlabel('Time (s)')
plt.ylabel('Surface elevation WP11 (m)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('z11-wave-T02p80-A00p25-lo03p125e-3.png')
plt.show()

# Plotting Surface 13
plt.plot(tEN_13, EXP_13, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
plt.plot(tEN_13, NUM_13, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tEN_13smooth, EXP_13smooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
#plt.plot(tEN_13smooth, NUM_13smooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tSPH, SPH_2 - SPH_2[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.plot(tSPHsmooth, SPH_2smooth - SPH_2smooth[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.xlim([tmin, tmax])
plt.ylim([zmin, zmax])
plt.xlabel('Time (s)')
plt.ylabel('Surface elevation WP13 (m)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('z13-wave-T02p80-A00p25-lo03p125e-3.png')
plt.show()

# Plotting Surface 14
plt.plot(tEN_14, EXP_14, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
plt.plot(tEN_14, NUM_14, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tEN_14smooth, EXP_14smooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
#plt.plot(tEN_14smooth, NUM_14smooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tSPH, SPH_3 - SPH_3[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.plot(tSPHsmooth, SPH_3smooth - SPH_3smooth[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.xlim([tmin, tmax])
plt.ylim([zmin, zmax])
plt.xlabel('Time (s)')
plt.ylabel('Surface elevation WP14 (m)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('z14-wave-T02p80-A00p25-lo03p125e-3.png')
plt.show()

# Plotting Surface 16
plt.plot(tEN_16, EXP_16, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
plt.plot(tEN_16, NUM_16, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tEN_16smooth, EXP_16smooth, color='C4', linestyle='--', marker='', label='Experimental Jakobsen et al., 2016')
#plt.plot(tEN_16smooth, NUM_16smooth, color='C2', linestyle=':', marker='', label='RANS-VOF Ransley et al, 2017')
#plt.plot(tSPH, SPH_4 - SPH_4[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.plot(tSPHsmooth, SPH_4smooth - SPH_4smooth[0], color='C1', linestyle='-', marker='', linewidth=SPH_LINE, label='SPH')
plt.xlim([tmin, tmax])
plt.ylim([zmin, zmax])
plt.xlabel('Time (s)')
plt.ylabel('Surface elevation WP16 (m)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('z16-wave-T02p80-A00p25-lo03p125e-3.png')
plt.show()

# Write txt file
data = np.column_stack([tSPHsmooth, SPH_0smooth - SPH_0smooth[0], SPH_1smooth - SPH_1smooth[0], SPH_2smooth - SPH_2smooth[0], SPH_3smooth - SPH_3smooth[0], SPH_4smooth - SPH_4smooth[0]])
datafile_path = "./wave_sph.txt"
np.savetxt(datafile_path, data, fmt=['%1.4e','%1.4e','%1.4e','%1.4e','%1.4e','%1.4e'], delimiter=',', header='Time (s), W0 (m), W1 (m), W2 (m), W3 (m), W4 (m)')