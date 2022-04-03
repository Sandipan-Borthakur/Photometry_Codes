import numpy as np

def tvsigmascl(img, factor1=1, factor2=1):
    med = np.median(img)
    std = np.std(img)
    img1 = img.copy()
    ind = np.where(img < med-std*factor1)
    img1[ind] = med-std*factor1
    ind = np.where(img > med+std*factor2)
    img1[ind] = med+std*factor2
    return img1
