"""
Brief example that computes a sea state contour from the PNBOIA data (https://www.marinha.mil.br/chm/dados-do-goos-brasil/pnboia-mapa).
Library virocon
https://github.com/virocon-organization/virocon

A contour implements a method to define multivariate extremes based on a joint probabilistic model of variables 
like significant wave height, wind speed or spectral peak period. Contour curves or surfaces for more than two 
environmental parameters give combination of environmental parameters which approximately describe the various 
actions corresponding to the given exceedance probability. See: 
https://virocon.readthedocs.io/en/latest/definitions.html

"""
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
import datetime
import numpy as np
from virocon import (
	read_ec_benchmark_dataset,
	get_OMAE2020_Hs_Tz,
	GlobalHierarchicalModel,
	IFORMContour,
	IFORMContour,
	ISORMContour,
	DirectSamplingContour,
	HighestDensityContour,
	plot_2D_contour,
)

### USER INPUT ###
# Folder with TXT buoy files
input_folder_name = 'datasets'
# Return period in years. Describes the average time period between two consecutive environmental states 
# that exceed a contour. In the univariate case the contour is a threshold.
tr = 50
# Sea state duration in hours. Time period for which an env
ts = 1
# Number of sea states for simulation
nSamples = 5
### USER INPUT ###

buoy_region = int(input('Enter region number (Santos = 1, Cabo Frio = 2 or Itajai = 3): '))

# Input TXT file name (buoy from https://www.marinha.mil.br/chm/dados-do-goos-brasil/pnboia-mapa)
if buoy_region == 1:
	inpute_file_name = 'historico_santos' 	# Buoy File name in folder datasets - Buoy SANTOS		25°26'37''S 45°02'17''W
elif buoy_region == 2:
	inpute_file_name = 'historico_cabofrio2_0' 	# Buoy File name in folder datasets - Buoy CABO FRIO 2 	23°37'79''S 42°12'17''W
elif buoy_region == 3:
	inpute_file_name = 'historico_itajai_0' 	# Buoy File name in folder datasets - Buoy ITAJAI 		27°24'35''S 47°15'93''W

input_file_txt = input_folder_name + '/' + inpute_file_name + '.txt'
# Output CSV file name formatted to be used with virocon functions
output_file_csv = input_folder_name + '/' + inpute_file_name + '_comma.csv'
# Output TXT file name formatted to be used with virocon functions
output_file_txt = input_folder_name + '/' + inpute_file_name + '_comma.txt'

df = pd.read_csv(input_file_txt, sep=',', usecols=['# Datetime', 'Wvht', 'Dpd'])

# Delete negative values
df = df.drop(df.index[df['Wvht'] < 0])
df = df.drop(df.index[df['Dpd'] < 0])

# Convert datetime format
dfAux = []
for index, row in df.iterrows():
	timeSTP = pd.Timestamp(row['# Datetime'])
	dfAux.append(timeSTP.strftime('%Y-%m-%d-%H'))

# Creating DataFrame
d2 = {'# Datetime':dfAux}
df2 = pd.DataFrame(d2)
# Assigning column of df2 to a new column of df
df['# Datetime'] = df2['# Datetime']
# Display modified DataFrame
# print("Modified DataFrame:\n",df)

row_count = df.shape[0]		# Returns number of rows
col_count = df.shape[1]		# Returns number of columns
print('Number of valid data', row_count)

# Save temp file
df.to_csv(input_folder_name + '/temp.txt',index=False)

# Rename Header Columns in CSV File
with open(input_folder_name + '/temp.txt', 'r', encoding='utf-8') as file:
	data = file.readlines()
data[0] = 'time (YYYY-MM-DD-HH),significant wave height (m),zero-up-crossing period (s)\n'
with open(input_folder_name + '/temp.txt', 'w', encoding='utf-8') as file:
	file.writelines(data)

# Check if ouputfile already exists, then delete it:
if os.path.exists(output_file_csv):
	os.remove(output_file_csv)

# Renaming the file
os.rename(input_folder_name + '/temp.txt', output_file_csv)

