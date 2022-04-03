Photometry Codes - To reduce raw images of the sky from MFOSC-P instrument mounted on the Mt. Abu 1.2m telescope
                                  and do photometry on the source of interest

Use lightcurve function from lightcurve.py to generate lightcurve of the source of interest. 
Use photometry.py to test the code. You can use for photometry folder to test the code.

lightcurve(imageCube,timearr,r_in,r_out,**kwargs)

Returns time array and magnitudes array for lightcurve.

imageCube = Datacube of multiple images observed at different time.
timearr = Time of observation of each image
r_in = inner sky aperture for background sky 
r_out = outer sky aperture for background sky

**kwargs - 
If you want a Circular aperture - 
circ_aper = float value. Aperture radius for the star.

If you want a Elliptical aperture - 
a = float value. Semi-major axis of the aperture
b = float value. Semi-minor axis of the aperture
theta = float value(optional). Tilted elliptical aperture.

Requirements - 
1. astroalign (pip install astroalign)

Steps to follow-
1. Right click on the star you want to do photometry.
2. Image with the aperture will appear. Press "q" if satisfied, else chose a different aperture.

