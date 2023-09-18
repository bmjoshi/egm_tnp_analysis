#=====================================
# + Basic commands for running the fit
#=====================================
# Check binning:
#---------------
#   python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --checkBins   &> Log_RecoSF2017UL/log2017ULCheckBin_highpt.txt &
#
# Create binning:
#----------------
#   python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --createBins   &> Log_RecoSF2017UL/log2017ULCreateBin_highpt.txt &
#
# Create histogram:
#------------------
#   python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --createHists   &> Log_RecoSF2017UL/log2017ULCreateHist_highpt.txt &
#
# The fitting steps:
#---------------------
# - python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --doFit                       &> Log_RecoSF2017UL/log2017ULFit_highpt_nominal.txt &
# - python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --doFit  --mcSig   --altSig   &> Log_RecoSF2017UL/log2017ULFit_highpt_MCfit.txt &
# - python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --doFit  --altSig             &> Log_RecoSF2017UL/log2017ULFit_highpt_AltSigfit.txt &
# - python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --doFit  --altBkg             &> Log_RecoSF2017UL/log2017ULFit_highpt_AltBkgfit.txt &
#
# Redo fail fit:
#-----------------
# - python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --doFit  --iBin ib       &> Log_RecoSF2017UL/log2017ULFix_highpt_nominal_binX.txt &
#
# EGM output text file:
#------------------------
# - python  tnpEGM_fitter.py  etc/config/setting_ele2017UL_highpt.py  --flag passingRECO  --sumUp    &> Log_RecoSF2017UL/log2017ULSumUp_highpt.txt &



# flag to be Tested

flags = {
        'passingRECO': 'passingRECO==1',
        'passingRECOEcalDriven': 'passingRECOEcalDriven==1',
        'passingRECOTrackDriven': 'passingRECOTracksDriven==1'
        }
baseOutDir = '/eos/user/b/bjoshi/www/EGM/TnP/PromptReco_official/tnpEleReco_PromptReco2022FG_lowpt'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpEleReco'

samplesDef = {
        'data'  : tnpSamples.Run3_Reco_124X_PromptReco_postEE['data_Run2022F'].clone(),
        'mcNom' : tnpSamples.Run3_Reco_124X_PromptReco_postEE['DY_1j_madgraph_postEE'].clone(),
        'tagSel': tnpSamples.Run3_Reco_124X_PromptReco_postEE['DY_1j_madgraph_postEE'].clone(),
        'mcAlt': None,
    }

## can add data sample easily

samplesDef['data'].add_sample(tnpSamples.Run3_Reco_124X_PromptReco_postEE['data_Run2022G'].clone()) 

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
if not samplesDef['mcNom' ] is None:   samplesDef['mcNom' ].set_mcTruth()
#if not samplesDef['mcAlt' ] is None:   samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None:   samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
	samplesDef['tagSel'].rename('mcAltSel_DY_madgraph_ele')
	samplesDef['tagSel'].set_cut('tag_Ele_pt > 37')

## set MC weight, simple way (use tree weight)
puFile = '/eos/cms/store/group/phys_egamma/tnpTuples/bjoshi/2023-04-25/2022/pu/DY_1j_madgraph_PromptReco2022FG_tnpEleReco.pu.puTree.root'
weightName = 'weights_2022_runFG.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree(puFile)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree(puFile)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree(puFile)



#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
	{'var':'sc_abseta', 'type':'float', 'bins':[0.0, 1.0, 1.444, 1.566, 2.0, 2.5]},
	{'var':'sc_pt', 'type':'float', 'bins':[10,20]},
	]



#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase = 'tag_Ele_pt>35 && sc_pt>10  &&  tag_sc_abseta<2.5 && sc_abseta<2.5  &&  sqrt(2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi)))<60'


# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = {
	0 : 'sc_pt < 20 && tag_Ele_IsoMVA94X > 0.96 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45 && sc_tkIso/sc_pt < 0.1',
	}

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################

tnpParNomFit = [
	"meanP[0.0, -3.0, 3.0]", "sigmaP[0.9, 0.5, 1.5]",
	"meanF[0.0, -3.0, 3.0]", "sigmaF[0.9, 0.5, 1.5]",
	"acmsP[90.0]", "betaP[0.02, 0.01, 0.10]", "gammaP[0.0, 0.0, 0.1]", "peakP[90.0]",
	"acmsF[90.0]", "betaF[0.02, 0.01, 0.10]", "gammaF[0.0]", "peakF[90.0]",
	]

tnpParAltSigFit = [
	"meanP[-0.0, -1.0, 1.0]", "sigmaP[0.5, 0.2, 3.0]", "alphaP[2.0, 1.2, 3.5]", "nP[3, -5, 5]", "sigmaP_2[0.5, 0.2, 3.0]", "sosP[1, 0.1, 5.0]",
	"meanF[-0.0, -1.0, 1.0]", "sigmaF[0.5, 0.2, 3.0]", "alphaF[2.0, 1.2, 3.5]", "nF[3, -5, 5]", "sigmaF_2[0.5, 0.2, 3.0]", "sosF[1, 0.1, 5.0]",
	"acmsP[90.0]", "betaP[0.02, 0.01, 0.10]", "gammaP[0.0, 0.0, 0.1]", "peakP[90.0]",
	"acmsF[90.0]", "betaF[0.02, 0.01, 0.10]", "gammaF[0.0]", "peakF[90.0]",
	]

tnpParAltSigFit_addGaus = [
	"meanP[-0.0, -1.0, 1.0]", "sigmaP[0.5, 0.2, 3.0]", "alphaP[2.0, 1.2, 3.5]", "nP[3, -5, 5]", "sigmaP_2[0.5, 0.2, 3.0]", "sosP[1, 0.1, 5.0]",
	"meanF[-0.0, -1.0, 1.0]", "sigmaF[0.5, 0.2, 3.0]", "alphaF[2.0, 1.2, 3.5]", "nF[3, -5, 5]", "sigmaF_2[0.5, 0.2, 3.0]", "sosF[1, 0.1, 5.0]",
	"acmsP[90.0]", "betaP[0.02, 0.01, 0.10]", "gammaP[0.0, 0.0, 0.1]", "peakP[90.0]",
	"acmsF[90.0]", "betaF[0.02, 0.01, 0.10]", "gammaF[0.0]", "peakF[90.0]",
	]

tnpParAltBkgFit = [
	"meanP[0.0, -3.0, 3.0]", "sigmaP[0.9, 0.5, 2.0]",
	"meanF[0.0, -3.0, 3.0]", "sigmaF[0.9, 0.5, 2.0]",
	"alphaP[0.00, -0.1, 0.1]",
	"alphaF[0.01,  -10.0, 0.1]",
        "tau1[-0.00,-1.0,0.0]","tau2[-0.05,-10.0,0.0]",
        "peak1[48.3,40.0,70.0]","peak2[53.4,40.0,70.0]",
        "f[0.13,0.0,1.0]"
	]
