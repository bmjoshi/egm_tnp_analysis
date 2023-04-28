#!/usr/bin/env python3
# coding: utf-8

import gc
import pickle

import uproot
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import to_rgba, to_rgb


#plt.style.use('cmsstyle') # use custom matplotlib style

def set_custom_alpha(col_, alpha_):
    rgb_ = to_rgba(col_)
    return (col_[0], col_[1], col_[2], alpha_)

def rgb2rgba(col_):
    _ = []
    for c in col_:
        _.append(float(c)/255.0)
    _.append(1.0)
    return tuple(_)

# config
config = {
    'puFile': '/eos/user/b/bjoshi/cms_tools/lumi/egm_pu/crab_2023-02-01/pileup_2022BC.root',
    'inputDir': '/eos/cms/store/group/phys_egamma/tnpTuples/bjoshi/2023-02-01/2022/mc/',
    'filename': 'TnPTree_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8_2022_DY_LO.root', 
    'tree': 'tnpEleIDs',
    'tag': '2022_runBC',
    'puType': 'truePU', # truePU, event_nPV, rho
    'outputfile': 'DY_1j_madgraph_preEE_tnpEleID.pu.puTree.root'
}

putree = uproot.open(config['puFile'])['pileup']
puprofile = putree.to_numpy()[0]
MAX_PU = putree.to_numpy()[1][-1]

mctree = uproot.open(config['inputDir']+config['filename'])[config['tree']]['fitter_tree']
puarray = mctree.arrays([config['puType']])[config['puType']]

# plot cms pileup
plt.figure(figsize=(6.6,6.6))
x_min = 0; x_max = MAX_PU

datanorm = np.sum(puprofile)
mcnorm = 1.0/len(puarray)

mcweights = np.ones_like(puarray)*mcnorm
    
y_ = plt.hist(puarray,
              histtype='stepfilled', color='tab:orange',
              bins=int(x_max), range=(x_min, x_max), label='MC', alpha=0.5, weights=mcweights)
y_ = plt.hist(puarray,
              histtype='step', color='tab:orange',
              bins=int(x_max), range=(x_min, x_max), linewidth=2, weights=mcweights)
max_y = max(y_[0])

xarray = putree.to_numpy()[1]
xarray = (xarray[:-1]+xarray[1:])/2.0
plt.errorbar(x=xarray, y=puprofile/datanorm, xerr=np.zeros_like(xarray), yerr=np.zeros_like(xarray))
max_y = max(max_y, max(puprofile/datanorm))

plt.xlabel(config['puType'], fontsize=14)
plt.ylabel('a.u.', fontsize=14)
leg_elements = [Patch(facecolor=set_custom_alpha(to_rgb('tab:orange'), 0.5), edgecolor='tab:orange', label='MC', linewidth=2)]

plt.legend(handles=leg_elements, loc='upper right',fontsize=18)
year = plt.text(x=x_max, y=max_y*1.05, s=config['tag'],
    fontsize=18)
plt.savefig('%s.png' % config['tag'])
plt.close()

puweights = (puprofile/datanorm)/y_[0]
tmp = (puweights==np.inf)*0+(puweights!=np.inf)*puweights # inf -> nan
puweights = np.nan_to_num(tmp,0) # convert nan -> 0
eventWeights = list(map(lambda x: puweights[int(x)], puarray))

newFile = uproot.recreate(config['outputfile'])
newFile['weights_'+config['tag']] = {'PUweight': eventWeights, 'totWeight': eventWeights}
newFile.close()
