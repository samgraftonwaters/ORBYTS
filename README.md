# ORBYTS
Python code for the ORBYTS outreach project to analyse the emission lines in the active galactic nucleus (AGN), NGC 4151. This code can be used to study the soft X-rays spectra of any AGN, provided the correct data is obtained.


**NGC4151_Code.py**
This code is used to fit Gaussian models to the strong emission lines in the RGS spectra, where the amplidute, line centre and width are measured. From here, the line shift can be calculated, allowing for the velocity and distance of each line to be calculated. This means the number of plasma clouds in the outflowing wind can be determined. See **S. Grafton-Waters et al 2021 Res. Notes AAS 5 172** (https://doi.org/10.3847/2515-5172/ac1689) for further details.

**RRC_Modelling.py**
This code is used to study the radiative recombination continua (RRC) features in the soft X-ray spectra. RRCs are produced when the free electrons, with a thermal distribution, recombine to the ground state of an ion. For PI plasma, the RRC is narrow and strong, whereas for collisionally ionised (CI) plasma, the line is broad and weak. 

The widths of each RRC line is approximately equal to the thermal energy of the plasma, kT. Therefore, this code estimates the plasma temperature based on the width. Two models are utalised here - the skewed Gaussian model (SGM) and normal Gaussian model (NGM).

**R_G_Ratios.py**


 DOI: 10.5281/zenodo.5116838 @ https://zenodo.org/record/5116838
