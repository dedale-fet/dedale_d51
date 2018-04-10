"""Issues to fix:
- Write an argparser
- Take details of resampling spectra into a function
- Discuss with Sam how to redesign this code for the milestone release
- Add docstrings to everything
"""

import numpy as np
import pandas as pd
from astropy.io import fits
from itertools import takewhile
import os

from dedale_d51.src.spectres import spectres
from dedale_d51.src.cosmossnap_utils import read_cosmossnap_photometry_file
from dedale_d51.src import darth_fader_utils as dfu


def main(trainpath, specpath, noisepath, photpath, cosmossnap_phot=False, plots=False):
    """Process the Euclid data to be run with Darth Fader

    List of steps:
        - Create the noisy testing spectra in log binning on which Darth Fader measures redshifts
        - Create clean training spectra in log binning which Darth Fader uses to learn the eigentemplates
        - Create errorcurve in log binning
        - I don't know what is componentcat, use an existing one.
        - Create true redshift reference file which Darth Fader uses [for what?]
        - [Optional] Create the df_input.pro file here.
    """

    # 1) Read the data and perform sanity checks
    specs = pd.read_csv(specpath) # TIPS noisy spectra
    train_specs = pd.read_csv(trainpath)
    noise = fits.getdata(noisepath) # Flat noise model simulated with TIPS
    if cosmossnap_phot:
        photometry = read_cosmossnap_photometry_file(photpath)
    else:
        photometry = pd.read_csv(photpath)
    ztrue = photometry["redshift"]

    wavs_lin = specs["lambda"].as_matrix()
    flux = specs.drop(["lambda"], axis=1).as_matrix()
    specIDs = specs.columns.values[1:].tolist()
    errorcurve = noise["error"]

    wavs_lin_train = train_specs["lambda"].as_matrix()
    flux_train = train_specs.drop(["lambda"], axis=1).as_matrix()
    specIDs_train = train_specs.columns.values[1:].tolist()

    assert np.allclose(noise["wave"], wavs_lin), "Noise and spectra should have the same wavelengths."
    assert len(ztrue) == flux.shape[1], "Redshifts and spectra should have the same length."

    # 2) Resample observed spectra and errorcurves
    lmin = wavs_lin.min()
    lmax = wavs_lin.max()
    nbins = len(wavs_lin)
    dl = (lmax - lmin)/nbins
    wavs_log = np.logspace(np.log10(lmin + 5*dl), np.log10(lmax - 5*dl), nbins-100) # FIXME - Massaging by hand because of the spectres code.

    errors = np.tile(errorcurve, (flux.shape[1], 1)).T
    spec_resampled, noise_resampled = spectres(wavs_lin, flux, wavs_log, spec_errs=errors)
    spec_resampled = pd.DataFrame(data=spec_resampled, columns=specIDs)

    empirical_errorcurve = errorcurve - 2.5e-23*wavs_lin - 5e-20 # Empirical correction to fix wiggles

    # 3) Resample training spectra
    lmin_train = wavs_lin_train.min()
    lmax_train = wavs_lin_train.max()
    assert lmin_train < wavs_log.min()/(1 + ztrue.max()), "Training min wavelength is too big."
    assert lmax_train >= wavs_log.max(), "Training max wavelength is too small."
    
    lstep = dfu.get_lstep(wavs_log)
        
    wavs_log_train = 10**np.arange(np.log10(lmin_train), np.log10(lmax_train), lstep)
    # Cropping training log to avoid problems with how spectres deals with the binning
    wavs_log_train = wavs_log_train[3:-1] 
    assert wavs_log_train.max() >= wavs_log.max(), "Logbinned training max wavelength became too small."
    
    spec_train_resampled = spectres(wavs_lin_train, flux_train, wavs_log_train)
    spec_train_resampled = pd.DataFrame(data=spec_train_resampled, columns=specIDs_train)
    
    # 4) Transform to Darth Fader format and save
    dfu.save_spectra_df_format(spec_train_resampled, "/Users/brunomor/lib/python/dedale_d51/data/darth_fader/2018-03-29_euclid_wide/2018-03-29_training_tips.fits.gz", saveIDs=False, subsample=0.02)
    specIds_test_out = dfu.save_spectra_df_format(spec_resampled, "/Users/brunomor/lib/python/dedale_d51/data/darth_fader/2018-03-29_euclid_wide/2018-03-29_testing_tips.fits.gz", saveIDs=True, subsample=0.01)
    dfu.save_errorcurve_df_format(empirical_errorcurve, "/Users/brunomor/lib/python/dedale_d51/data/darth_fader/2018-03-29_euclid_wide/2018-03-29_errorcurve_tips_1e18.fits.gz")

    ztrue_test_out = ztrue[photometry['Id'].isin(specIds_test_out)]
    assert len(ztrue_test_out) == len(specIds_test_out), "Redshifts and IDs do not have the same length."
    dfu.save_ztrue_df_format(ztrue_test_out, "/Users/brunomor/lib/python/dedale_d51/data/darth_fader/2018-03-29_euclid_wide/2018-03-29_ztrue.fits.gz")

    return None

#-------------

if __name__ == "__main__":
    
    training_specpath = "/Users/brunomor/lib/python/dedale_d51/data/2018-03-25_euclid_tips_df_training_eigentemplates.csv"
    incat_specpath = "/Users/brunomor/lib/python/dedale_d51/data/2018-01-04_Euclid_tips_spectra_wide_matched.csv"
    rmscurve_path = "/Users/brunomor/Work/Dedale/data/euclid_simulations/2017-02-10_euclid_dedale_meeting_run/2017-02-10_TIPS_results/2017-02-14_euclid_noise_sim_tests/flat_spectrum_1-18_noise_wide.fits"
    photpath = "/Users/brunomor/lib/python/dedale_d51/data/2018-01-04_Euclid_photometry_matched2tips.csv" # To get true redshifts
    
    main(training_specpath, incat_specpath, rmscurve_path, photpath)
