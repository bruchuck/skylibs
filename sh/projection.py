
import numpy as np
from numpy import pi, sin, cos, sqrt, arctan
from math import factorial

import time
import envmap
from libsh import ffi, lib
from tqdm import tqdm
from scipy.special import sph_harm

# calcula coeficiente A / pi para determinado l
def calculateACoef(L):
    if(L == 0):
        return 1.0
    elif(L == 1):
        return 2.0 / 3.0
    elif(L % 2 == 1):
        return 0.0
    else:
        return pi * ((-1.0)**(L / 2.0 - 1.0)) / ((L + 2.0) * (L - 1.0)) * factorial(L) / (2.0 ** L * (factorial(L / 2))**2.0)

#A = [pi, (2.0 * pi) / 3.0, 0.25* pi, 0.0] # valor pré calculado de A 
#A = [1, 2.0 / 3.0, 0.25, 0.0] # valor pré calculado de A / pi
A = [1.0, 1.0, 1.0, 1.0]

# constant map
Y = {}
# Banda 0
Y[(0, 0)] = 0.5 * sqrt(1 / pi) * A[0]
# Banda 1
Y[(1, -1)] = sqrt(3.0 / (4.0 * pi)) 
Y[(1, 0)] = sqrt(3.0 / (4.0 * pi)) 
Y[(1, 1)] = sqrt(3.0 / (4.0 * pi)) 
# Banda 2
Y[(2, -2)] = 0.5 * sqrt(15.0 / pi)
Y[(2, -1)] = 0.5 * sqrt(15.0 / pi)
Y[(2, 0)] = 0.25 * sqrt(5.0 / pi) * 0.25
Y[(2, 1)] = 0.5 * sqrt(15.0 / pi) 
Y[(2, 2)] = 0.25 * sqrt(15.0 / pi) * 0.5

# Banda 3 --> A[3] = 0 !!
Y[(3, -3)] = 0.25 * sqrt(35.0 / (2 * pi)) * A[3]
Y[(3, -2)] = 0.5 * sqrt(105.0 / pi) * A[3]
Y[(3, -1)] = 0.25 * sqrt(21.0 / (2 * pi)) * A[3]
Y[(3, 0)] = 0.25 * sqrt(7.0 / pi) * A[3]
Y[(3, 1)] = 0.25 * sqrt(21.0 / (2 * pi)) * A[3]
Y[(3, 2)] = 0.25 * sqrt(105.0 / pi) * A[3]
Y[(3, 3)] = 0.25 * sqrt(35.0 / (2 * pi)) * A[3]

# mapeando para função
SH = {}
SH[(0,  0)] = lambda normal: Y[(0,  0)]
SH[(1, -1)] = lambda normal: Y[(1, -1)] * normal[1]
SH[(1,  0)] = lambda normal: Y[(1,  0)] * normal[2]
SH[(1,  1)] = lambda normal: Y[(1,  1)] * normal[0]
SH[(2, -2)] = lambda normal: Y[(2, -2)] * normal[0] * normal[1]
SH[(2, -1)] = lambda normal: Y[(2, -1)] * normal[1] * normal[2]
SH[(2,  0)] = lambda normal: Y[(2,  0)] * (3.0 * normal[2] * normal[2] - 1.0)
SH[(2,  1)] = lambda normal: Y[(2,  1)] * normal[0] * normal[2]
SH[(2,  2)] = lambda normal: Y[(2,  2)] * (normal[0] * normal[0] - normal[1] * normal[1])


#Scipy version
def project_scipy(env, degrees):
    # An environment map projection is three different spherical functions, one
    # for each color channel. The projection integrals are estimated by
    # iterating over every pixel within the image.
    ch = 3
    if degrees is None:
        degrees = np.ceil(np.maximum(envmap.shape) / 2.)

    retval = np.zeros(((degrees + 1)**2, 3), dtype=np.float)
    coeffs = np.zeros((3,IrradianceCoeffsCount))

    f = env.data * env.solidAngles()[:,:,np.newaxis]

    x, y, z, valid = env.worldCoordinates()
    theta = np.arctan2(x, -z)
    phi = np.arccos(y)

    for l in tqdm(range(degrees + 1)):
        for col, m in enumerate(range(-l, l + 1)):
            start = time.time()
            Y = sph_harm(m, l, theta, phi)
            print(time.time() - start)
            for c in range(ch):
                retval[l**2+col,c] = np.nansum(Y*f[:,:,c])

    return retval

#C version
def project_c(env, degrees=2, progress=True):
    # An environment map projection is spherical harmonics functions,
    # one projection for each color channel. The projection integrals are estimated by
    # iterating over every pixel within the image.

    ch = 3
    retval = np.zeros(((degrees + 1)**2, ch), dtype=np.float)
    Ysh = np.zeros((np.shape(env.data)[0], np.shape(env.data)[1]), dtype=np.float64)

    f = env.data * env.solidAngles()[:,:,np.newaxis]

    x, y, z, valid = env.worldCoordinates()
    normals = np.dstack((x,y,-z))

    output_data_ptr = ffi.cast("double *", Ysh.ctypes.data)
    normals_ptr = ffi.cast("float *", normals.ctypes.data)
    height = ffi.cast("unsigned int", np.shape(env.data)[0])
    width = ffi.cast("unsigned int", np.shape(env.data)[1])

    for l in tqdm(range(degrees + 1), disable=not progress):
        for col, m in enumerate(range(-l, l + 1)):
            #start = time.time()
            lib.ySH(normals_ptr, output_data_ptr, height, width, l, m)
            #print(time.time() - start)
            for c in range(ch):
                retval[l**2+col,c] = np.nansum(Ysh*f[:,:,c])
    return retval

#Pure python version
def project(env, degrees):
    # An environment map projection is three different spherical functions, one
    # for each color channel. The projection integrals are estimated by
    # iterating over every pixel within the image.

    ch = 3
    if degrees is None:
        degrees = np.ceil(np.maximum(envmap.shape) / 2.)

    retval = np.zeros(((degrees + 1)**2, ch), dtype=np.float)
    f = env.data * env.solidAngles()[:,:,np.newaxis]
    x, y, z, valid = env.worldCoordinates()
    normals = np.dstack((x,y,-z))

    for l in tqdm(range(degrees + 1)):
        for col, m in enumerate(range(-l, l + 1)):
            Ysh = [[SH[l, m](normal) for normal in row] for row in normals]
            for c in range(ch):
                retval[l**2+col,c] = np.nansum(Ysh*f[:,:,c])
    return retval