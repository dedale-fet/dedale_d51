from __future__ import division, print_function
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import quad, simps
from astropy.table import Table, vstack
from astropy.io import fits
import glob
import os
import string
import time
import sys

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

def process_cosmosnap_to_tips(specname, photname, Lmin, Lmax, dL, resamp_prec=100, zfraction=None, zmin=1.0, zmax=2.0, flux_thresh=None, outfolder="./"):
    print("Spec: ", specname)
    print("Phot: ", photname)
    print("Outfolder: ", outfolder)
    
    wavelengths = np.arange(Lmin + dL/2, Lmax + dL/2, dL)
    
    t0 = time.time()
    # Assert files are from the same run
    assert get_digits(specname) == get_digits(photname), "Ordering didn't work, files are not the same"

    # From photometry output, choose a subset of {zfraction}% spectra ID at redshift < {zmax}
    # and Halpha flux >= {flux_thresh}
    phot = Table.read(photname, format="ascii")
    zrange = phot[(phot["z"] >= zmin) & (phot["z"] <= zmax)]
    if flux_thresh is not None:
        assert isinstance(flux_thresh, (float, int)), "flux_thresh must be an int or float"
        zrange = zrange[zrange["Flux_Ha"] >= flux_thresh]
    if len(zrange) == 0:
        print("No objects remain after redshift cut.")
        return None
    
    if zfraction is not None:
        np.random.seed(i)
        frac_idx = np.random.choice(np.arange(len(zrange)), size=int(len(zrange)*zfraction),
                                    replace=False)
        zfrac = zrange[frac_idx]
        print(len(zfrac))
    else:
        zfrac = np.copy(zrange)
        print(len(zfrac))
    entries = zfrac["SpcExt"]
    specIDs = zfrac["Id"]
    redshifts = zfrac["z"]
    
    hdulist = fits.open(specname)
    
    for specID, entry, z in zip(specIDs, entries, redshifts):
        hdu = hdulist[entry]
        assert int(hdu.name) == specID, ("Spec ID from phot and spec cats " +
                                         "doesnt'match: %d vs %d" % (int(hdu.name), specID))
        hdudata = hdu.data
        spectrum = np.array([hdudata.field("lambda"), hdudata.field("flux")]).T

        # Create output hdulist, format to TIPS specifications and save.
        tbhdu = fits.BinTableHDU.from_columns(
            [fits.Column(name='wave', format='D', array=spectrum[:, 0]),
             fits.Column(name='flux', format='D', array=spectrum[:, 1])])
        outclean = os.path.join(outfolder, "clean_TIPSspec_ID_" + str(specID) + ".fits")
        try:
            tbhdu.writeto(outclean)
        except IOError as e:
            print(e)
            print("Removing older file...")
            os.system("rm " + outclean)
            tbhdu.writeto(outclean)
    t1 = time.time() - t0        
    print("File done in %.1f seconds!" % t1)
    
    return None


if __name__ == "__main__":
    photname = sys.argv[1]
    specname = sys.argv[2]
    outfolder = sys.argv[3]
    process_cosmosnap_to_tips(specname, photname, Lmin=1250, Lmax=20000, dL=5,
    zmin=0, zmax=10.0, outfolder=outfolder)
