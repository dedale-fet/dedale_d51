#!/bin/tcsh -f
#PBS -N TIPS_spectra
#PBS -l nodes=1:ppn=1
#PBS -q compute
#PBS -t 1-250
#PBS -o /home/moraes/qsub_logs/
#PBS -j oe
#PBS -S /bin/tcsh

cd $PBS_O_WORKDIR
source /etc/profile.d/modules.csh
module load versioning/apr2017/git-2.9.3
module load dev_tools/oct2016/cmake-3.7.0-rc2
module load dev_tools/apr2017/gcc-6.3.0
module load dev_tools/oct2016/boost-1.62.0
module load dev_tools/nov2014/make-4.1
module load dev_tools/oct2016/python-Anaconda-2-4.2.0
module load science/oct2016/gsl-2.2.1
module load fft/may2017/fftw-3.3.6
module load astro/nov2016/wcslib-5.15
module load astro/aug2017/tips-a62a0631

echo Working directory is $PBS_O_WORKDIR
echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo This jobs runs on the following processors:
echo `cat $PBS_NODEFILE`

@ BLOCKID = ( ${PBS_ARRAYID} - 1 )
time python run_tips_on_block.py 250 ${BLOCKID}
