#!/bin/tcsh -f
#PBS -N euclid_cosmossnap
#PBS -l nodes=1:ppn=1
#PBS -q compute
#PBS -t 1-58
#PBS -o /home/moraes/qsub_logs/
#PBS -j oe
#PBS -S /bin/tcsh

cd $PBS_O_WORKDIR
source /etc/profile.d/modules.csh
module load dev_tools/oct2017/python-Anaconda-3-5.0.0.1

echo Working directory is $PBS_O_WORKDIR
echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo This jobs runs on the following processors:
echo `cat $PBS_NODEFILE`

@ FILEID = ( ${PBS_ARRAYID} - 1 )
python /share/splinter/moraes/REPOSITORIES/dedale_d51/scripts/2018-03-19_make_euclid_spectroscopy.py /share/data1/moraes/Dedale_Project/2016-06-13_simulated_catalogs/2016-09-06_euclid_run/2016-09-06_euclid_run_spectra_spec_${FILEID}.fits
