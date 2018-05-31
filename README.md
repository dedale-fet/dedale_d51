# MS4 - Application to EUCLID data - Realistic galaxy simulations and redshift measurements [Change title later]

This repository contains a suite of tools to link astrophysical simulation codes, which are combined in a pipeline to generate galaxy photometry and spectroscopy representative of the expected quality of the Euclid Mission data. This simulated data set can be used to help develop and benchmark spectroscopic and photometric redshift estimation methods, and to assess whether their redshift accuracy meets the official Mission Requirements for successful cosmological measurements.

The software available in the repository includes:
   - List the functionality here
   - bla 1
   - bla 2

---
> Main Authors: **Bruno Moraes (UCL), Filipe Abdalla (UCL), whoelse**  
> Year: **2016-2018**   
> Corresponding Author: [b.moraes@ucl.ac.uk](mailto:b.moraes@ucl.ac.uk)
> Website: [https://github.com/dedale-fet](https://github.com/dedale-fet)

---

## Table of Contents
1. [Introduction](#intro)
    * [The need for simulations](#need4sims)
    * [The structure](#struct)
2. [Requirements](#requirements)
    * [COSMOSSNAP](#cosmossnap)
    * [TIPS](#tips)
    * [A cluster with PBS](#pbscluster)
3. [Example](#example)
    * [Generating a COSMOSSNAP data set](#step1)
    * [Preprocessing to TIPS](#step2)
    * [Generating spectra with TIPS](#step3)
    * [Postprocessing and final set generation](#step4)
    * [Measuring redshifts](#step5)

---

## <a name="intro"></a> Introduction

### <a name="need4sims"></a> The need for simulations
   - Truth table to test scientific pipeline analysis
   - We want realistic spectroscopic and photometric properties and types at the object level.
   - We want realistic population-level spectrophotometric properties.
   - Photometric properties
       - Galaxy population from the real-life COSMOS survey.
       - Forward-simulated fluxes with filters from current and upcoming surveys.
   - 

### <a name="struct"></a> The structure
    - COSMOSSNAP for the base spectro-photometric simulation
    - White gaussian noise 
    - TIPS for realistic Euclid slitless spectroscopy 

## <a name="requirements"></a> Requirements

### <a name="cosmossnap"></a> COSMOSSNAP
   - What is COSMOSSNAP.
   - How to install it.

### <a name="tips"></a> TIPS
   - What is TIPS.
   - How to install it.

### <a name="pbscluster"></a> A cluster with PBS nodes

## <a name="example"></a> Example: Euclid-like spectroscopic data