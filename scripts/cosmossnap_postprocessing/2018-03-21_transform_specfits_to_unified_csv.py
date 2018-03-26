import numpy as np
import sys
import os
import glob
import pandas as pd
from astropy.io import fits
from itertools import takewhile
import time

from dedale_d51.src.cosmossnap_utils import resample_and_integrate, blueshift #,read_cosmossnap_photometry_file

def read_cosmossnap_photometry_file(filename):
    # Get column names from header
    with open(filename, 'r') as fobj:
        headiter = takewhile(lambda s: s.startswith('#'), fobj)
        colnames = [elem.split()[2] for elem in headiter]
    # Open with pandas
    photometry = pd.read_csv(filename, delim_whitespace=True, comment="#", names=colnames)
    return photometry


def main(photfile, specfolder, Lmin, Lmax, dL, zmax=None, restframe=False, resamp_prec=100, subsample_fraction=1.0, outpath="./templates.csv"):

    # Input data
    photometry = read_cosmossnap_photometry_file(photfile)
    if zmax is not None:
        assert isinstance(zmax, (int, float)), ("zmax should be the maximum redshift value for "
                                                + "object selection (a float between 0 and 6)")
        photometry = photometry[photometry["z"] < zmax]
    specIDs = photometry["Id"]
    redshifts = photometry["z"]
            
    flist = glob.glob(os.path.join(specfolder, "*.fits"))
    assert len(flist) == 58, "File list is not complete."

    # Initialize output tables
    template_clean = {}
    wavelengths = np.arange(Lmin + dL/2, Lmax + dL/2, dL)
    template_clean["lambda"] = wavelengths
    
    for specname in flist:
        t0 = time.time()
        hdulist = fits.open(specname)
        
        for hdu in hdulist[1:]:
            photmask = (int(hdu.name) == specIDs)
            
            if np.sum(photmask) == 0:
                continue
            assert np.sum(photmask) == 1, "There is more than one ID match."
            
            z = redshifts[photmask].values[0]

            hdudata = hdu.data
            spectrum = np.array([hdudata.field("lambda"), hdudata.field("flux")]).T
            if restframe:
                spectrum = blueshift(spectrum, z)            
            spectrum = resample_and_integrate(spectrum, Lmin, Lmax, dL,
                                              resamp_prec=resamp_prec)
            
            template_clean[hdu.name.strip()] = spectrum[:, 1]
        t1 = time.time() - t0        
        print("File %s done in %.1f seconds!" % (os.path.basename(specname), t1))
        
    outdata = pd.DataFrame.from_dict(template_clean)
    # Reordering columns to put wavelength first
    cols = outdata.columns.values.tolist()
    cols.remove('lambda')
    cols = ['lambda'] + cols
    outdata = outdata[cols]
    
    outdata.to_csv(outpath, index=False)
            
    return None


if __name__ == "__main__":
    photfile = "/Users/brunomor/lib/python/dedale_d51/data/2016-06-22_cosmossnap_photometry.out"
    
    # Folder where FITS spectra can be found
    specfolder = "/Users/brunomor/lib/python/dedale_d51/data/2018-03-19_euclid_cosmossnap_spec/" 
    
    # Euclid TIPS values
    Lmin = 1253.2
    Lmax = 18592.8
    dL = 13.4
    Lmax_cosmossnap = 40200
    zmax = (Lmax_cosmossnap/Lmax - 1)

    # Output path *specific for Darth Fader templates for Euclid training*
    outpath = "/Users/brunomor/lib/python/dedale_d51/data/2018-03-25_euclid_tips_df_training_eigentemplates.csv" 

    main(photfile, specfolder, Lmin, Lmax, dL, zmax=zmax, resamp_prec=100, restframe=True,
         subsample_fraction=1.0, outpath=outpath)

