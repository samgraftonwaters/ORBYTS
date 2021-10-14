#Need to install the packages
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import math
import pandas as pd
import glob

#AGN redshift
z = input('What is the redshift of the AGN?')

#What epoch are you studying?
YEAR = input('Which Year are you looking at? ')

NGCspreadsheetfile=glob.glob('*.xls*')
df_YEAR=pd.ExcelFile(NGCspreadsheetfile[0])
#Python then prints all the values from the table

NGCdict_YEAR={}
sheetlist=[]
for sheet_YEAR in df_YEAR.sheet_names:
      NGCdict_YEAR[sheet_YEAR]=df_YEAR.parse(sheet_YEAR, skiprows=3)
      sheetlist.append(sheet_YEAR)
NGCdict_YEAR['YEAR']

#Python then prints all the values from the table
df_YEAR=NGCdict_YEAR['YEAR']

#The "for" loop says: "for each emission line in the table column, put each value for CEN, WID and AMP into the Gaussian model and plot this on the spectrum. Repeat untill all rows have been completed and all emission lines have been fitted. "
for i in range(len(df_YEAR[df_YEAR.columns[1]])):
    cen_YEAR =df_YEAR[df_YEAR.columns[1]]*z
    cen_err_YEAR =df_YEAR[df_YEAR.columns[2]]
    width_YEAR =df_YEAR[df_YEAR.columns[5]]
    width_err_YEAR =df_YEAR[df_YEAR.columns[6]]
    amp_YEAR =df_YEAR[df_YEAR.columns[3]]
    amp_err_YEAR =df_YEAR[df_YEAR.columns[4]]

    vel_width_YEAR =df_YEAR[df_YEAR.columns[7]]
    vel_width_err_YEAR =df_YEAR[df_YEAR.columns[8]]

    velocity_YEAR =df_YEAR[df_YEAR.columns[11]]
    velocity_err_YEAR =df_YEAR[df_YEAR.columns[12]]

    distance_YEAR =df_YEAR[df_YEAR.columns[13]]
    distance_err_YEAR =df_YEAR[df_YEAR.columns[14]]

#Save each nomalisation into an array to call later
Norm_YEAR = []
Norm_YEAR = amp_YEAR
Norm_YEAR.append(Norm_YEAR)
#Print the array

#The normalisation errors
Err_norm_YEAR = amp_YEAR+amp_err_YEAR
Norm_Err_YEAR = Norm_YEAR - Err_norm_YEAR

#Define the G and R ratios
def G_Ratio(r, i, f):
    G = (f + i)/r
    return(G)

def R_Ratio(i, f):
    R= f/i
    return(R)

#Calculate the G and R ratios for OVII and NVII triplets.
print(' ')
print (f'{YEAR} R and G Ratios')
G_O_YEAR = G_Ratio(Norm_YEAR[r], Norm_YEAR[i], Norm_YEAR[f])
R_O_YEAR = R_Ratio(Norm_YEAR[i], Norm_YEAR[f])
 #Add in the number where the r, i, and f lines are in the array. E.g. if the OVII forbidden line is the 5th value in the array, change Norm_YEAR[f] to Norm_YEAR[4]
 #Python nomenclature starts at 0 not 1. e.g. the first number in an array is called with [0]

G_N_YEAR = G_Ratio(Norm_YEAR[r], Norm_YEAR[i], Norm_YEAR[f])
R_N_YEAR = R_Ratio(Norm_YEAR[i], Norm_YEAR[f])
#Add in the number where the r, i, and f lines are in the array. E.g. if the NVI forbidden line is the 8th value in the array, change Norm_YEAR[f] to Norm_YEAR[7]

#Print the R and G ratios for O VII and N VII
print("O VII")
print('G =', G_O_YEAR, 'R =', R_O_YEAR)
print("N VI")
print('G =', G_N_YEAR, 'R =', R_N_YEAR)
