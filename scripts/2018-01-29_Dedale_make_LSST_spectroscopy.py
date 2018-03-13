from __future__ import division, print_function
import numpy as np
import glob
import os
import sys
import pandas as pd
from astropy.io import fits

def main(specname, lsst):

    if not os.path.exists("/share/splinter/moraes/REPOSITORIES/dedale_d5.1/data/lsst_cosmossnap_spec/"):
        os.mkdir("/share/splinter/moraes/REPOSITORIES/dedale_d5.1/data/lsst_cosmossnap_spec/")

    # Open LSST table and get SpcExt IDs
    lsst_specIDs = pd.read_csv(lsst, usecols=["Id"]).values.flatten().tolist()

    print("Processing %s" % os.path.basename(specname))

    file_digit_id = int(os.path.basename(specname).split("_")[-1].split(".")[0])

    # Create new list for HDUs
    lsst_hdus = []
    lsst_hdus.append(fits.PrimaryHDU())

    # Open FITS file
    hdulist = fits.open(specname)
    for hdu in hdulist[1:]:
        specID = int(hdu.name)
        if specID in lsst_specIDs:
            lsst_hdus.append(hdu)
    
    new_hdulist = fits.HDUList(lsst_hdus)

    outname = ('/share/splinter/moraes/REPOSITORIES/dedale_d5.1/data/lsst_cosmossnap_spec/lsst_cosmossnap_spectra_%d.fits' % file_digit_id)
    new_hdulist.writeto(outname, overwrite=True)

    return None


if __name__ == "__main__":

    specname = sys.argv[1]
    lsst_photometry_path = "/share/splinter/moraes/REPOSITORIES/dedale_d5.1/data/2017-12-06_LSST_photometry.csv"

    main(specname, lsst_photometry_path)
