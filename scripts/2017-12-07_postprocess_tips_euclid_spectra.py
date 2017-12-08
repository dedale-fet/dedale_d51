from __future__ import division, print_function
import numpy as np
import sys
import os
import glob
import re
from astropy.io import fits
from astropy.table import Table


def main(specfolder, outname):
    # Create list of all individual TIPS spectra in folder
    flist = glob.glob(os.path.join(specfolder, "*.fits"))
    flist.sort()

    # Process
    outspec = Table()

    for i, fname in enumerate(flist):
        spec_id = re.findall("\d+", fname)[-1]
        tips_spec = fits.getdata(fname)

        # Get common wavelength values from first file only
        if i == 0:
            outspec["lambda"] = tips_spec.field("wave")
        else:
            assert np.all(outspec["lambda"] == tips_spec.field("wave")), (
                "File %s does not share same wavelength values as others."
                % fname)

        # Do not save spectra where TIPS returns all NaNs for some reason
        tips_failed = bool(np.isnan(tips_spec.field("flux")).all())
        if tips_failed:
            continue
        
        outspec[spec_id] = tips_spec.field("flux")

    outpath = os.path.join("../data", outname)
    outspec.write(outpath, format="csv", overwrite=True)

    return None


if __name__ == '__main__':
    # Examples from Bruno's laptop. Create an argparser later
    #specfolder = "/Users/brunomor/Desktop/temp_work/2017-12-08_Dedale_temp"
    #outname = "euclid_tips_spectra_wide.csv"
    specfolder = sys.argv[1]
    outname = sys.argv[2]

    main(specfolder, outname)