# IMPORTANT !!!
# Only CSV file with coma "," separations. Problems with filter dropna using semicolons ";"
# Load sea state measurements.
df = pd.read_csv(output_file_csv, index_col=0)
# df.replace('.', ',')
# Replace semicollon to comma
# df.apply(lambda x: x.str.replace(';',','))
# df.stack().str.replace(';',',').unstack()
# Remove Rows with empty cells
new_df = df.dropna()
# print(new_df)
# Rename multiple column headers
# create a dictionary
# key = old name
# value = new name
# dict = {'YEAR-MONTH-DAY-HOUR': 'time (YYYY-MM-DD-HH)',
# 		'Hsig': 'significant wave height (m)',
# 		'TP': 'zero-up-crossing period (s)'}
# # call rename () method
# new_df.rename(columns=dict, inplace=True)

# Save as txt file without column ID and using semicolons
new_df.to_csv(output_file_txt, sep=';')
# new_df.to_csv(output_file_txt, index=False)

print('Input file successfully changed to be used with package virocon')

# Load the sea state data set
data = read_ec_benchmark_dataset(output_file_txt)

# Define the structure of the joint distribution model.
dist_descriptions, fit_descriptions, semantics = get_OMAE2020_Hs_Tz()
model = GlobalHierarchicalModel(dist_descriptions)

# Estimate the model's parameter values (fitting).
model.fit(data, fit_descriptions=fit_descriptions)

# Compute IFORM and ISORM contours with a return period of tr years.
# tr = 50  # Return period in years. Describes the average time period between two consecutive environmental states that exceed a contour. In the univariate case the contour is a threshold.
# ts = 1  # Sea state duration in hours. Time period for which an environmental state is measured.
alpha = 1.0 / (tr * 365.25 * 24.0 / ts)
# inverse first-order reliability method (IFORM)
iform_contour = IFORMContour(model, alpha)
# inverse second-order reliability method (ISORM). More conservative
isorm_contour = ISORMContour(model, alpha)

waveHeight_IF = iform_contour.coordinates[:,0]
wavePeriod_IF = iform_contour.coordinates[:,1]
waveHeight_IS = isorm_contour.coordinates[:,0]
wavePeriod_IS = isorm_contour.coordinates[:,1]

# Number of points
nPts_IF = waveHeight_IF.size
nPts_IS = waveHeight_IS.size
# Interval of 5 points
intPts_IF = int(nPts_IF/nSamples)
intPts_IS = int(nPts_IS/nSamples)
# Maximum wave height (n-year significant wave height, Hs,n), index and respective period
maxH_IF = np.amax(waveHeight_IF)
maxHid_IF = np.argmax(waveHeight_IF)
maxHperiod_IF = wavePeriod_IF[maxHid_IF]
maxH_IS = np.amax(waveHeight_IS)
maxHid_IS = np.argmax(waveHeight_IS)
maxHperiod_IS = wavePeriod_IS[maxHid_IS]

# a_ = np.sqrt(6.50) # 2.55
# b_ = np.sqrt(11.0) # 3.32
# Peak spectral period
# Valamanesh et al., 2015. Multivariate analysis of extreme metocean conditions for offshore wind turbines
a_ = 11.7 / np.sqrt(9.81) # 3.74
b_ = 17.2 / np.sqrt(9.81) # 5.49
# # IEC 2009. Wind Turbines Part 3: Design requirements for offshore wind turbines
# a_ = 11.1 / np.sqrt(9.81) # 3.54
# b_ = 14.3 / np.sqrt(9.81) # 4.57
T1_IF = a_ * np.sqrt(maxH_IF)
T2_IF = b_ * np.sqrt(maxH_IF)
T1_IS = a_ * np.sqrt(maxH_IS)
T2_IS = b_ * np.sqrt(maxH_IS)

