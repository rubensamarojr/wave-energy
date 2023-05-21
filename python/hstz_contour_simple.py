"""
Brief example that computes a sea state contour.
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
# Folder with CSV buoy files
input_folder_name = 'datasets'
# Input CSV file name (buoy from https://simcosta.furg.br)
inpute_file_name = 'SIMCOSTA_RS-5_OCEAN_2016-12-07_2023-02-15' # Buoy File name in folder datasets - Buoy RS-5
# inpute_file_name = 'SIMCOSTA_RS-5_ANT._OCEAN_2016-12-07_2021-11-18' # Buoy RS-5_ANT
# inpute_file_name = 'SIMCOSTA_RJ-3_OCEAN_2016-07-14_2023-02-14' # Buoy RJ-3
# Return period in years. Describes the average time period between two consecutive environmental states 
# that exceed a contour. In the univariate case the contour is a threshold.
tr = 50
# Sea state duration in hours. Time period for which an env
ts = 1
### USER INPUT ###


input_file_csv = input_folder_name + '/' + inpute_file_name + '.csv'
# Output CSV file name formatted to be used with virocon functions
output_file_csv = input_folder_name + '/' + inpute_file_name + '_comma.csv'
# Output TXT file name formatted to be used with virocon functions
output_file_txt = input_folder_name + '/' + inpute_file_name + '_comma.txt'

# File skip first N lines (Verify how many lines need to be skiped until the header)
# Find the data
# read the file into a list of lines
with open(input_file_csv,'r') as f:
	lines = f.read().split('\n')

word_to_find = 'YEAR,MONTH' # dummy word. you take it from input

# iterate over lines, and print out line numbers which contain
# the word of interest.
for i,line in enumerate(lines):
	if word_to_find in line: # or word in line.split() to search for full words
		print('Data header found in line {}'.format(i+1))
		skipN = i

# Change the delimiter (";" -> ",") in a CSV file
# https://stackoverflow.com/questions/6040711/how-to-change-the-field-separator-of-a-file-using-python
with open(input_file_csv) as infile:
	# Skip 14 lines
	for x in range(skipN):
		next(infile)
	f = open(input_folder_name + '/temp.txt', 'w')
	with f as outfile:
		for line in infile:
			fields = line.split(',')		# Semicolon
			outfile.write(','.join(fields))	# Comma

# Read the temp file
# df = pd.read_csv(input_folder_name + '/temp.txt', index_col=0)
df = pd.read_csv(input_folder_name + '/temp.txt')

# pop function which is used in removing or deleting columns from the CSV files
df.pop('MINUTE')
df.pop('SECOND')
# print(df)

# Using + operator to combine columns
df['Date'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY'].astype(str) + '-' + df['HOUR'].astype(str)

# df['Date'] = (pd.to_datetime(df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY'].astype(str) + '-' + df['HOUR'].astype(str), format='%Y-%m-%d-%H'))
# # Convert datetime to string/object
# df['ConvertedDate']=df['Date'].astype(str)
# # Iterate over given columns only from the dataframe
# for column in df[['ConvertedDate']]:
# 	# Select column contents by column name using [] operator
# 	columnSeriesObj = df[column]
# 	# Loop over number of rows
# 	for objID in range(len(df)):
# 		DatetImeObj = datetime.datetime.strptime(columnSeriesObj.values[objID], '%Y-%m-%d %H:%M:%S')
# 		finalDateTime = datetime.datetime.strftime(DatetImeObj , '%Y-%m-%d-%H')
# 		columnSeriesObj.values[objID] = finalDateTime

# Rearrange columns
cols = df.columns.tolist()
# Moves the last column to the first one
cols = cols[-1:] + cols[:-1]
df = df[cols]

# pop function which is used in removing or deleting columns from the CSV files
df.pop('YEAR')
df.pop('MONTH')
df.pop('DAY')
df.pop('HOUR')
# df.pop('Date')

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

print('Input file successfully changed to be used with package virocon')

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

data = read_ec_benchmark_dataset(output_file_txt)

# Define the structure of the joint distribution model.
dist_descriptions, fit_descriptions, semantics = get_OMAE2020_Hs_Tz()
model = GlobalHierarchicalModel(dist_descriptions)

# Estimate the model's parameter values (fitting).
model.fit(data, fit_descriptions=fit_descriptions)

# Compute an IFORM and ISORM contours with a return period of 50 years.
# tr = 50  # Return period in years. Describes the average time period between two consecutive environmental states that exceed a contour. In the univariate case the contour is a threshold.
# ts = 1  # Sea state duration in hours. Time period for which an environmental state is measured.
alpha = 1 / (tr * 365.25 * 24 / ts)
# inverse first-order reliability method (IFORM)
iform_contour = IFORMContour(model, alpha)
# inverse second-order reliability method (ISORM). More conservative
isorm_contour = ISORMContour(model, alpha)

plots_n = []
# Plot the contour
fig, axs = plt.subplots(1, 2, figsize=[10, 8], sharex=True, sharey=True)
# fig, axs = plt.subplots(1, 2, figsize=[10, 8], sharex=True, sharey=True, gridspec_kw={'width_ratios': [1000, 1]})
plot_2D_contour(iform_contour, data, semantics=semantics, ax=axs[0], swap_axis=True)
plot_2D_contour(isorm_contour, data, semantics=semantics, ax=axs[1], swap_axis=True)
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