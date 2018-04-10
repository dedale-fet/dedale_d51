"""Issues to fix:
- Write function to create Darth Fader df_input_param.pro file
"""

import numpy as np
import pandas as pd
import os
from astropy.io import fits


def save_spectra_df_format(fluxes, filepath, saveIDs=False, subsample=None):
    if not isinstance(fluxes, pd.DataFrame):
        raise TypeError("Fluxes must be a pandas dataframe")

    if subsample is not None:
        if not (isinstance(subsample, (float, int)) and (0 < subsample < 1)):
            raise TypeError("subsample must be a real number between 0 and 1 [fraction of subsample].")
        nspecs = fluxes.as_matrix().shape[1]
        keep = np.random.choice(nspecs, size=int(subsample*nspecs), replace=False)
        fluxes = fluxes.iloc[:, keep]

    specIDs = fluxes.columns.values.astype("int")
    if saveIDs:
        basename_noext = os.path.basename(filepath).split(".")
        specID_basename = basename_noext[0] + "_specIDs.txt"
        specID_path = os.path.join(os.path.dirname(filepath), specID_basename)
        np.savetxt(specID_path, specIDs, fmt='%s')

    fluxdata = fluxes.as_matrix()
    hdu = fits.PrimaryHDU()
    hdu.data = fluxdata.T
    hdu.writeto(filepath, overwrite=True)

    return specIDs


def save_errorcurve_df_format(errorcurve, filepath):
    out_error = fits.HDUList()
    out_error.append(fits.ImageHDU())
    out_error[0].data = errorcurve
    try:
        out_error.writeto(filepath, overwrite=True)
    except IOError as e:
        raise IOError("Could not save file, check path", "Error raised: %s" % e.args[0])

    return None


def save_ztrue_df_format(z, filepath):
    out_ztrue = fits.PrimaryHDU()
    out_ztrue.data = z
    try:
        out_ztrue.writeto(filepath, overwrite=True)
    except IOError as e:
        raise IOError("Could not save file, check path", "Error raised: %s" % e.args[0])

    return None


def get_lstep(wavelengths):
    logsteps = np.log10(wavelengths[1:]) - np.log10(wavelengths[:-1])
    try:
        lstep = float(np.unique(logsteps.round(decimals=10)))
    except TypeError as e:
        raise TypeError("Logarithmic binning lstep is not unique", "Error raised: %s" % e.args[0])

    return lstep
