#!/usr/bin/python

from __future__ import division, print_function
import os

for jobnumber, galmin in enumerate(range(1, 580000, 10000)):
    jobname = "COSMOSSNAP_" + str(jobnumber)
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
                "module load dev_tools/oct2015/python-Anaconda-2-4.0.0", "",
                "echo Working directory is $PBS_O_WORKDIR",
                "echo Running on host `hostname`",
                "echo Time is `date`",
                "echo Directory is `pwd`",
                "echo This jobs runs on the following processors:",
                "echo `cat $PBS_NODEFILE`"]

    galmax = galmin + 9999

    textlist.append("$COSMOSSNAPDIR/source/cosmossnap -c /share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_euclid_run.para -SNAP_OUT /share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_euclid_run_spectra_%d.out -STAR NO -AGN NO -SPECTRA_OUT /share/splinter/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_euclid_run_spectra_spec_%d.fits -SPECTRA_LAMBDA 1250,40200,5 -LINES_STARTEND %d,%d" % (jobnumber, jobnumber, galmin, galmax))

    batchtext = "\n".join(textlist)
    batchtext += "\n"

    # Save string to new shell file
    filename = ("qsub_launcher_" + jobname + ".sh")
    with open(filename, 'w') as batch:
        batch.write(batchtext)
    # Launch qsub job and erase batch file
    os.system("qsub " + filename)
    os.system("sleep 1")
    os.system("rm " + filename)

#--------------------------------------------------------------------