# Minimum wave period, index
minT_IF = np.amin(wavePeriod_IF)
minTid_IF = np.argmin(wavePeriod_IF)
minT_IS = np.amin(wavePeriod_IS)
minTid_IS = np.argmin(wavePeriod_IS)
# Maximum wave period, index and respective height
maxT_IF = np.amax(wavePeriod_IF)
maxTid_IF = np.argmax(wavePeriod_IF)
maxTheight_IF = waveHeight_IF[maxHid_IF]
maxT_IS = np.amax(wavePeriod_IS)
maxTid_IS = np.argmax(wavePeriod_IS)
maxTheight_IS = waveHeight_IS[maxHid_IS]

# Period interval
periodInt_IF = (maxT_IF - minT_IF)/nSamples
# periodInt_IF = (maxT_IF - maxHperiod_IF)/2.0
periodInt_IS = (maxT_IS - minT_IS)/nSamples
# periodInt_IS = (maxT_IS - maxHperiod_IS)/2.0

# IFORM
ids_IF = []
# Return index
# Search right points
for ii in range(1, nSamples):
	if ii > nSamples/2:
		break
	idAux1 = np.where(np.logical_and(wavePeriod_IF > maxHperiod_IF + (ii - 0.05)*periodInt_IF, wavePeriod_IF < maxHperiod_IF + (ii + 0.05)*periodInt_IF))
	# idAux1 = np.where(np.logical_and(wavePeriod_IF > 0.95*T1_IF, wavePeriod_IF < 1.05*T1_IF))
	# Find max Height for the period
	maxHaux = 0
	for jj in idAux1[0]:
		if waveHeight_IF[jj] > maxHaux:
			maxHaux = waveHeight_IF[jj]
			idMaxH = jj
	ids_IF.append(idMaxH)

del ii

# Search left point
for ii in range(1, nSamples):
	if ii > nSamples/2:
		break
	idAux2 = np.where(np.logical_and(wavePeriod_IF > maxHperiod_IF - (ii + 0.05)*periodInt_IF, wavePeriod_IF < maxHperiod_IF - (ii - 0.05)*periodInt_IF))
	# idAux2 = np.where(np.logical_and(wavePeriod_IF > 0.95*T2_IF, wavePeriod_IF < 1.05*T2_IF))
	# Find max Height for the period
	maxHaux = 0
	for jj in idAux2[0]:
		if waveHeight_IF[jj] > maxHaux:
			maxHaux = waveHeight_IF[jj]
			idMaxH = jj
	ids_IF.append(idMaxH)

wavePts_IF = []
wavePts_IF.append(waveHeight_IF[0])
for xx in ids_IF:
	wavePts_IF.append(waveHeight_IF[xx])
# wavePts_IF.append(waveHeight_IF[maxTid_IF])
periodPts_IF = []
periodPts_IF.append(wavePeriod_IF[0])
del xx
for xx in ids_IF:
	periodPts_IF.append(wavePeriod_IF[xx])
# periodPts_IF.append(wavePeriod_IF[maxTid_IF])

periodOutput_IF = ['{:.2f}'.format(elem) for elem in periodPts_IF]
waveOutput_IF = ['{:.2f}'.format(elem) for elem in wavePts_IF]

# ISORM
ids_IS = []
# Return index
# Search right points
for ii in range(1, nSamples):
	if ii > nSamples/2:
		break
	idAux1 = np.where(np.logical_and(wavePeriod_IS > maxHperiod_IS + (ii - 0.05)*periodInt_IS, wavePeriod_IS < maxHperiod_IS + (ii + 0.05)*periodInt_IS))
	# idAux1 = np.where(np.logical_and(wavePeriod_IS > 0.95*T1_IS, wavePeriod_IS < 1.05*T1_IS))
	# Find max Height for the period
	maxHaux = 0
	for jj in idAux1[0]:
		if waveHeight_IS[jj] > maxHaux:
			maxHaux = waveHeight_IS[jj]
			idMaxH = jj
	ids_IS.append(idMaxH)

del ii

