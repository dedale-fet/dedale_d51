#!/usr/bin/python

from __future__ import division, print_function
import os
import glob

outdir = "/share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2017-08-25_euclid_Nice_run_individual_spectra_for_TIPS_1/"

for filenumber in range(58):
    jobname = "COSMOSSNAP_TO_TIPS_" + str(filenumber)
    # Construct string that will be written to the batch file
    textlist = ["#!/bin/tcsh -f",
                "#PBS -N " + jobname,
                "#PBS -l nodes=1:ppn=1",
                "#PBS -q compute",
                "#PBS -o /home/moraes/qsub_logs/",
                "#PBS -j oe",
                "#PBS -S /bin/tcsh", "",
                "cd $PBS_O_WORKDIR",
                "source /etc/profile.d/modules.csh",
		"module load versioning/apr2017/git-2.9.3",
		"module load dev_tools/oct2016/cmake-3.7.0-rc2",
		"module load dev_tools/apr2017/gcc-6.3.0",
		"module load dev_tools/oct2016/boost-1.62.0",
		"module load dev_tools/nov2014/make-4.1",
		"module load dev_tools/oct2016/python-Anaconda-2-4.2.0",
		"module load science/oct2016/gsl-2.2.1",
		"module load fft/may2017/fftw-3.3.6",
		"module load astro/nov2016/wcslib-5.15",
		"module load astro/aug2017/tips-a62a0631", "",
                "echo Working directory is $PBS_O_WORKDIR",
                "echo Running on host `hostname`",
                "echo Time is `date`",
                "echo Directory is `pwd`",
                "echo This jobs runs on the following processors:",
                "echo `cat $PBS_NODEFILE`", ""]

    textlist.append("time python /share/splinter/moraes/Dedale_Project/process_cosmossnap_to_tips.py /share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_euclid_run_spectra_%d.out /share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_euclid_run_spectra_spec_%d.fits %s" % (filenumber, filenumber, outdir))

    batchtext = "\n".join(textlist)
    batchtext += "\n"

    # Save string to new shell file
    filename = ("qsub_launcher_" + jobname + ".sh")
    with open(filename, 'w') as batch:
        batch.write(batchtext)
    # Launch qsub job and erase batch file
    os.system("qsub " + filename)
    os.system("sleep 0.1")
    os.system("rm " + filename)

#--------------------------------------------------------------------

