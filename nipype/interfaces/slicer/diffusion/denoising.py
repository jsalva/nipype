"""Autogenerated file - DO NOT EDIT         
If you spot a bug, please report it on the mailing list and/or change the generator."""

from nipype.interfaces.base import CommandLine, CommandLineInputSpec, TraitedSpec, File, Directory, traits, isdefined, InputMultiPath, OutputMultiPath
import os
from nipype.interfaces.slicer.base import SlicerCommandLine


class jointLMMSEInputSpec(CommandLineInputSpec):
    re = InputMultiPath(traits.Int, desc="Estimation radius.", sep=",", argstr="--re %s")
    rf = InputMultiPath(traits.Int, desc="Filtering radius.", sep=",", argstr="--rf %s")
    ng = traits.Int(desc="The number of the closest gradients that are used to jointly filter a given gradient direction (0 to use all).", argstr="--ng %d")
    inputVolume = File(position="0", desc="Input DWI volume.", exists=True, argstr="--inputVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), position="1", hash_files=False, desc="Output DWI volume.", argstr="--outputVolume %s")


class jointLMMSEOutputSpec(TraitedSpec):
    outputVolume = File(position="1", desc="Output DWI volume.", exists=True)


class jointLMMSE(SlicerCommandLine):
    """title: Joint Rician LMMSE Image Filter

category: Diffusion.Denoising

description: 
This module reduces Rician noise (or unwanted detail) on a set of diffusion weighted images. For this, it filters the image in the mean squared error sense using a Rician noise model. The N closest gradient directions to the direction being processed are filtered together to improve the results: the noise-free signal is seen as an n-diemensional vector which has to be estimated with the LMMSE method from a set of corrupted measurements. To that end, the covariance matrix of the noise-free vector and the cross covariance between this signal and the noise have to be estimated, which is done taking into account the image formation process.
The noise parameter is automatically estimated from a rough segmentation of the background of the image. In this area the signal is simply 0, so that Rician statistics reduce to Rayleigh and the noise power can be easily estimated from the mode of the histogram.
A complete description of the algorithm may be found in:
Antonio Tristan-Vega and Santiago Aja-Fernandez, DWI filtering using joint information for DTI and HARDI, Medical Image Analysis, Volume 14, Issue 2, Pages 205-218. 2010. 
  

version: 0.1.1.$Revision: 1 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/JointRicianLMMSEImageFilter

contributor: Antonio Tristan Vega, Santiago Aja Fernandez. University of Valladolid (SPAIN). Partially founded by grant number TEC2007-67073/TCM from the Comision Interministerial de Ciencia y Tecnologia (Spain).
  

"""

    input_spec = jointLMMSEInputSpec
    output_spec = jointLMMSEOutputSpec
    _cmd = " jointLMMSE "
    _outputs_filenames = {'outputVolume':'outputVolume.nii'}


class dwiNoiseFilterInputSpec(CommandLineInputSpec):
    iter = traits.Int(desc="Number of iterations for the noise removal filter.", argstr="--iter %d")
    re = InputMultiPath(traits.Int, desc="Estimation radius.", sep=",", argstr="--re %s")
    rf = InputMultiPath(traits.Int, desc="Filtering radius.", sep=",", argstr="--rf %s")
    mnvf = traits.Int(desc="Minimum number of voxels in kernel used for filtering.", argstr="--mnvf %d")
    mnve = traits.Int(desc="Minimum number of voxels in kernel used for estimation.", argstr="--mnve %d")
    minnstd = traits.Int(desc="Minimum allowed noise standard deviation.", argstr="--minnstd %d")
    maxnstd = traits.Int(desc="Maximum allowed noise standard deviation.", argstr="--maxnstd %d")
    hrf = traits.Float(desc="How many histogram bins per unit interval.", argstr="--hrf %f")
    uav = traits.Bool(desc="Use absolute value in case of negative square.", argstr="--uav ")
    inputVolume = File(position="0", desc="Input DWI volume.", exists=True, argstr="--inputVolume %s")
    outputVolume = traits.Either(traits.Bool, File(), position="1", hash_files=False, desc="Output DWI volume.", argstr="--outputVolume %s")


class dwiNoiseFilterOutputSpec(TraitedSpec):
    outputVolume = File(position="1", desc="Output DWI volume.", exists=True)


class dwiNoiseFilter(SlicerCommandLine):
    """title: Rician LMMSE Image Filter

category: Diffusion.Denoising

description: 
This module reduces noise (or unwanted detail) on a set of diffusion weighted images. For this, it filters the image in the mean squared error sense using a Rician noise model. Images corresponding to each gradient direction, including baseline, are processed individually. The noise parameter is automatically estimated (noise estimation improved but slower).
Note that this is a general purpose filter for MRi images. The module jointLMMSE has been specifically designed for DWI volumes and shows a better performance, so its use is recommended instead.
A complete description of the algorithm in this module can be found in:
S. Aja-Fernandez, M. Niethammer, M. Kubicki, M. Shenton, and C.-F. Westin. Restoration of DWI data using a Rician LMMSE estimator. IEEE Transactions on Medical Imaging, 27(10): pp. 1389-1403, Oct. 2008. 


version: 0.1.1.$Revision: 1 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.0/Modules/RicianLMMSEImageFilter

contributor: Antonio Tristan Vega, Santiago Aja Fernandez and Marc Niethammer. Partially founded by grant number TEC2007-67073/TCM from the Comision Interministerial de Ciencia y Tecnologia (Spain).

"""

    input_spec = dwiNoiseFilterInputSpec
    output_spec = dwiNoiseFilterOutputSpec
    _cmd = " dwiNoiseFilter "
    _outputs_filenames = {'outputVolume':'outputVolume.nii'}