# Search left point
for ii in range(1, nSamples):
	if ii > nSamples/2:
		break
	idAux2 = np.where(np.logical_and(wavePeriod_IS > maxHperiod_IS - (ii + 0.05)*periodInt_IS, wavePeriod_IS < maxHperiod_IS - (ii - 0.05)*periodInt_IS))
	# idAux2 = np.where(np.logical_and(wavePeriod_IS > 0.95*T2_IS, wavePeriod_IS < 1.05*T2_IS))
	# Find max Height for the period
	maxHaux = 0
	for jj in idAux2[0]:
		if waveHeight_IS[jj] > maxHaux:
			maxHaux = waveHeight_IS[jj]
			idMaxH = jj
	ids_IS.append(idMaxH)

wavePts_IS = []
wavePts_IS.append(waveHeight_IS[0])
for xx in ids_IS:
	wavePts_IS.append(waveHeight_IS[xx])
# wavePts_IS.append(waveHeight_IS[maxTid_IS])
periodPts_IS = []
periodPts_IS.append(wavePeriod_IS[0])
del xx
for xx in ids_IS:
	periodPts_IS.append(wavePeriod_IS[xx])
# periodPts_IS.append(wavePeriod_IS[maxTid_IS])

periodOutput_IS = ['{:.2f}'.format(elem) for elem in periodPts_IS]
waveOutput_IS = ['{:.2f}'.format(elem) for elem in wavePts_IS]

print('IFORM T1: ' + '{:.3f}s'.format(T1_IF))
print('IFORM T2: ' + '{:.3f}s'.format(T2_IF))
# print('IFORM Interval period: ' + '{:.3f}s'.format(periodInt_IF))
print('IFORM Maximum wave height: ' + '{:.3f}m'.format(maxH_IF))
print('IFORM Period of the maximum wave height: ' + '{:.3f}s'.format(maxHperiod_IF))
# print('IFORM Wave Periods[s]: ', periodOutput_IF)
# print('IFORM Wave heights[m]: ', waveOutput_IF)
print('ISORM T1' + ' = {:.3f}s'.format(T1_IS))
print('ISORM T2' + ' = {:.3f}s'.format(T2_IS))
# print('ISORM Interval period: ' + '{:.3f}s'.format(periodInt_IS))
print('ISORM Maximum wave height: ' + '{:.3f}m'.format(maxH_IS))
print('ISORM Period of the maximum wave height: ' + '{:.3f}s'.format(maxHperiod_IS))
# print('ISORM Wave Periods[s]: ', periodOutput_IS)
# print('ISORM Wave heights[m]: ', waveOutput_IS)

plots_n = []
# Plot the contour
fig, axs = plt.subplots(1, 2, figsize=[10, 8], sharex=True, sharey=True)
# fig, axs = plt.subplots(1, 2, figsize=[10, 8], sharex=True, sharey=True, gridspec_kw={'width_ratios': [1000, 1]})
plot_2D_contour(iform_contour, data, semantics=semantics, ax=axs[0], swap_axis=True)
plot_2D_contour(isorm_contour, data, semantics=semantics, ax=axs[1], swap_axis=True)

# Plot the periods limits
# only one line may be specified; ymin & ymax specified as a percentage of y-range
axs[0].axvline(x=T1_IF, ymin=0.00, ymax=0.95, color='purple', ls='--', lw=1)
axs[0].text(T1_IF-3.0, maxH_IF + 1.0, r'T$_{1}$' + ' = {:.2f}s'.format(T1_IF), backgroundcolor='w', color='purple')
axs[0].axvline(x=T2_IF, ymin=0.00, ymax=0.95, color='purple', ls='--', lw=1)
axs[0].text(T2_IF+1.0, maxH_IF + 1.0, r'T$_{2}$' + ' = {:.2f}s'.format(T2_IF), backgroundcolor='w', color='purple')
axs[1].axvline(x=T1_IS, ymin=0.00, ymax=0.95, color='purple', ls='--', lw=1)
axs[1].text(T1_IS-3.0, maxH_IS - 1.0, r'T$_{1}$' + ' = {:.2f}s'.format(T1_IS), backgroundcolor='w', color='purple')
axs[1].axvline(x=T2_IS, ymin=0.00, ymax=0.95, color='purple', ls='--', lw=1)
axs[1].text(T2_IS+1.0, maxH_IS - 1.0, r'T$_{2}$' + ' = {:.2f}s'.format(T2_IS), backgroundcolor='w', color='purple')

