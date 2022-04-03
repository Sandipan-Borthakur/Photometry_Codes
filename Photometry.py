import matplotlib.pyplot as plt
import numpy as np
from astropy.io import ascii
from lightcurve import lightcurve
from cube_generation import gen_bias,gen_flat,cube_gen
import os
from tvsigma import tvsigmascl

path='for phototmetry/'                               # Data to be divided into three folders - science, bias and flat
sciencelist=os.listdir(os.path.join(path,'science'))  # Generates list of filenames in the science folder
imgCube,timearr=cube_gen(path,sciencelist)            # Generated the imagecube and time array required for the lightcurve function  

circ_aper,r_in,r_out=3.5,15,20                        # use either circ_aper or a and b. Use theta(optional) only if a and b is used. 
a=5
b=4
theta=0
m_list=[]
n_stars_photometry = 5

for i in range(n_stars_photometry):
    imglist,timearray=imgCube[:],timearr[:]
    t,m=lightcurve(imglist,timearray,r_in,r_out,a=a,b=b) # Can chose either circular or elliptical aperture. For circular aperture write - circ_aper = .
    plt.plot(t,m,'bo')                                   #  For elliptical aperture write a= ,b =. You can also chose for tilted ellipse by adding the parameter theta = .
    plt.show()
    meantime=np.mean(timearray)
    m_list.append(m)
# ascii.write([t,m_list[0],m_list[1],m_list[2],m_list[3],m_list[4]],str(meantime)+'V1948Cyg_V.csv',names=['Time','Mag(Source)','Mag(2MASS19291490+5006277)','Mag(2MASS19291377+5006585)',
#                                                                                             'Mag(2MASS19290790+5006011)','Mag(2MASS19292589+5006477)'],format='csv')