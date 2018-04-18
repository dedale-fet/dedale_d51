;+
; NAME:
;        df_input_params.pro
;
; PURPOSE:
;    Specifies the inputs for the Darth Fader pipeline
;
; INPUTS: 
;   *INDIR - directory containing the input test spectra, training set
;           and/or eigentemplates
;   *incat - name of FITS file containing test spectra
;   *trainingcat - name of FITS file containing training set to compute
;                 eigentemplates. If you have already computed these,
;                 set trainingcat=''
;   *rmscurve - the name of the FITS file containing your RMS error
;               curve(s) associated with the test spectra. For white
;               gaussian noise, set rmscurve = ''
;   *templatecat - name of FITS file containing eigentemplates. Set
;                  templatecat='' if you wish Darth Fader to compute
;                  these from a training set. NOTE: Either templatecat
;                  or trainingcat MUST be specified.
;
;   *lstep - logarithmic pixel scaling. Note: Spectra must be LOG-BINNED. 
;   *(optional) training_lmin, training_lmax, data_lmin, data_lmax -
;   the start and end wavelengths of the training spectra and test
;   spectra, used to compute shiftpar (see below). You may specify
;   shiftpar directly, if you choose
;   *shiftpar - this is the pixel difference between the end of the
;               template and the end of the test spectrum. If
;               training_lmax = data_lmax, this will be 0. 
;
;   *EstimRedshiftsFromNoisyData - set to 1 if you wish to use the
;                                  noisy data in the cross-correlation
;                                  step to estimate redshifts. This is
;                                  recommended for white gaussian
;                                  noise.
;   *ComputeEigentemplates - set to 0 if you have already computed
;                            eigentemplates from the training set and
;                            have specified templatecat
;   *nscale - number of scales in the denoising steps. Set to 0 to
;             compute automatically from the data
;   *EnergPercent - Darth Fader will retain all eigentemplates such
;                   that the total eigenvalue weight of the retained
;                   templates is greater than/equal to EnergPercent
;
;   *OUTDIR - existing directory in which to place the outputs of the
;             Darth Fader run
;   *OutputComponents, OutputTemplates, OutputRedshifts,
;   OutputCleanCatalogue - set to 1 to write these data to a
;                          file. Must specify the relevant filename. 
;
; OUTPUTS: 
;    Structure detailing input parameters, algorithm parameters and
;    output parameters, to be used by Darth Fader
; 
; HISTORY: 
;       Written: Adrienne Leonard, Oct 2013
;-

function df_input_params_florent

;; \\ INPUT FILES AND LOCATIONS //
INDIR = './2018-04-04_Florent_spec_data/df_format/'                      ; Input directory containing the spectra as FITS files
incat = '2018-04-04_testing.fits.gz' ; Must specify trainingcat or templatecat, the other may be specified as ''
trainingcat = '2018-04-04_training.fits.gz' ; Set rmscurve = '' for white gaussian nosie
rmscurve = '' ;'errorcurve.fits.gz'            
templatecat = '' ;'templates.fits'
componentcat = 'components.fits'
zcat = 'lsst_cosmossnap_spectra_testset_10000_truez.fits'

;; \\ INPUT DATA PARAMETERS //

lstep = double(2.170930e-04) ; logarithmic pixel scaling
training_lmin = 1250.234446                       ; training set min. wavelength in angstroms
training_lmax =  10499.200832              ; training set max. wavelength in angstroms
data_lmin = 3600.478232                       ; data min. wavelength in angstroms
data_lmax = 9799.353237                 ; data max. wavelength in angstroms
shiftpar = round((alog10(double(training_lmax)) - alog10(double(data_lmax)))/double(lstep)) ; pixel difference between the end of the 
                                            ;training set and the test data spectra

;; \\ ALGORITHM SPECIFICATIONS //

