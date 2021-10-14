import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from lmfit import SkewedGaussianModel
from lmfit import ThermalDistributionModel
import math
import pandas as pd
import glob
from scipy.stats import maxwell
import scipy.stats as stats
from mpmath import *

#AGN redshift
z = input('What is the redshift of the AGN?')

#What epoch are you studying?
YEAR = input('Which Year are you looking at? ')

# Reading the data
Spec = open(f'/{YEAR}.dat') #Open the file

Spec = np.recfromtxt(Spec, names=['Wave', 'Wave_E', 'Wave_e', 'Flux', 'Flux_E', 'Flux_e', 'Model', 'Back'])
#Read the file and set the names of the columns
#To convert wavelength units to energy units
h = 6.63E-34 #Planck constant
c = 3E8 #Speed of light

#Set the x-axis range in terms of

X = ((h*c)/((Spec.Wave/z*1E-10)))/1.6E-19 #Energy units
Y = Spec.Flux #Flux column
X_err = Spec.Wave_E #Wavelength errors column
Y_err = Spec.Flux_E #Flux errors column


#Set the energy/wavelength range for the RRC feature
x_low = float(input('Lower x-limit '))
x_up = float(input('Upper x-limit '))

xdat = []
ydat = []
T = list(zip(X, Y))


for i in range(len(T)):
	if T[i][0] > x_low and T[i][0] <= x_up:
		xdat.append(T[i][0])
		ydat.append(T[i][1])
X = xdat
Y = ydat

#Plot to check that the x-axis range is correct
plt.plot(X, Y, '-')
plt.xlabel(r'Energy (eV)', fontsize=18) #Sets the x axis label (energy units)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 18) #Sets the y axis label (incluing units)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(x_low, x_up) #Sets the limits of the x axis between 7 and 28 A
plt.ylim(-1, 5) #Sets the limits of the y axis between -1 and 40 Counts/s/m^2/A
plt.show()

####################

#Set up initial model parameters
cen = (x_low + x_up)/2
amp = 1
wid = 0.1
gam = -1

#Define the normal Gaussian Model
def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (np.sqrt(2*np.pi) * wid)) * np.exp(-(x-cen)**2 / (2*wid**2))

gaus_model = Model(gaussian)
NGM = gaus_model.fit(Y, x=X, amp=amp, cen=cen, wid=wid)

#Define the skewed Gaussian Model
skew_model = SkewedGaussianModel()
params = skew_errmodel.make_params(amplitude=amp, center=cen, sigma=wid, gamma=gam)
SGM = skew_model.fit(Y, params, x=X)

#intial model to check parameters are good
plt.figure()
plt.plot(X, Y)
plt.plot(X, NGM.init_fit, color='red')
plt.plot(X, SGM.init_fit, color='blue')

plt.xlabel(r'Energy (eV)', fontsize=18) #Sets the x axis label (energy units)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 18) #Sets the y axis label (incluing units)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(x_low, x_up) #Sets the limits of the x axis between 7 and 28 A
plt.ylim(-1, 5)
plt.show()

#Fitted model to data
plt.figure()
plt.plot(X, Y)
plt.plot(X, NGM.best_fit, color='red')
plt.plot(X, SGM.best_fit, color='blue')

plt.xlabel(r'Energy (eV)', fontsize=18) #Sets the x axis label (energy units)
plt.ylabel(r'Flux (Counts/s/$m^2$/$\AA$)', fontsize = 18) #Sets the y axis label (incluing units)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlim(x_low, x_up) #Sets the limits of the x axis between 7 and 28 A
plt.ylim(-1, 5)
plt.show()

##########################################

#####Normal Gaussian Model

#Parameter values and errors for the normal Gaussian model
print(NGM.fit_report())

print()
print('-------------------------------')
print('Parameter    Value       Stderr')
for name, param in NGM.params.items():
    print('{:7s} {:11.5f} ± {:11.5f}'.format(name, param.value, param.stderr))

#Save parameter values to measure the plasma temperature
cen_val = NGM.params['center'].value
amp_val = NGM.params['amplitude'].value
wid_val = NGM.params['sigma'].value

cen_err = NGM.params['center'].stderr
amp_err = NGM.params['amplitude'].stderr
wid_err = NGM.params['sigma'].stderr

#Calculate the plasma temperature from the RRC width
k = 1.38E-23 #Boltzmann constant
FWHM = wid_val * 2.355 #Define the full width half maximum (FWHM)

T = (FWHM * 1.6E-16)/k #Measured plasma temperature

FWHM_Err = wid_val+wid_err * 2.355 #calculating the error in the temperature
T_err = (FWHM_Err * 1.6E-16)/k
T_ERR = T - T_err

print('T =', T,'±', T_ERR) #Temperature and error


#####Skewed Gaussian Model
#Parameter values and errors for the skewed Gaussian model
print(SGM.fit_report())

print()
print('-------------------------------')
print('Parameter    Value       Stderr')
for name, param in SGM.params.items():
    print('{:7s} {:11.5f} ± {:11.5f}'.format(name, param.value, param.stderr))

#Save parameter values to measure the plasma temperature
cen_val = SGM.params['center'].value
amp_val = SGM.params['amplitude'].value
wid_val = SGM.params['sigma'].value
skew_val = SGM.params['gamma'].value

cen_err = SGM.params['center'].stderr
amp_err = SGM.params['amplitude'].stderr
wid_err = SGM.params['sigma'].stderr
skew_err = SGM.params['gamma'].stderr

#Calculate the plasma temperature from the RRC width assuming FWHM = 2.355 * sigma, which is the same as the NGM
k = 1.38E-23 #Boltzmann constant
FWHM_norm = wid_val * 2.355 #Define the full width half maximum (FWHM)

T_norm = (FWHM_norm * 1.6E-16)/k #Measured plasma temperature

FWHM_norm_Err = wid_val+wid_err * 2.355 #calculating the error in the temperature
T_norm_err = (FWHM_norm_Err * 1.6E-16)/k
T_norm_ERR = T_norm - T_norm_err

print('T =', T_norm,'±', T_norm_ERR) #Temperature and error

"""Alternatively, you can estiamte the width of the RRC using the relation from Rusch, P. F., & Lelieur, J. P. 1973, AC, 45, 1541, 
doi: 10.1021/ac60330a060 (https://pubs.acs.org/doi/abs/10.1021/ac60330a060):"""

k = 1.38E-23
FWHM = wid_val * np.sinh(skew_val)/skew_val

T = (FWHM * 1.6E-16)/k
#print(T)

FWHM_Err = (wid_val - wid_err) * (np.sinh(skew_val - skew_err)/(skew_val - skew_err))
T_err = (FWHM_Err * 1.6E-16)/k
print(T_err)

T_ERR =  T - T_err

print('T =', T,'±', T_ERR) #Temperature and error