# Plot the maximum wave height
axs[0].scatter(maxHperiod_IF, maxH_IF, color='dodgerblue') # royalblue
axs[0].text(maxHperiod_IF-1.0, maxH_IF+0.25, 'T = {:.2f}s, H = {:.2f}m'.format(maxHperiod_IF, maxH_IF), backgroundcolor='w', color='dodgerblue') # royalblue
axs[1].scatter(maxHperiod_IS, maxH_IS, color='dodgerblue') # royalblue
axs[1].text(maxHperiod_IS-1.0, maxH_IS+0.25, 'T = {:.2f}s, H = {:.2f}m'.format(maxHperiod_IS, maxH_IS), backgroundcolor='w', color='dodgerblue') # royalblue


# # Plot the sample points
# axs[0].scatter(periodPts_IF, wavePts_IF, color='dodgerblue') # royalblue
# for ii, jj in zip(periodPts_IF, wavePts_IF):
# 	axs[0].text(ii-1.0, jj+0.25, '({:.2f}, {:.2f})'.format(ii, jj), backgroundcolor='w', color='dodgerblue') # royalblue
# # Plot the sample points
# axs[1].scatter(periodPts_IS, wavePts_IS, color='dodgerblue') # royalblue
# for ii, jj in zip(periodPts_IS, wavePts_IS):
# 	axs[1].text(ii-1.0, jj+0.25, '({:.2f}, {:.2f})'.format(ii, jj), backgroundcolor='w', color='dodgerblue') # royalblue


# plot_2D_contour(iform_contour, data, semantics=semantics, ax=None, swap_axis=True)
# plot_2D_contour(isorm_contour, data, semantics=semantics, ax=None, swap_axis=True)
titles = ['IFORM ' + str(tr) + ' years', 'ISORM ' + str(tr) + ' years']
for i, (ax, title) in enumerate(zip(axs, titles)):
	ax.set_title(title)
plt.tight_layout()

# fig.delaxes(axs[1]) # Hide subplot

fig = plt.gcf() # get current figure

# Make directory
fig_directory_name = 'figs'
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, fig_directory_name)
if not os.path.exists(final_directory):
	os.makedirs(final_directory)

# Save Figure
fig_name = inpute_file_name + '_tr' + str(tr) + 'years_envirom_countor'
fig.savefig(fig_directory_name + '/' + fig_name + '.png')
plt.show()
plt.close(fig)    # close the figure window

print('Figure saved in folder \'{}\''.format(fig_directory_name))



# # Compute four types of contours with a return period of 50 years.
# iform = IFORMContour(model, alpha)
# print('IFORMContour Done')
# isorm = ISORMContour(model, alpha)
# print('ISORMContour Done')
# direct_sampling = DirectSamplingContour(model, alpha)
# print('DirectSamplingContour Done')
# highest_density = HighestDensityContour(model, alpha) # Problems: from_scipy_sparse_matrix removed in NetworkX 3.0  
# print('HighestDensityContour Done')

# # Plot the contours on top of the metocean data.
# fig, axs = plt.subplots(4, 1, figsize=[4, 12], sharex=True, sharey=True)
# plot_2D_contour(iform, sample=data, semantics=semantics, ax=axs[0])
# plot_2D_contour(isorm, sample=data, semantics=semantics, ax=axs[1])
# plot_2D_contour(direct_sampling, sample=data, semantics=semantics, ax=axs[2])
# plot_2D_contour(highest_density, sample=data, semantics=semantics, ax=axs[3])
# titles = ['IFORM', 'ISORM', 'Direct sampling', 'Highest density']
# for i, (ax, title) in enumerate(zip(axs, titles)):
# 	ax.set_title(title)
# 	if i < 3:
# 		ax.set_xlabel('')

# plt.tight_layout()
# plt.show()