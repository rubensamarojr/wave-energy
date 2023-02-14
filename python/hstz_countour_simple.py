"""
Brief example that computes a sea state contour.
Library virocon
https://github.com/virocon-organization/virocon
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
	plot_2D_contour,
)

# File skip first N lines (Verify how many lines need to be skiped until the header )
skipN = 14
# Input CSV file name (buoy from https://simcosta.furg.br/)
inpute_file_name = 'SIMCOSTA_RS-5_ANT._OCEAN_2016-12-07_2021-11-18' # Buoy File name in folder datasets
# inpute_file_name = 'SIMCOSTA_RJ-3_OCEAN_2016-07-14_2023-02-14'
input_file_csv = 'datasets/' + inpute_file_name + '.csv'
# Output CSV file name formatted to be used with virocon functions
output_file_csv = 'datasets/' + inpute_file_name + '_comma.csv'
# Output TXT file name formatted to be used with virocon functions
output_file_txt = 'datasets/' + inpute_file_name + '_comma.txt'


# Change the delimiter (";" -> ",") in a CSV file
# https://stackoverflow.com/questions/6040711/how-to-change-the-field-separator-of-a-file-using-python
with open(input_file_csv) as infile:
	# Skip 14 lines
	for x in range(skipN):
		next(infile)
	f = open("datasets/temp.txt", "w")
	with f as outfile:
		for line in infile:
			fields = line.split(',')		# Semicolon
			outfile.write(','.join(fields))	# Comma

# Read the temp file
# df = pd.read_csv("datasets/temp.txt", index_col=0)
df = pd.read_csv("datasets/temp.txt")

# pop function which is used in removing or deleting columns from the CSV files
df.pop('MINUTE')
df.pop('SECOND')
# print(df)

# Using + operator to combine columns
df["Date"] = df['YEAR'].astype(str) + "-" + df["MONTH"].astype(str) + "-" + df["DAY"].astype(str) + "-" + df["HOUR"].astype(str)

# df["Date"] = (pd.to_datetime(df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY'].astype(str) + '-' + df['HOUR'].astype(str), format='%Y-%m-%d-%H'))
# # Convert datetime to string/object
# df['ConvertedDate']=df["Date"].astype(str)
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
df.to_csv('datasets/temp.txt',index=False)

# Rename Header Columns in CSV File
with open('datasets/temp.txt', 'r', encoding='utf-8') as file:
	data = file.readlines()
data[0] = "time (YYYY-MM-DD-HH),significant wave height (m),zero-up-crossing period (s)\n"
with open('datasets/temp.txt', 'w', encoding='utf-8') as file:
	file.writelines(data)

# Check if ouputfile already exists, then delete it:
if os.path.exists(output_file_csv):
	os.remove(output_file_csv)

# Renaming the file
os.rename("datasets/temp.txt", output_file_csv)

print("Input File successfully changed")

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

# Compute an IFORM contour with a return period of 50 years.
tr = 50  # Return period in years.
ts = 1  # Sea state duration in hours.
alpha = 1 / (tr * 365.25 * 24 / ts)
contour = IFORMContour(model, alpha)

# Plot the contour
plot_2D_contour(contour, data, semantics=semantics, swap_axis=True)
fig = plt.gcf() # get current figure

# Make directory
fig_directory_name = 'figs'
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, fig_directory_name)
if not os.path.exists(final_directory):
	os.makedirs(final_directory)

# Save Figure
fig_name = inpute_file_name + '_envirom_countor'
fig.savefig(fig_directory_name + '/' + fig_name + '.png')
plt.show()
plt.close(fig)    # close the figure window