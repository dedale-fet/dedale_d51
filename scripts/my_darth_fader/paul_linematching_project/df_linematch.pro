function df_linematch, inpeaks, linepix, linenames, delpix, thresh = thresh, keep_all=keep_all

nlinestomatch = n_elements(linepix)
npeaks = n_elements(inpeaks)

if not keyword_set(thresh) then if not keyword_set(keep_all) then thresh = 10
if keyword_set(keep_all) then thresh = 5000

name = []
distance = []

if npeaks lt nlinestomatch then begin
   
   for i = 0, npeaks - 1 do begin
      
      diff = inpeaks[i]-(linepix+delpix)
      idx = where(abs(diff) eq min(abs(diff)))

      if n_elements(idx) eq 1 then begin
         if abs(diff[idx]) lt thresh then begin
            name = [name, linenames[idx]]
            distance = [distance, diff[idx]]
         endif
      endif else begin
         tt=where(abs(diff[idx]) lt thresh)
         name = [name,linenames[idx[tt]]]
         distance = [distance, diff[idx[tt]]]
      endelse
      
;   stop
      
      ;; now remove any duplicates
      
   endfor
   ;stop
   if n_elements(name) eq 0 then begin
      matches={name:0, distance:0}
      goto,fin
   endif
   sortind = sort(name)
   uniqind = uniq(name[sortind])
   namefin=strarr(n_elements(uniqind))
   distfin = intarr(n_elements(uniqind))
   if n_elements(name) gt n_elements(uniq(name)) then begin
      incl=[]
      for j = 0, n_elements(uniqind)-1 do begin
         dumind=sortind[uniqind[j]]
         bestind=dumind
         distbest = distance[dumind]
                                ;print,name[dumind],distance[dumind]
         for k = 0, n_elements(name) - 1 do begin
                                ;print,k,dumind
            if k eq dumind then goto,skip
            if strmatch(name[dumind], name[k]) then begin
                                ;print,'distance dumind', distance[dumind]
                                ;print,'distance k', distance[k]
           if abs(distbest) gt abs(distance[k]) then begin
                                ;  print,'k distance shorter'
              bestind = k
              distbest = distance[k]
           endif 
        endif
            skip:
         endfor
         namefin[j] = name[bestind]
         distfin[j] = distance[bestind]
      endfor
                                ; stop
      name=namefin
      distance=distfin
   endif
;stop

endif else begin

   indpk = []
   for i = 0, nlinestomatch - 1 do begin
      
      diff = inpeaks-(linepix[i]+delpix)
      idx = where(abs(diff) eq min(abs(diff)))
      
      if n_elements(idx) eq 1 then begin
         if abs(diff[idx]) lt thresh then begin
            distance = [distance, diff[idx]]
            name = [name,linenames[i]]
            indpk = [indpk,idx]
         endif
      endif else begin
         tt=where(abs(diff[idx]) lt thresh)
         name = [name,replicate(linenames[i],n_elements(tt))]
         distance = [distance, diff[idx[tt]]]
         indpk = [indpk,idx[tt]]
      endelse
   endfor

;; still need uniqueness here

   if n_elements(indpk) eq 0 then begin
      matches={name:0, distance:0}
      goto,fin
   endif
   sortind = sort(indpk)
   uniqind = uniq(indpk[sortind])
   namefin=strarr(n_elements(uniqind))
   distfin = intarr(n_elements(uniqind))
   if n_elements(indpk) gt n_elements(uniq(indpk)) then begin
      incl=[]
      for j = 0, n_elements(uniqind)-1 do begin
         dumind=sortind[uniqind[j]]
         bestind=dumind
         distbest = distance[dumind]
                                ;print,name[dumind],distance[dumind]
         for k = 0, n_elements(indpk) - 1 do begin
                                ;print,k,dumind
            if k eq dumind then goto,skip2
            if indpk[dumind] eq indpk[k] then begin
                                
               if abs(distbest) gt abs(distance[k]) then begin
                  
                  bestind = k
                  distbest = distance[k]
               endif 
            endif
            skip2:
         endfor
         namefin[j] = name[bestind]
         distfin[j] = distance[bestind]
      endfor
                                ; stop
      name=namefin
      distance=distfin
   endif
   
   
endelse

matches={name:name, distance:distance}    
fin: 
return, matches
end
