# Application to Euclid data: spectroscopic and photometric galaxy simulations

This repository contains a suite of tools to link astrophysical simulation codes, which are combined in a pipeline to generate galaxy photometry and spectroscopy representative of the expected quality of the Euclid Mission data. This simulated data set can be used to help develop and benchmark spectroscopic and photometric redshift estimation methods, and to assess whether their redshift accuracy meets the official Mission Requirements for successful cosmological measurements.

<!---
The software available in the repository includes:
   - List the functionality here
   - bla 1
   - bla 2
--->

> Corresponding Author: **Bruno Moraes (University College London)**, [b.moraes@ucl.ac.uk](mailto:b.moraes@ucl.ac.uk)
>

## Table of Contents
1. [Introduction](#intro)
    * [Dark Energy and the Euclid satellite](#science)
    * [Spectroscopic and photometric redshifts](#specphot)
    * [Simulations need](#need4sims)
    <!--- * [The structure](#struct) --->
2. [Requirements](#requirements)
    * [Basic Python dependencies](#basic)
    * [COSMOSSNAP](#cosmossnap)
    * [TIPS](#tips)
    * [ISAP](#isap)
    * [A PBS cluster](#pbscluster)
3. [Getting Started](#start)
3. [Example](#example)
    * [Generating a COSMOSSNAP data set](#step1)
    * [Preprocessing to TIPS](#step2)
    * [Generating spectra with TIPS](#step3)
    * [Postprocessing and final set generation](#step4)
    * [Measuring redshifts](#step5)

---

## <a name="intro"></a> Introduction

### <a name="science"></a> Dark Energy and the Euclid Satellite

The European Space Agency [Euclid Mission](http://sci.esa.int/euclid) aims to measure the global properties of the Universe to unprecedented accuracy, with particular emphasis on the properties of the mysterious Dark Energy that is driving the acceleration of the expansion of the Universe. These properties can be inferred from the statistical distribution of galaxies in the Universe and from the effects of the matter distribution on their observed shapes through gravitational lensing. However, this requires extreme precision and accuracy on shape and positional measurements of galaxies.

In particular, measuring their radial distances from us is one of the most challenging problems in modern observational cosmology. The way we infer those distances is through the Doppler effect: due to the expansion of the Cosmos, galaxies are receding from us and their light is consequently shifted towards longer wavelengths (the "red" side of the electromagnetic spectrum). This _redshift_ is directly related to a galaxy's distance, and by measuring it from the properties of the received light, we can reconstruct its position.

### <a name="specphot"></a> Spectroscopic and photometric redshifts

In astronomy, there are two main methods for measuring galaxy redshifts. Measuring _spectroscopic redshifts_ consists in observing the full spectral energy distribution (SED) of a galaxy and identifying features that allow a secure redshift determination. A galaxy's spectrum is a consequence of a series of relatively well-understood physical phenomena, mostly concerning the nuclear and chemical reactions inside stars and the types and ages of stellar populations within the galaxy in question. Atomic emission and absorption lines give rise to very distinct peaks and troughs in a galaxy SED. By identifying such a feature, its wavelength can be compared to the known wavelength of such a transition observed in Earth’s laboratories, and this yields the value of the redshift by the cosmological Doppler effect.

_Photometric redshift_ measurements, on the other hand, try to reconstruct the redshift value out of only a handful of numbers representing the integrated light flux in broadband filters. Degeneracies abound, making results less precise and possibly biased, but they circumvent the need of a spectrograph and can also reach fainter magnitudes, as light is integrated in broad wavelength ranges. Robust photometric redshifts depend much more on a correct model for spectral templates and understanding of the global properties and types of galaxies, and less on the detection of specific features.


### <a name="need4sims"></a> Simulation needs

<!---__ADD PARAGRAPH HERE AS TO WHY SIMULATIONS ARE IMPORTANT__--->

When generating a large realistic simulated spectroscopic and photometric data set to be used as a test bed for redshift estimation, we need to ensure that it is representative of the expected quality of Euclid data. Another requirement is to have a realistic distribution of galaxies in several photometric observational parameters. We want our simulated data to follow representative redshift, color, magnitude and spectral type distributions. These quantities depend on each other in intricate ways; correctly capturing the correlations is essential if we want to have a realistic assessment of the accuracy and improvements of our proposed methods.

We also require realistic spectral energy distributions (SEDs) and emission-line strengths. Euclid will observe an estimated 50 million spectra through slitless spectroscopy. The required sensitivity is defined in terms of the significance of the detection of the Hα Balmer transition line. These requirements imply a detection rate that depends on magnitude and redshift, therefore demanding that we simulated realistic Hα line width and strength, which depend on the properties of the continuum of the spectral distribution. In addition to continuum and line properties, extinction of light by dust within each galaxy needs to be simulated.

<!---
### <a name="struct"></a> The structure
    - COSMOSSNAP for the base spectro-photometric simulation
    - White gaussian noise 
    - TIPS for realistic Euclid slitless spectroscopy 
--->

## <a name="requirements"></a> Requirements

### <a name="basic"></a> Basic Python dependencies

All necessary Python dependencies are included in the Anaconda distribution. The code is compatible with Python 2 and 3.

### <a name="cosmossnap"></a> COSMOSSNAP
COSMOSSNAP is a FORTRAN 77 package to generate spectrophotometric simulations based on real data from the Hubble Telescope [COSMOS survey](http://cosmos.astro.caltech.edu/). It uses galaxy properties catalogs from COSMOS observations, combined with many follow-up ground observations, to generate a synthetic catalog reproducing the relevant observational properties, whilst associating a "true" consistent redshift and SED to each galaxy. Details are described in [Jouvel et al. (2009)](https://arxiv.org/abs/0902.0625).

Previous public links to COSMOSSNAP are deprecated. To obtain a copy of the software and installation instructions, please contact the Corresponding Author.

### <a name="tips"></a> TIPS

TIPS is a software package designed to perform simulations of astronomical slitless spectroscopy observations. It is the pixel simulator of the NISP slitless spectrograph of the ESA Euclid space mission (http://sci.esa.int/euclid). It is based on the aXeSIM code, which is part of the aXe sofware package developed for the support of the Hubble Space Telescope slitless spectroscopic observation modes. 

To install TIPS, clone and follow instructions from https://gitlab.in2p3.fr/in2p3_euclid/tips

### <a name="isap"></a> ISAP
ISAP (Interactive Sparse Astronomical Data Analysis Packages) is a collection of packages in IDL and C++ related to sparsity and its application in astronomical data analysis. You will only need it if you intend to estimate spectroscopic redshifts or denoise galaxy spectra. Instructions for downloading and installing ISAP can be found on its [main webpage](http://www.cosmostat.org/software/isap).

_You will also need an IDL installation and license for this functionality to work. [IDL](http://www.idl-envi.com) is a numerical analysis software analogous to Matlab and is often used in astrophysics, especially in legacy code._


### <a name="pbscluster"></a> A PBS cluster

You will definitely need a computational cluster if you intend to run COSMOSSNAP or TIPS on a non-trivial amount of data. This repository provides PBS scripts to run the different steps of the data processing in such a setting. These were tested in a cluster using the C Shell ([I know, sorry...](http://www.shlomifish.org/open-source/anti/csh/)), so you will need to adapt some lines to Bash if that's what your system uses. This should be easy to do if you have moderate experience with shell scripting.

## <a name="start"></a> Getting Started

To use the functionality developed in this repository, simply clone it into your preferred location and ensure that your system's PYTHONPATH points to it. Setting paths for the [Requirements](#requirements) will be necessary only for the specific functionality you intend to use.

All calls to data in any of the examples refer to the relative location a 'data' folder. To set this up, create an empty 'data' folder in ./dedale_d51/, download this [tarball](add_link_here) (for example, with wget) and untar it within the data folder. __BEWARE: This currently contains several GBs of data.__ This alternative [tarball](add_link_here) contains only the data needed to run the example below. For alternative ways to distribute the full data set, contact the Corresponding Author.

## <a name="example"></a> Example: Euclid-like spectroscopic data

### <a name="step1"></a> Generating a COSMOSSNAP data set

#### The base simulated catalog

COSMOSSNAP uses real data as a basis, thereby ensuring that realistic relationships between galaxy type, colors, size, redshift and SED are preserved. It is necessary to ensure that the chosen data is of high enough precision and optical depth to be representative of the observational properties that will be attained by Euclid. COSMOSSNAP chooses the Hubble Telescope COSMOS survey data, combined with additional data from ground telescopes for more precise photometric redshifts. This data set is matched to Hubble ACS imaging data, to provide realistic size-magnitude distributions, employing weak-lensing-quality shape measurements. This produces a realistic master galaxy catalogue with magnitudes, colors, shapes and photometric redshifts for 538 000 galaxies on a 1.38 deg2 region of the sky down to an i-band magnitude of ∼26.5. For each galaxy, LePHARE integrates all spectra in the library for several redshift test values and finds the combination of a spectrum and a redshift value that provide the best possible fit to the observed multi-band data. In this way, each galaxy is assigned a best-fit template and a redshift value. Galaxy emission line fluxes are calculated based on continuum properties of each galaxy. The final SED of each galaxy is then corrected by host extinction (i.e. dimming due to dust within the galaxy itself, estimated from the photometric properties) and redshifted following the best-fit photometric redshift value. At the end of the generation procedure, we have a galaxy catalogue with an ideal set of photometric properties and best-fit spectral templates with realistic continuum and emission line properties.

Our task is to forward-model the observational process in both the spectroscopic and photometric cases in a manner consistent with expected observational conditions.

#### Realistic broadband photometric properties

To generate realistic photometric properties, the first step is to integrate the best-fit spectral template through a set of broadband wavelength filters that will be used for a given galaxy survey. In actuality, the full transmission curve includes not only filter effects, but also atmospheric transmission (in the case of ground observations), telescope optical effects and more. The full transmission curve is commonly referred to as filter throughput (even though it is not only due to the filter itself). Euclid will require assistance from ground-based survey data sets in order to measure accurate photometric redshifts. COSMOSSNAP takes a defined set of filter throughput definitions for any given ground-based galaxy survey and calculates magnitudes for each galaxy in the catalogue.

<figure style="float: right; padding-bottom:0.5em;">
<img src="./doc/figures/readme/des_filters.png" width="350" />
<figcaption style="width:350; font-size:80%; text-align:justify;">Optical broadband filters designed for the Dark Energy Survey, covering the range from the ultraviolet to the near-infrared. COSMOSSNAP simulates the integration of galaxy SEDs through a given set of filters, including multiple sources of experimental noise. </figcaption>
</figure>

Optical broadband observations are also subject to noise. The two main sources of noise are caused by finite photon counts and CCD read-out noise. These are also introduced by COSMOSSNAP. To verify that the photometric simulations are indeed realistic to the required level, we compare the DES magnitudes and magnitude errors to real data from the CFHT Stripe-82 Survey (CS82). The DES-like i filter data is simulated to have very similar quality to the true CS82 data. The distributions of magnitude errors and depth are in good agreement, confirming that the simulations are a faithful representation of realistic photometric data.

#### Realistic clean spectra

For obtaining realistic spectral templates, we need to resample and integrate the best-fit SEDs. As given by the simulations, these SEDs are pure functional forms. At the end of the observational process, what we obtain is an integrated flux in linear wavelength bins, including noise from sources such as the detector read-out, photon counts, intrinsic galaxy variations, zodiacal light and more.

### <a name="step3"></a> Generating spectra with TIPS

Describe PBS runs and scripts for TIPS spectroscopic generation.

<figure style="float: center; padding-bottom:0.5em;">
<img src="./doc/figures/readme/spec_panel.png" width="500" />
<figcaption style="font-size:80%; text-align:justify;">Several examples of simulated spectra for galaxies at different redshifts, for both shallower (light blue) and deeper (dark blue) observations. The dotted red line indicates the position of the redshifted Hα emission line. </figcaption>
</figure>

### <a name="step4"></a> Postprocessing and final set generation

Brief explanation, figure, point to notebook.

<figure style="float: left; padding-bottom:0.5em;">
<img src="./doc/figures/readme/euclid_selection.png" width="350" />
<figcaption style="width:350; font-size:80%; text-align:justify;">Distribution of representative Euclid spectroscopic galaxies in redshift (top) and Hα flux (bottom) after both wavelength and Hα flux selection are taken into account. </figcaption>
</figure>