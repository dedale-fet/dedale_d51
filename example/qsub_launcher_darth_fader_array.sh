#!/bin/tcsh -f
#PBS -N Darth_Fader
#PBS -l nodes=1:ppn=1
#PBS -q compute
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

# From Paul's IDL configuration
alias idl /share/apps/itt/idl/idl80/bin/idl

# # From /home/cosmos/SourceBinPaths, for IDL stuff
setenv ISAP /home/cosmos/library_src/ISAP
setenv PATH ${PATH}:/home/cosmos/library_src/ISAP/bin

# For idutils and kcorrect
setenv IDLUTILS_DIR /home/cosmos/library_src/idlutils
setenv PATH ${PATH}:$IDLUTILS_DIR/bin
setenv KCORRECT_DIR /home/cosmos/library_src/kcorrect
setenv PATH ${PATH}:${KCORRECT_DIR}/bin

alias isap "idl $ISAP/idl/isap.pro"

echo Working directory is $PBS_O_WORKDIR
echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo This jobs runs on the following processors:
echo `cat $PBS_NODEFILE`

set DF_COMMANDS = ".compile $INPUTPATH\n.compile $DF_PATH\ndarth_fader, DecSpectra, Templates, z_estimated, cleancat,  altindir=$GALDIR, altincat=$INCATBASE, altoutdir=$GALDIR, /verbose,  Data=Data, Training=Training,  TnoBaseline=TnoBaseline, altzcat=$ZCAT"

echo $DF_COMMANDS | isap
#echo $DF_COMMANDS

echo Job is done
echo Time is `date`
