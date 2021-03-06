
 
pro darth_fader_wrapper, Res
;; Read inputs from df_input_params
;ins=df_input_params_Saclay_reference_run()
;ins=df_input_2018_Saclay_production_runs()
ins=df_input_2018_euclid_wide()
;; read in catalogue of true redshifts for comparison 
;z_true = readfits(ins.indir +'/ztrue_saclay.fits.gz')
;vs =size(z_true)
;NbrGal = vs[1]

;; run Darth Fader
darth_fader, DecSpectra, Templates, z_estimated, cleancat, /verbose,  Data=Data, Training=Training,  TnoBaseline=TnoBaseline
;plothist,z_true-z_estimated,bin=0.002
;stop
;; plot results of redshift estimation
;;;;window, 0, title = 'Before cleaning'
;;;;plot, z_true, z_estimated, psym = 5, xrange = [0,1.5], yrange = [0,1.5], xtitle = 'True redshift', $
;;;;      ytitle = 'Estimated redshift'

;; Compare results to input data. Catastrophic failures are redshift
;; estimates that lie outside of z_true +/- 0.005*(1+z_true)
print, "Successfully came back to example_darth_fader" 
;diff = abs(z_true - z_estimated)

;idx = where(diff le 0.005*(1+z_true), count)

;print, '% of catastrophic failures before cleaning = ', (1 - double(count)/double(NbrGal))*100.

;; Compare results of the cleaned catalogue, using the same criterion
;; as above  
;;;;window, 1, title = 'After cleaning'
;;;;plot, z_true[cleancat.indices], cleancat.redshifts, psym = 5, xrange = [0,1.5], yrange = [0,1.5], $
;;;;      xtitle = 'True redshift', ytitle = 'Estimated redshift'

nretained = n_elements(cleancat.indices)

print, '% of galaxies retained after cleaning = ', double(nretained)/double(NbrGal)*100.
;idx = where(diff[cleancat.indices] le 0.005*(1+z_true[cleancat.indices]), count2)
;print, '% of catastrophic failures after cleaning = ', (1 - double(count2)/double(nretained))*100.

;; Return a structure containing the results, if required
;Res = {DecSpectra: DecSpectra, Templates: Templates, Estred: z_estimated, cleancat: cleancat,  z_true: z_true, NbrGal: NbrGal, nretained: nretained, $
;        Data:Data, Training:Training}
;print, "Returned structure as it should."
return
end