ComputeEigentemplates = 1       ; Set to 0 if you have already computed the eigentemplates (note: must then specify templatecat)
nscale = 6                      ; Number of scales used in the denoising steps. Set to 0 to compute this automatically from the data.
EnergPercent = 99.93            ; Darth Fader will retain all eigentemplates such that the total eigenvalue weight of the 
Ntemplates = 0                  ; retained templates is greater than/equal to EnergPercent. Specifying Ntemplates 
ComputeComponents = 1           ; forces a number of templates to be retained, and overrides EnergPercent
Gen2 = 0
regul = 0
EstRed = 1
EstimRedshiftFromNoisyData = 0  ; Set to 1 if you wish to use the noisy data for cross-correlation


FDR=3.                          ; Parameter used for the detection level of peaks in the wavelet space 
RegulParam=0.01                   ; Regularization parameter in the denoising
CleanCatalogue = 1              ; Set to 0 to skip the cleaning step
NpeakCrit = 6                   ; Peak counting criterion used in the cleaning
NsigmaPeak = 0.01
Linematch = 1                   ; Peaks detected in wavelet space, but with an amplitude smaller than NsigmaPeak * RMSnoise  
lines = ['OII_1','Break']       ; are rejected
matchtype = 'OR'
matchthresh = 10
linefile = 'lines.txt'


;; \\ OUTPUT SPECIFICATIONS //

OUTDIR = './df_output/'                   ; Directory in which to place the outputs of the Darth Fader Run
OutputComponents = 1            ; Output components of the spectra to a file? 1: Yes, 0: No
CompFileName = 'components.fits'
OutputTemplates = 0             ; Output relevant eigentemplates to a file? 1: Yes, 0: No
TempFileName = 'templates.fits'
OutputAllEigen = 0              ; Output all eigentemplates to a file? 1: Yes, 0: No
AllEigenName = 'alleigen.fits'
OutputRedshifts = 1             ; Output galaxy redshifts to a file? 1: Yes, 0: No
RedshiftFileName = 'redshifts_gen1.fits'
OutputCleanCatalogue = 1        ;Output clean catalogue to a file? 1: Yes, 0: No
CleanFileName = 'clean_catalogue.fits'

inp={indir:indir, $
     incat:incat, $
     trainingcat:trainingcat, $
     rmscurve:rmscurve, $
     templatecat:templatecat, $
     componentcat:componentcat, $
     zcat:zcat, $
     lstep:lstep, $
     training_lmin: training_lmin, $
     training_lmax: training_lmax, $
     data_lmin: data_lmin, $
     data_lmax: data_lmax, $
     shiftpar: shiftpar, $
     ComputeEigenTemplates:ComputeEigenTemplates, $
     nscale:nscale, $
     EnergPercent:Energpercent, $
     Ntemplates:Ntemplates, $
     ComputeComponents:ComputeComponents, $
     Gen2:Gen2, $
     regul:regul, $
     EstRed:EstRed, $
     EstimRedshiftFromNoisyData:EstimRedshiftFromNoisyData, $
     FDR: FDR, $
     RegulParam: RegulParam, $
     CleanCatalogue:CleanCatalogue, $
     NpeakCrit:NpeakCrit, $
     NsigmaPeak: NsigmaPeak, $
     LineMatch:LineMatch, $
     lines:lines, $
     matchtype:matchtype, $
     matchthresh:matchthresh, $
     linefile:linefile,$
     outdir:outdir, $
     outputComponents:OutputComponents, $
     CompFileName:CompFileName, $
     OutputTemplates:OutputTemplates, $
     TempFileName:TempFileName, $
     OutputAllEigen:OutputAllEigen, $
     AllEigenName:AllEigenName, $
     OutputRedshifts:OutputRedshifts, $
     RedshiftFileName:RedshiftFileName, $
     OutputCleanCatalogue:OutputCleanCatalogue, $
     CleanFileName:CleanFileName}

return,inp
end

