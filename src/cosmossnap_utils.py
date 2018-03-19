import numpy as np
import string
from scipy.interpolate import interp1d
from scipy.integrate import simps

def get_digits(name):
    translator = string.maketrans('', '')
    digit_trans = translator.translate(translator, string.digits)
    digits = name.translate(translator, digit_trans)
    return digits


def blueshift(spectrum, z):
    spectrum[:, 0] /= (1 + z)
    return spectrum


def get_maxfluxHa(spectrum):
    Hamask = (spectrum[:, 0] > 6540) & (spectrum[:, 0] < 6580)
    fluxHa = spectrum[Hamask]
    maxfluxHa = np.sum(fluxHa[:, 1])
    return maxfluxHa


def resample_and_integrate(spectrum, Lmin, Lmax, dL, resamp_prec=100):
    assert Lmin >= spectrum[:, 0].min(), "Lmin must be >= than min spectral wavelength"
    assert Lmax <= spectrum[:, 0].max(), "Lmax must be <= than max spectral wavelength"
    
    spline = interp1d(spectrum[:, 0], spectrum[:, 1])
    
    x = np.arange(Lmin, Lmax, dL/resamp_prec)
    xdata = x.reshape(int((Lmax - Lmin)/dL), resamp_prec)
    integrated_spec = simps(spline(xdata), dx=dL/resamp_prec, axis=1)
    
    out_spectrum = np.array([np.arange(Lmin + dL/2, Lmax + dL/2, dL), integrated_spec]).T
    assert out_spectrum.shape == ((Lmax - Lmin)/dL, 2)
    del spectrum
    
    return out_spectrum