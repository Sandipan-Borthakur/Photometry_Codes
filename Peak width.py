from scipy.interpolate import UnivariateSpline as us
from astropy.io import ascii
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from scipy.signal import chirp, find_peaks, peak_widths

import numpy as np
def line_select_callback(eclick, erelease):
    global x1, y1, x2, y2
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

path='E://LNCV053/Archival Data/'
data=ascii.read(path+'ASSASN.csv')
x,y=data['hjd'],data['mag']
p=[]
for i in range(3):
    fig, current_ax = plt.subplots()
    plt.scatter(x, y)
    plt.xlim((min(x) - 2, max(x) + 2))
    plt.ylim((min(y) - 0.5, max(y) + 0.5))
    plt.gca().invert_yaxis()
    toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                           drawtype='box', useblit=True,
                                           button=[1, 3],  # don't use middle button
                                           spancoords='pixels',
                                           interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    xcorners = toggle_selector.RS.corners[0]
    ycorners = toggle_selector.RS.corners[1]
    index1 = np.where((x > x1) & (x < x2))[0]
    z1 = x[index1]
    z2 = y[index1]
    index2 = np.where((z2 > y1) & (z2 < y2))[0]
    xdata = z1[index2]
    ydata = z2[index2]
    ind = np.argsort(xdata)
    ydata = ydata[ind]
    xdata.sort()
    xdata=np.array(xdata)
    ydata=np.array(ydata)
    xdata=xdata.astype('float')
    ydata = ydata.astype('float')
    p.append([xdata,ydata])
    plt.plot(xdata,ydata)
    plt.show()