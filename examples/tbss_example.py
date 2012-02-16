# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
A pipeline to perform TBSS.
"""
from nipype.workflows.fsl.dti import create_eddy_correct_pipeline
from nipype.pipeline.plugins.multiproc import MultiProcPlugin

"""
Tell python where to find the appropriate functions.
"""
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import os                                    # system functions
from nipype.workflows.fsl import tbss

"""
Confirm package dependencies installed.
"""
from nipype.utils.misc import package_check
package_check('numpy', '1.3', 'tbss_test')
package_check('scipy', '0.7', 'tbss_test')
package_check('networkx', '1.0', 'tbss_test')
package_check('IPython', '0.10', 'tbss_test')

fsl.FSLCommand.set_default_output_type('NIFTI')

"""
Specify the related directories http://fcon_1000.projects.nitrc.org/indi/pro/eNKI_RS_TRT/FrontPage.html
"""
dataDir = os.path.abspath('nki_rs_data')
workingdir = './tbss_example'
subjects_list = ['2475376', '3313349']#, '3808535', '3893245', '8735778', '9630905']

gen_fa = pe.Workflow(name="gen_fa")
gen_fa.base_dir = os.path.join(os.path.abspath(workingdir), 'l1')

subject_id_infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']), name='subject_id_infosource')
subject_id_infosource.iterables = ('subject_id', subjects_list)

datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'], outfields=['dwi', 'bvec', 'bval']), name='datasource')
datasource.inputs.base_directory = os.path.abspath(dataDir)
datasource.inputs.template = '%s/session2/DTI_mx_137/dti.%s'
datasource.inputs.template_args = dict(dwi=[['subject_id', 'nii.gz']],
                                       bvec=[['subject_id', 'bvec']],
                                       bval=[['subject_id', 'bval']])
gen_fa.connect(subject_id_infosource, 'subject_id', datasource, 'subject_id')

eddy_correct = create_eddy_correct_pipeline()
eddy_correct.inputs.inputnode.ref_num = 0
gen_fa.connect(datasource, 'dwi', eddy_correct, 'inputnode.in_file')

bet = pe.Node(interface=fsl.BET(), name='bet')
bet.inputs.mask = True
bet.inputs.frac = 0.34
gen_fa.connect(eddy_correct, 'pick_ref.out', bet, 'in_file')

dtifit = pe.Node(interface=fsl.DTIFit(), name='dtifit')
gen_fa.connect(eddy_correct, 'outputnode.eddy_corrected', dtifit, 'dwi')
gen_fa.connect(subject_id_infosource, 'subject_id', dtifit, 'base_name')
gen_fa.connect(bet, 'mask_file', dtifit, 'mask')
gen_fa.connect(datasource, 'bvec', dtifit, 'bvecs')
gen_fa.connect(datasource, 'bval', dtifit, 'bvals')

datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = os.path.join(os.path.abspath(workingdir), 'l1_results')
datasink.inputs.parameterization = False
gen_fa.connect(dtifit, 'FA', datasink, 'FA')

if __name__ == '__main__':
    gen_fa.write_graph()
    gen_fa.run()#plugin=MultiProcPlugin(plugin_args={'n_procs': 4}))


"""
Here we get the FA list including all the subjects.
"""

tbss_source = pe.Node(interface=nio.DataGrabber(outfiles=['fa_list']), name='tbss_source')
tbss_source.inputs.base_directory = datasink.inputs.base_directory
tbss_source.inputs.template = 'FA/%s_FA.nii'
tbss_source.inputs.template_args = dict(fa_list=[[subjects_list]])

'''
TBSS analysis
'''
tbss_all = tbss.create_tbss_all()
tbss_all.inputs.inputnode.target = fsl.Info.standard_image("FMRIB58_FA_1mm.nii.gz")
tbss_all.inputs.inputnode.skeleton_thresh = 0.2

tbssproc = pe.Workflow(name="tbssproc")
tbssproc.base_dir = os.path.join(os.path.abspath(workingdir), 'l2')
tbssproc.connect(tbss_source, 'fa_list', tbss_all, 'inputnode.fa_list')

if __name__ == '__main__':
    tbssproc.write_graph()
    tbssproc.run(plugin=MultiProcPlugin(plugin_args={'n_procs': 4}))