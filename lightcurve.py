import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from photutils import centroid_com, centroid_1dg, centroid_2dg
from photutils import aperture_photometry,CircularAperture, CircularAnnulus,EllipticalAperture
import numpy as np
from astropy.stats import sigma_clipped_stats
from tvsigma import tvsigmascl
from fitgauss2D import fitgauss2D
import astroalign as aa
from astropy.io import fits
from cube_generation import cube_gen,read_fits_images
import os
from astropy.table import Table
from astropy.io import ascii

global names,data


def onclick(event):
    global x, y
    if event.button==3:
        x = event.xdata
        y = event.ydata
        plt.close()


def lightcurve(imageCube,timearr,r_in,r_out,**kwargs):

    plt.imshow(tvsigmascl(imageCube[0]), cmap="gray", origin="lower")
    plt.connect('button_press_event', onclick)
    plt.show()

    roi_width = 10

    x_min = x - roi_width if x - roi_width > 0 else 0
    x_max = x + roi_width + 1 if x + roi_width + 1 < 1024 else 1024
    y_min = y - roi_width if y - roi_width > 0 else 0
    y_max = y + roi_width + 1 if y + roi_width + 1 < 1024 else 1024

    roi = imageCube[0][int(y_min):int(y_max), int(x_min):int(x_max)]
    x_C, y_C = centroid_com(roi)
    x_C1, y_C1 = x_C + int(x_min), y_C + int(y_min)
    mag = []
    t=[]
    for i in range(len(imageCube)):
        print(i)
        t.append(timearr[i])
        d = imageCube[i]
        transf, (source_list, target_list) = aa.find_transform(source=imageCube[0], target=d)
        dst_calc = aa.matrix_transform([(x_C1, y_C1)], transf.params)

        x_min = dst_calc[0][0] - roi_width if dst_calc[0][0] - roi_width > 0 else 0
        x_max = dst_calc[0][0] + roi_width + 1 if dst_calc[0][0] + roi_width + 1 < 1024 else 1024
        y_min = dst_calc[0][1] - roi_width if dst_calc[0][1] - roi_width > 0 else 0
        y_max = dst_calc[0][1] + roi_width + 1 if dst_calc[0][1] + roi_width + 1 < 1024 else 1024

        cropped_image = d[int(y_min):int(y_max), int(x_min):int(x_max)]
        x_C, y_C = centroid_com(cropped_image)
        x_C, y_C = x_C + int(x_min), y_C + int(y_min)
        positions = [(x_C, y_C)]

        if 'circ_aper' in kwargs.keys():
            circ_aper = kwargs['circ_aper']
            aperture = CircularAperture(positions, r=circ_aper)  # 3.5
        elif 'a' in kwargs.keys() and 'b' in kwargs.keys():
            a = kwargs['a']
            b = kwargs['b']
            try:
                theta = kwargs['theta']
            except:
                theta = 0
            aperture = EllipticalAperture(positions, a=a, b=b, theta=theta)  # 3.5
        else:
            print('Check for correct Aperture')
            stop
        annulus_aperture = CircularAnnulus(positions, r_in=r_in, r_out=r_out)  # 15,20
        annulus_masks = annulus_aperture.to_mask(method='center')

        if i==0:
            plt.imshow(tvsigmascl(imageCube[0]), cmap="gray", origin="lower")
            aperture.plot(color='white', lw=2)
            annulus_aperture.plot(color='red', lw=2)
            plt.show()
        bkg_median = []
        for mask in annulus_masks:
            annulus_data = mask.multiply(d)
            annulus_data_1d = annulus_data[mask.data > 0]
            _, median_sigclip, _ = sigma_clipped_stats(annulus_data_1d)
            bkg_median.append(median_sigclip)
        bkg_median = np.array(bkg_median)
        phot = aperture_photometry(d, aperture)
        phot['annulus_median'] = bkg_median
        phot['aper_bkg'] = bkg_median * aperture.area
        phot['aper_sum_bkgsub'] = phot['aperture_sum'] - phot['aper_bkg']
        p = -2.5 * np.log10(phot['aper_sum_bkgsub'])
        p = float(p)
        mag.append(p)
    return(t,mag)

