from __future__ import division, print_function
import sys
import glob
import subprocess
import os

# Getting input variables
try:
    nblocks = int(sys.argv[1])
    blockid = int(sys.argv[2]) 
except ValueError:
    raise IOError("Input nblocks and blockid must be integers.")

# Initialise variables
flist = glob.glob("/share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2017-08-25_euclid_Nice_run_individual_spectra_for_TIPS_1/*fits")
assert len(flist) > 0, "No files correspond to your selection of spectra."
flist.sort()
config = "/share/splinter/moraes/Dedale_Project/2017-08-24_TIPS_tests_2/TIPS_files_to_splinter/mpdr_conf_spe.fits"
#nexp = 4 # Euclid Wide
nexp = 20 # Euclid Deep
outdir = "/state/partition1/moraes/2017-08-26_tips_output/"

# Create output folder
try:
    os.makedirs("/state/partition1/moraes/2017-08-26_tips_output/")
except OSError as err:
    print("Folder already exists, moving forward...")

# Define and select block from file list
blocksize = len(flist)//nblocks
fileblock = flist[blockid*blocksize:(blockid+1)*blocksize]

print("Processing %d spectra from block %d out of %d total blocks" % (len(fileblock), blockid, nblocks))

# Setup arguments for subprocess call
callargs = ["time",
            "python",
            "/share/splinter/moraes/REPOSITORIES/euclid/tips/tips/scripts/mk_spc_1d.py"]
prepend_idx = len(callargs)
callargs.extend(("1.5 %d 1.2 %s %s" % (nexp, config, outdir)).split())

for fname in fileblock:
    callargs.insert(prepend_idx, fname)
    subprocess.call(callargs)
    del callargs[prepend_idx]
    print("Finished file %s" % os.path.basename(fname))
