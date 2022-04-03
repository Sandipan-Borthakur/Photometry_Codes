import math
import numpy as np
from numpy import zeros,newaxis
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Cursor,Button
import scipy.optimize as opt

import numpy as np
import pandas as pd
from astropy.modeling import models, fitting
from astropy.stats import (gaussian_sigma_to_fwhm, gaussian_fwhm_to_sigma,
                           sigma_clipped_stats)

def fitgauss2D(cropped_image):
    _, clipmed, clipstd = sigma_clipped_stats(cropped_image, sigma=2)
    indi = np.where(cropped_image <= clipmed + 6 * clipstd)
    subimnoise = np.random.randn(cropped_image.shape[0], cropped_image.shape[1]) * 50
    cropped_image[indi] = subimnoise[indi]

    yme,xme=np.where(cropped_image ==cropped_image.max())
    gauss = models.Gaussian2D(amplitude=cropped_image.max(), theta=0,
                              x_mean=xme, y_mean=yme,
                              x_stddev= 2 * gaussian_fwhm_to_sigma,
                              y_stddev= 2 * gaussian_fwhm_to_sigma)
    fitter = fitting.LevMarLSQFitter()
    y, x = np.indices(cropped_image.shape)
    fit = fitter(gauss, x, y, cropped_image)

    mean_y = fit.y_mean.value
    mean_x = fit.x_mean.value
    fwhm_y = fit.y_stddev.value * gaussian_sigma_to_fwhm
    fwhm_x = fit.x_stddev.value * gaussian_sigma_to_fwhm
    amplitude = fit.amplitude.value
    theta = np.rad2deg(fit.theta.value)

    return mean_x,mean_y,fwhm_x,fwhm_y,amplitude,theta

