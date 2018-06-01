#!/bin/tcsh

set INPUTPATH = "/share/data1/moraes/Dedale_Project/Darth_Fader/2018-04-23_Florent_production_runs/2018-04-23_df_input_params"
set DF_PATH = "/share/splinter/moraes/REPOSITORIES/dedale_d51/scripts/my_darth_fader/darth_fader"

# Jobs to launch
foreach f ( /share/data1/moraes/Dedale_Project/Darth_Fader/2018-04-23_Florent_production_runs/df_format/GalTypeSB_SNR20/*IID*SNR20.fits )
    set suffix = ( $f:as/IID/ / )
    set zcat = "'zest$suffix[2]'"
    set catbase = `basename $f`
    set catbase = "'$catbase'"
    set interA = `echo $INPUTPATH | cut -f1-7 -d"/"`
    set interB = `echo $suffix[2] | cut -c2- | cut -f1 -d"."`
    set GALDIR = "'$interA/df_format/$interB/'"
    qsub -v INPUTPATH=$INPUTPATH,GALDIR=$GALDIR,DF_PATH=$DF_PATH,INCATBASE=$catbase,ZCAT=$zcat /home/moraes/qsub_launcher_darth_fader_array.sh
end
