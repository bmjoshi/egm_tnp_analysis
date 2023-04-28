#! /bin/bash
echo $PWD
echo "Setting environment"
workdir="/afs/cern.ch/work/b/bjoshi/Analysis/UMN/egm_tnp_analysis/";
cmssw_path="/afs/cern.ch/work/b/bjoshi/Analysis/UMN/CMSSW_10_2_8/src";
cd $cmssw_path; cmsenv; cd $workdir
export PYTHONPATH=$workdir;
cd $cmssw_path; cmsenv; cd $workdir
# $1 config: etc/config/settings_pho_run2022BC.py
# $2 id
python tnpEGM_fitter.py $1 --flag $2 --checkBins
python tnpEGM_fitter.py $1 --flag $2 --createBins
python tnpEGM_fitter.py $1 --flag $2 --createHists
python tnpEGM_fitter.py $1 --flag $2 --doFit
python tnpEGM_fitter.py $1 --flag $2 --sumUp
