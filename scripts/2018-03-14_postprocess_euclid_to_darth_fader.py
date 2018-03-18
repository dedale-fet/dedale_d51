import numpy as np
from spectres import spectres
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits

def main(specpath, noisepath, plots=False):
    """Process the Euclid data to be run with Darth Fader
    
    List of steps:
        - Create the noisy testing spectra in log binning on which Darth Fader measures redshifts
        - Create clean training spectra in log binning which Darth Fader uses to learn the eigentemplates
        - Create errorcurve in log binning
        - I don't know what is componentcat, use an existing one.
        - Create true redshift reference file which Darth Fader uses [for what?]
        - [Optional] Create the df_input.pro file here.
    """
    # Read data
    
    ## XXX - Need to import more data, including clean Euclid spectra for template learning
    specs = pd.read_csv(specpath)
    noise = fits.getdata(noisepath)
    wavs_lin = wide["lambda"].as_matrix()
    specs = wide.drop(["lambda"], axis=1).as_matrix()

    assert np.allclose(noise["wave"], wavs_lin), "Noise and spectra wavelengths not compatible."
    errorcurve = noise["error"]
    
    # Preprocess and feed to resampling
    lmin = wavs_lin.min()
    lmax = wavs_lin.max()
    nbins = len(wavs_lin)
    dl = (lmax - lmin)/nbins
    wavs_log = np.logspace(np.log10(lmin + 5*dl), np.log10(lmax - 5*dl), nbins-100)
    errors = np.tile(errorcurve, (specs.shape[1], 1)).T
    spec_resampled, noise_resampled = spectres(wavs_lin, specs, wavs_log, spec_errs=errors)
    
    empirical_errorcurve = errorcurve - 2.5e-23*wavs_lin - 5e-20 # Empirical correction to fix wiggles
    
    # XXX - Process the training spec somewhere before here. Copy-paste from 2016-10-06 notebook.
    
    if plots:
        plt.plot(wavs_log, noise_resampled[:, 1340], "C2")
        plt.plot(wavs_lin, errorcurve)
        plt.plot(wavs_lin, empirical_errorcurve) 
        plt.show()

        plt.plot(wavs_lin, specs[:, 1340])
        plt.plot(wavs_log, spec_resampled[:, 1340], lw=2)
        plt.show()    
    
    # Transform to Darth Fader format
    ## Create errorcurve and save
    errorcurve = fits.HDUList()
    errorcurve.append(fits.ImageHDU())
    errorcurve[0].data = empirical_errorcurve
    errorcurve.writeto("../data/darth_fader/2018-03-13_euclid_wide/errorcurve_euclid_wide.fits.gz")
    
    ## Create trainign
    return None

if __name__ == "__main__":
    
    specpath = "../data/2018-01-04_Euclid_tips_spectra_wide_matched.csv"
    noisepath = "/Users/brunomor/Work/Dedale/data/euclid_simulations/2017-02-10_euclid_dedale_meeting_run/2017-02-10_TIPS_results/2017-02-14_euclid_noise_sim_tests/flat_spectrum_1-18_noise_wide.fits"
    
    main(specpath, noisepath)
