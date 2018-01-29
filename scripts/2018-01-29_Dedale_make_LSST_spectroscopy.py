from __future__ import division, print_function
import numpy as np
import glob
import os
import pandas as pd
from astropy.io import fits

def main(cosmossnap, lsst):

    if not os.path.exists("../data/lsst_cosmossnap_spec/"):
        os.mkdir("../data/lsst_cosmossnap_spec/")

    # Open LSST table and get SpcExt IDs
    lsst_specIDs = pd.read_csv(lsst, usecols=["Id"]).values.flatten().tolist()

    for specname in cosmossnap:
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

        outname = ('../data/lsst_cosmossnap_spec/lsst_cosmossnap_spectra_%d.fits' % file_digit_id)
        new_hdulist.writeto(outname, overwrite=True)

    return None


if __name__ == "__main__":

    cosmossnap_specfiles = glob.glob("/share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_*fits")
    cosmossnap_specfiles.sort()

    lsst_photometry_path = "../data/2017-12-06_LSST_photometry.csv"

    main(cosmossnap_specfiles, lsst_photometry_path)
