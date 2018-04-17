"""Issues to fix:
- Write an argparser
"""

import numpy as np
import os
import errno
import pandas as pd

from dedale_d51.src import darth_fader_utils as dfu


def print_run_basic_info():

    return None


def main(outfolder):

    try:
        os.mkdir(outfolder)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

    # 1) Process training spectra
    specs_info = {}
    specs_info["training"] = {"specpath": os.path.join(infolder, "lsst_cosmossnap_spectra_restframe_training_set_10000.npy"),
                              "wavpath": os.path.join(infolder, "lsst_cosmossnap_spectra_restframe_training_set_wavelength.npy"),
                              "outpath": os.path.join(outfolder, "2018-04-04_training.fits.gz")}
    specs_info["testing_clean"] = {"specpath": os.path.join(infolder, "lsst_cosmossnap_spectra_testset_10000.npy"),
                                   "wavpath": os.path.join(infolder, "lsst_cosmossnap_spectra_testset_wavelength.npy"),
                                   "outpath": os.path.join(outfolder, "2018-04-04_testing.fits.gz")}

    for specset, specinfo in specs_info.items():
        print(specset)
        specs = np.load(specinfo["specpath"]).T # Transposing to more common ordering
        specs = pd.DataFrame(data=specs)
        filepath = os.path.join(outfolder, specinfo["outpath"])
        dfu.save_spectra_df_format(specs, filepath, saveIDs=False, subsample=0.1)

        wavs = np.load(specinfo["wavpath"])
        lstep = dfu.get_lstep(wavs)
        print("lmin = %f" % wavs.min())
        print("lmax = %f" % wavs.max())
        print("lstep = %e" % lstep)

    return None


if __name__ == "__main__":
    # Inputs
    infolder = "/Users/brunomor/lib/python/dedale_d51/data/darth_fader/2018-04-04_Florent_spec_data/download/"
    outfolder = "/Users/brunomor/lib/python/dedale_d51/data/darth_fader/2018-04-04_Florent_spec_data/df_format/"

    main(outfolder)
