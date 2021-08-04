# ORBYTS
Python code for the ORBYTS outreach project to analyse the emission lines in the active galactic nucleus (AGN), NGC 4151. This code can be used to study the soft X-rays spectra of any AGN, provided the correct data is obtained.

To cite these codes, use **DOI: 10.5281/zenodo.5116838 @ https://zenodo.org/record/5116838**

**NGC4151_Code.py** 

This code is used to fit Gaussian models to the strong emission lines in the RGS spectra, where the amplidute, line centre and width are measured. From here, the line shift can be calculated, allowing for the velocity and distance of each line to be calculated. This means the number of plasma clouds in the outflowing wind can be determined. See **S. Grafton-Waters et al 2021 Res. Notes AAS 5 172** (https://doi.org/10.3847/2515-5172/ac1689) for further details.

**RRC_Modelling.py**

This code is used to study the radiative recombination continua (RRC) features in the soft X-ray spectra. RRCs are produced when the free electrons, with a thermal distribution, recombine to the ground state of an ion. For PI plasma, the RRC is narrow and strong, whereas for collisionally ionised (CI) plasma, the line is broad and weak. 

The widths of each RRC line is approximately equal to the thermal energy of the plasma, kT. Therefore, this code estimates the plasma temperature based on the width. Two models are utalised here - the skewed Gaussian model (SGM) and normal Gaussian model (NGM).

**R_G_Ratios.py**

**Analysis_Table.xls**

Table template to place your results; this table is then read later to plot data or obtain R and G ratio values. Change name accordingly - for example 'YEAR' of observation; the tabs refer to the epoch observation. The columns (in Python notation) are:

[1] Observed wavelength value; [2] Observed wavelength error
[3] Line amplitude value; [4] [3] Line amplitude error
[5] Line width value (wavelength units); [6] Line width error (wavelength units)
[7] Line width value (velocity units); [8] Line width error (velocity units)
[9] Rest wavelength (from SPEX line list: ); [10] Ion name
[11] Line velocity value; [12] Line velocity error
[13] Distance value; [14] Distance error
