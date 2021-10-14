%pip install lmfit
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import math
import pandas as pd
import glob
plt.rcParams['figure.figsize'] = [10, 8]

#AGN redshift
z = input('What is the redshift of the AGN?')

# 2000, 2003, 2006, 2011, 2012, 2015
YEAR = input('Which Year are you looking at? ')
# Obs1, Obs2, Obs3 ...
OBS = input('What observation are you investigating? ')

# Reading the data
Spec = open(f'/{YEAR}/{OBS}.dat') #Open the file

Spec = np.recfromtxt(Spec, names=['Wave', 'Wave_E', 'Wave_e', 'Flux', 'Flux_E', 'Flux_e', 'Model', 'Back'])
#Read the file and set the names of the columns

#From the table, choose the columns we want to use
X = Spec.Wave/z  #Wavelength column
Y = Spec.Flux #Flux column
X_err = Spec.Wave_E #Wavelength errors column
Y_err = Spec.Flux_E #Flux errors column

#Plotting the Spectrum (with out errors)
plt.plot(X, Y) #Plots X axis against Y axis (wavelenght angainst flux)
plt.xlabel(r'Wavelength ($\AA$)', fontsize = 20) #Sets the x axis label (including units)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 20)#Sets the y axis label (incluing units)
plt.xlim(7, 37) #Sets the limits of the x axis between 7 and 28 A
plt.ylim(-1, 35) #Sets the limits of the y axis between -1 and 80 Counts/s/m^2/A
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show() #Shows the plot

plt.figure()
plt.subplot(311)
plt.plot(X, Y)
plt.xlim(7,15)
plt.ylim(0,10)
plt.subplot(312)
plt.plot(X, Y)
plt.xlim(15,28)
plt.ylim(0,50)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 20)
plt.subplot(313)
plt.plot(X, Y)
plt.xlim(28,37)
plt.ylim(0,20)
plt.xlabel(r'Wavelength ($\AA$)', fontsize = 20)
plt.show()

#Defining our models
#Here we set up our model, in this case a Gaussian is used to model the emission lines

#Defining our simple Gaussian model
def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2*np.pi) * wid)) * np.exp(-(x-cen)**2 / (2*wid**2))

X = Spec.Wave/1.00332
Y = Spec.Flux

#Set the x limits:
x_low = float(input('Lower x-limit '))
x_up = float(input('Upper x-limit '))
#For the full spectrum, set x_low = 7 and x_up = 38

xdat = []
ydat = []
T = list(zip(X, Y))

for i in range(len(T)):
	if T[i][0] > x_low and T[i][0] <= x_up:
		xdat.append(T[i][0])
		ydat.append(T[i][1])
X = xdat
Y = ydat

plt.plot(X, Y, '-')
plt.xlabel(r'Wavelength ($\AA$)', fontsize=18) #Sets the x axis label (including units)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 18) #Sets the y axis label (incluing units)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(x_low, x_up) #Sets the limits of the x axis between 7 and 28 A
plt.ylim(-1, 40) #Sets the limits of the y axis between -1 and 40 Counts/s/m^2/A
plt.show()

CEN = float(input('What is the wavelength of the line? (%.2f < cen < %.2f):' % (x_low, x_up)))
AMP = float(input('What is the amplitude of the line? (0 < amp < 10):' ))
WID = float(input('What is the width of the line? (0.001 < wid < 0.5):' ))

#Print your selected parameter values
print(AMP, CEN, WID)

#Take your Gaussian (defined above) and set it to a model
gmodel = Model(gaussian)
#The Gaussian model fits the data using the intitial parameter values chosen 
result1 = gmodel.fit(Y, x=X, amp=AMP, cen=CEN, wid=WID)

#Asym_Model = Model(Asym_Gaus)
#Result = Asym_Model.fit(Y, x=X, A=AMP, cen=CEN, wid=WID, r=1 )


#Plot the model to the data from your initial values
#Was the initial parameter estimate good enough?
plt.figure()
plt.plot(X, Y)
#plt.plot(X, result1.init_fit)
plt.plot(X, result1.init_fit)
plt.plot(X, result1.best_fit)
plt.xlabel(r'Wavelength ($\AA$)', fontsize=18) #Sets the x axis label (including units)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 18) #Sets the y axis label (incluing units)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(x_low, x_up) #Sets the limits of the x axis between 7 and 28 A
plt.ylim(-1, 40) #Sets the limits of the y axis between -1 and 40 Counts/s/m^2/A
plt.show()

plt.figure()
plt.plot(X, Y)
plt.plot(X, result1.best_fit)
plt.xlabel(r'Wavelength ($\AA$)', fontsize=18) #Sets the x axis label (including units)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 18) #Sets the y axis label (incluing units)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(x_low, x_up) #Sets the limits of the x axis between 7 and 28 A
plt.ylim(-1, 40) #Sets the limits of the y axis between -1 and 40 Counts/s/m^2/A

plt.show()

#Print out the model properties
print(result1.fit_report())
#The main information here that we want are the "[Variables]": amp, cen and wid values along with their errors
print()
print('-------------------------------')
print('Parameter    Value       Stderr')
for name, param in result1.params.items():
    print('{:7s} {:11.5f} ± {:11.5f}'.format(name, param.value, param.stderr))
#Here we have printed the three parameters and their errors (±) in a clearer way.

