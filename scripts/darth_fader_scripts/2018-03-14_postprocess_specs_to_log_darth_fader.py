import numpy as np
from dedale_d51.src.spectres import spectres
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
from itertools import takewhile


def read_cosmossnap_photometry_file(filename):
    # Get column names from header
    with open(filename, 'r') as fobj:
        headiter = takewhile(lambda s: s.startswith('#'), fobj)
        colnames = [elem.split()[2] for elem in headiter]
    # Open with pandas
    photometry = pd.read_csv(filename, delim_whitespace=True, comment="#", names=colnames)
    return photometry


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
    
    # 1) Read the necessary data and perform sanity checks
    specs = pd.read_csv(specpath) # TIPS noisy spectra
    clean_specs = pd.read_csv(trainpath)
    noise = fits.getdata(noisepath) # Flat noise model simulated with TIPS
    if cosmossnap_phot:
        photometry = read_cosmossnap_photometry_file(photpath)
    else:
        photometry = pd.read_csv(photpath)
    ztrue = photometry["redshift"].as_matrix()
    
    wavs_lin = specs["lambda"].as_matrix()
    flux = specs.drop(["lambda"], axis=1).as_matrix()
    errorcurve = noise["error"]

    assert np.allclose(noise["wave"], wavs_lin), "Noise and spectra should have the same wavelengths."
    assert len(ztrue) == flux.shape[1], "Redshifts and spectra should have the same length."

    # 2) Resampling operations
    # Resample clean training spectrum
    # Resample test spectra and corresponding noise
    # Empirical correction to noise
    ###
    # Preprocess and feed to resampling
    lmin = wavs_lin.min()
    lmax = wavs_lin.max()
    nbins = len(wavs_lin)
    dl = (lmax - lmin)/nbins
    wavs_log = np.logspace(np.log10(lmin + 5*dl), np.log10(lmax - 5*dl), nbins-100)
    errors = np.tile(errorcurve, (specs.shape[1], 1)).T
    spec_resampled, noise_resampled = spectres(wavs_lin, flux, wavs_log, spec_errs=errors)
    
    empirical_errorcurve = errorcurve - 2.5e-23*wavs_lin - 5e-20 # Empirical correction to fix wiggles
    # XXX - Process the training spec somewhere before here. Copy-paste from 2016-10-06 notebook.
    ###
    
    # 3) Create true redshift file that Darth Fader uses
    ###
    ###
    
    # 4) Transform to Darth Fader format and save
    ###
    ## Create errorcurve and save
    errorcurve = fits.HDUList()
    errorcurve.append(fits.ImageHDU())
    errorcurve[0].data = empirical_errorcurve
    errorcurve.writeto("../data/darth_fader/2018-03-13_euclid_wide/errorcurve_euclid_wide.fits.gz")
    ###
    
    # 5) Create Darth Fader df_input_param.pro file
    ###
    
    # 6) Plot some examples if wanted
    ###
    if plots:
        plt.plot(wavs_log, noise_resampled[:, 1340], "C2")
        plt.plot(wavs_lin, errorcurve)
        plt.plot(wavs_lin, empirical_errorcurve) 
        plt.show()

        plt.plot(wavs_lin, specs[:, 1340])
        plt.plot(wavs_log, spec_resampled[:, 1340], lw=2)
        plt.show()
    ###
    
    return None

if __name__ == "__main__":
    
    training_specpath = "/Users/brunomor/lib/python/dedale_d51/data/2018-03-25_euclid_tips_df_training_eigentemplates.csv"
    incat_specpath = "/Users/brunomor/lib/python/dedale_d51/data/2018-01-04_Euclid_tips_spectra_wide_matched.csv"
    rmscurve_path = "/Users/brunomor/Work/Dedale/data/euclid_simulations/2017-02-10_euclid_dedale_meeting_run/2017-02-10_TIPS_results/2017-02-14_euclid_noise_sim_tests/flat_spectrum_1-18_noise_wide.fits"
    photpath = "/Users/brunomor/lib/python/dedale_d51/data/2018-01-04_Euclid_photometry_matched2tips.csv" # To get true redshifts
    
    main(training_specpath, incat_specpath, rmscurve_path, photpath)
