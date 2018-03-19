from __future__ import division, print_function
import numpy as np
import glob
import os
import sys
import pandas as pd
from astropy.io import fits

def main(specname, euclid):

    if not os.path.exists("/share/splinter/moraes/REPOSITORIES/dedale_d51/data/euclid_cosmossnap_spec/"):
        os.mkdir("/share/splinter/moraes/REPOSITORIES/dedale_d51/data/euclid_cosmossnap_spec/")

    # Open euclid table and get SpcExt IDs
    euclid_specIDs = pd.read_csv(euclid, usecols=["Id"]).values.flatten().tolist()

    print("Processing %s" % os.path.basename(specname))

    file_digit_id = int(os.path.basename(specname).split("_")[-1].split(".")[0])

    # Create new list for HDUs
    euclid_hdus = []
    euclid_hdus.append(fits.PrimaryHDU())

    # Open FITS file
    hdulist = fits.open(specname)
    for hdu in hdulist[1:]:
        specID = int(hdu.name)
        if specID in euclid_specIDs:
            euclid_hdus.append(hdu)
    
    new_hdulist = fits.HDUList(euclid_hdus)

    outname = ('/share/splinter/moraes/REPOSITORIES/dedale_d5.1/data/euclid_cosmossnap_spec/euclid_cosmossnap_spectra_%d.fits' % file_digit_id)
    new_hdulist.writeto(outname, overwrite=True)

    return None


if __name__ == "__main__":
    """Running example:
    python 2018-03-19_make_euclid_spectroscopy.py /share/data1/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_euclid_run_spectra_spec_40.fits
    """
    
    specname = sys.argv[1]
    euclid_photometry_path = "/share/splinter/moraes/REPOSITORIES/dedale_d51/data/2018-01-04_Euclid_photometry_matched2tips.csv"

    main(specname, euclid_photometry_path)
