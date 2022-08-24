# Plot DeepCwind displacements (Surge, Heave, Pitch)
# A. J. Couling, 2013. Validation of a FAST semi-submersible floating wind turbine numerical model with DeepCwind test data

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
tmax = 50.0
smin = -0.10
smax = +0.30
hmin = -0.02
hmax = +0.10
pmin = -5.0
pmax = +1.0
tShift = 0.0

# Font sizes
SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 14
w2nd_LINE = 1.5
wSPH_LINE = 1.0

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def readCSV3a(fileName, listTime, listSurge, listHeave, listPitch, typeFile):
    """
    This function read CSV file 
    and fill the list
    """
    with open(fileName, 'r+') as f:
        # Skip first N rows
        if typeFile == 'SPH':
            Nrows = 0
        else:
            Nrows = 18
        for i in range(Nrows):
            f.readline()
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if typeFile == 'SPH':
                listTime.append(row['time [s]'])
                listSurge.append(row['surge [m]'])
                listHeave.append(row['heave [m]'])
                listPitch.append(row['pitch [deg]'])
            else:
                listTime.append(row['Time [s]'])
                listSurge.append(row['surge [m]'])
                listHeave.append(row['heave [m]'])
                listPitch.append(row['pitch [deg]'])
    return listTime, listSurge, listHeave, listPitch

# Read files data
# csv 2nd order Surge file name
# filename2nd00 = "SurgePaddle_mkb0010_0000.csv"
# filename2nd01 = "SurgePaddle_mkb0010_0001.csv"
# filename2nd02 = "SurgePaddle_mkb0010_0002.csv"
# filename2nd03 = "SurgePaddle_mkb0010_0003.csv"
# t2nd = []
# w2nd_00 = []
# w2nd_01 = []
# w2nd_02 = []
# w2nd_03 = []

# readCSV3a(filename2nd00, t2nd, w2nd_00, '2nd')
# readCSV2a(filename2nd01, w2nd_01, '2nd')
# readCSV2a(filename2nd02, w2nd_02, '2nd')
# readCSV2a(filename2nd03, w2nd_03, '2nd')

# # Convert list to array
# t2nda = np.array(t2nd)
# w2nd_00a = np.array(w2nd_00)
# w2nd_01a = np.array(w2nd_01)
# w2nd_02a = np.array(w2nd_02)
# w2nd_03a = np.array(w2nd_03)

# # Convert to float
# t2nd  = t2nda.astype( np.float64)
# w2nd_00 = w2nd_00a.astype(np.float64)
# w2nd_01 = w2nd_01a.astype(np.float64)
# w2nd_02 = w2nd_02a.astype(np.float64)
# w2nd_03 = w2nd_03a.astype(np.float64)

# csv SPH file name
filenameSPH00 = "floatinginfo/FloatingMotion_mk60.csv"
tSPH = []
sSPH = []
hSPH = []
pSPH = []

readCSV3a(filenameSPH00, tSPH, sSPH, hSPH, pSPH, 'SPH')

# Convert list to array
tSPHa = np.array(tSPH)
sSPHa = np.array(sSPH)
hSPHa = np.array(hSPH)
pSPHa = np.array(pSPH)

# Convert to float
tSPH  = tSPHa.astype( np.float64)
sSPH = sSPHa.astype(np.float64)
hSPH = hSPHa.astype(np.float64)
pSPH = pSPHa.astype(np.float64)

#print(tEN_2)
#print(EXP_2)
#print(NUM_2)


# Plotting Surge
#plt.plot(t2nd, w2nd_00, color='C4', linestyle='--', marker='', linewidth=w2nd_LINE, label='2nd order Stokes Theory')
plt.plot(tSPH - tShift, (sSPH - sSPH[0]), color='C1', linestyle='-', marker='', linewidth=wSPH_LINE, label='SPH-DVI')
plt.xlim([tmin, tmax])
plt.ylim([smin, smax])
plt.xlabel('Time (s)')
plt.ylabel('Surge (m)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('surge-floating-T12p10-A10p30-lo01p500e-2.png')
plt.show()

# Plotting Heave
#plt.plot(t2nd, w2nd_01, color='C4', linestyle='--', marker='', linewidth=w2nd_LINE, label='2nd order Stokes Theory')
plt.plot(tSPH - tShift, (hSPH - hSPH[0]), color='C1', linestyle='-', marker='', linewidth=wSPH_LINE, label='SPH-DVI')
plt.xlim([tmin, tmax])
plt.ylim([hmin, hmax])
plt.xlabel('Time (s)')
plt.ylabel('Heave (m)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('heave-floating-T12p10-A10p30-lo01p500e-2.png')
plt.show()

# Plotting Pitch
#plt.plot(t2nd, w2nd_02, color='C4', linestyle='--', marker='', linewidth=w2nd_LINE, label='2nd order Stokes Theory')
plt.plot(tSPH - tShift, (pSPH - pSPH[0]), color='C1', linestyle='-', marker='', linewidth=wSPH_LINE, label='SPH-DVI')
plt.xlim([tmin, tmax])
plt.ylim([pmin, pmax])
plt.xlabel('Time (s)')
plt.ylabel('Pitch (deg)')
legend = plt.legend(loc=4, shadow=True, prop={'size': SMALL_SIZE})
legend.get_frame().set_facecolor('C0') # Put a nicer background color on the legend
fig = plt.gcf() # get current figure
fig.savefig('pitch-floating-T12p10-A10p30-lo01p500e-2.png')
plt.show()


# # Write txt file
# data = np.column_stack([tSPHsmooth, sSPHsmooth - sSPHsmooth[0], wSPH_01smooth - wSPH_01smooth[0], wSPH_02smooth - wSPH_02smooth[0], wSPH_03smooth - wSPH_03smooth[0], wSPH_04smooth - wSPH_04smooth[0]])
# datafile_path = "./Surge_sph.txt"
# np.savetxt(datafile_path, data, fmt=['%1.4e','%1.4e','%1.4e','%1.4e','%1.4e','%1.4e'], delimiter=',', header='Time (s), W0 (m), W1 (m), W2 (m), W3 (m), W4 (m)')