cen_val = result1.params['cen'].value
amp_val = result1.params['amp'].value
wid_val = result1.params['wid'].value

cen_err = result1.params['cen'].stderr
amp_err = result1.params['amp'].stderr
wid_err = result1.params['wid'].stderr

#Velocity
Wave_Rest = float(input('What is the rest wavelength of the fitted line? '))

def Speed(wave_obs, wave_rest, c):
    v = ((wave_obs/wave_rest) - 1)*c
    return(v)

c = 3E8 #Speed of light

v_out = Speed(cen_val, Wave_Rest, c)
#print('vout =', v_out, 'm/s') #This prints out the velocity of the emission line, relative to the rest frame

v = Speed(cen_val + cen_err, Wave_Rest, c)

v_out_err = np.sqrt((np.sqrt(v_out**2) - np.sqrt(v**2))**2)

#The error is the difference between the observed velocity and the velocity uncertainty value
print(' ')

#Print out the final line: Velocity ± Error
print('-----------------')
print('v_out =', v_out, '±', v_out_err/2 , 'm/s')

#Distance
def Dist(v, G, M):
    R = (2 * G * M) / (v**2)
    return(R)
G = 6.67E-11 #Gravitational constant
M_sol = 1.9891E30 #Mass of sun in kg
M = 4E7 * M_sol #black hole mass \citep{Bentz_Katz2015}
v_out = v_out #outflow velocity

R = Dist(v_out, G, M)
print(' ')

############
### Error on the distance
vel = (np.sqrt(v_out**2) + np.sqrt(v_out_err**2))

r = Dist(vel, G, M) #Calculate the distance using the velocity + error in velocity (distance uncertainty)

R_err = R - r #The error in the distance is equal to the difference between the distance and the distance uncertainty


#Print out the final line: Distance + Error
print('------------')
print('R =', R, '±', R_err/2, 'm')

######### Line width
def Vel_Width(wid, cen, c):
    v = (2.335 * wid * c) / cen
    return v

c = 3E8 #Speed of light

WV = Vel_Width(wid_val, cen_val, c)

#Error on Velocity width

WV_err = Vel_Width(wid_val+wid_err, cen_val+cen_err, c)

WV_Error = WV_err - WV  #The error is the difference between the new value and the acutal value observed value
print(' ')

#Print out the final line: Velocity width ± Error
print('------------------')
print('Vel Width = ', WV , '±', WV_Error/2)

X = Spec.Wave 
Y = Spec.Flux

# 2000, 2003, 2006, 2011, 2012, 2015
YEAR = input('Which Year are you looking at? ')
# Obs1, Obs2, Obs3 ...
OBS = input('What observation are you investigating? ')

#This reads the spreadsheet from the epoch (Year) and Observation (OBS)
NGCspreadsheetfile=glob.glob(f'/{YEAR}/*.xls*')
df=pd.ExcelFile(NGCspreadsheetfile[0])

#Python reads the columns for the values of interest and saves them in a list "Sheetlist = []"
NGCdict={}
sheetlist=[]
for sheet in df.sheet_names:
      NGCdict[sheet]=df.parse(sheet, skiprows=3)
      sheetlist.append(sheet)
NGCdict[OBS]

#Python then prints all the values from the table
df=NGCdict[OBS]
print(df)

#and plots each Gausian model onto each emission line from the data
plt.plot(X, Y, color='grey')

#The FOR loop says: "for each emission line in the table column, put each value for CEN, WID and AMP 
#into the Gaussian model and plot this on the spectrum. 
#Repeat untill all rows have been completed and all emission lines have been fitted.

for i in range(len(df[df.columns[1]])):
    cen=df[df.columns[1]]*1.00332
    cen_err=df[df.columns[2]]
    width=df[df.columns[5]]
    width_err=df[df.columns[6]]
    amp=df[df.columns[3]]
    amp_err=df[df.columns[4]]

    vel_width=df[df.columns[7]]
    vel_width_err=df[df.columns[8]]

    velocity=df[df.columns[11]]
    velocity_err=df[df.columns[12]]

    distance=df[df.columns[13]]
    distance_err=df[df.columns[14]]

    gmodel = Model(gaussian) 
    result1 = gmodel.fit(Y, x=X, amp=amp[i], cen=cen[i], wid=width[i])
    
    plt.plot(X, result1.init_fit, color='red')

#Example plots from columns in the spreadsheet
plt.xlabel(r'Wavelength ($\AA$)', fontsize=18)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(7, 38)
plt.show()

plt.errorbar(cen, velocity, xerr=cen_err, yerr=velocity_err, color='red', fmt='o')
plt.xlabel(r'Wavelength ($\AA$)', fontsize=18)
plt.ylabel(r'Velocity ($m s^{-1}$)', fontsize = 18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(7, 38)
plt.show()

#Distance against wavelength 
plt.errorbar(cen, distance, xerr=cen_err, yerr=distance_err, color='blue', fmt='x')
plt.xlabel(r'Wavelength ($\AA$)', fontsize=18)
plt.ylabel(r'Distance (m)', fontsize = 18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(7, 38)
plt.show()

#Distance against velocity
plt.errorbar(velocity, distance, xerr=velocity_err, yerr=distance_err, color='green', fmt='s')
plt.xlabel(r'Velocity ($m s^{-1}$)', fontsize=18)
plt.ylabel(r'Distance (m)', fontsize = 18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(7, 38)
plt.show()
