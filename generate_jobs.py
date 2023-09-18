import os

# use the script to generate condor jobs
# this will generate a submission file that submits all the jobs to condor

condor_template = 'condor_bjoshi.sub'

electron_94X_ids = ['passingMVA94Xwp80isoV2',
                    'passingMVA94Xwp80noisoV2',
                    'passingMVA94Xwp90isoV2',
                    'passingMVA94Xwp90noisoV2',
                    'passingCutBasedVeto94XV2',
                    'passingCutBasedLoose94XV2',
                    'passingCutBasedMedium94XV2',
                    'passingCutBasedTight94XV2']

photon_94X_ids = [
    'passingCutBasedLoose94XV2'     ,
    'passingCutBasedMedium94XV2'    ,
    'passingCutBasedTight94XV2'     ,
    'passingMVA94XV2wp80'           ,
    'passingMVA94XV2wp90'           ]


electron_122X_ids = [
       'passingMVA122Xwp80isoV1',
       'passingMVA122Xwp80noisoV1',
       'passingMVA122Xwp90isoV1',
       'passingMVA122Xwp90noisoV1',
       'passingCutBasedVeto122XV1', 
       'passingCutBasedLoose122XV1', 
       'passingCutBasedMedium122XV1', 
       'passingCutBasedTight122XV1', 
        ]

photon_122X_ids = [
    'passingCutBasedLoose122XV1'     ,
    'passingCutBasedMedium122XV1'    ,
    'passingCutBasedTight122XV1'     ,
    'passingMVA122XV1wp80'           ,
    'passingMVA122XV1wp90'           ]

cfgfiles = {
#        'pho_122X_2022FG': 'etc/config/settings_pho_PromptReco2022FG.py',
#        'ele_122X_2022FG': 'etc/config/settings_ele_PromptReco2022FG.py',
#        'pho_122X_2022BCD': 'etc/config/settings_pho_ReReco2022BCD.py',
#        'ele_122X_2022BCD': 'etc/config/settings_ele_ReReco2022BCD.py',
#        'pho_122X_2022E': 'etc/config/settings_pho_ReReco2022E.py',
#        'ele_122X_2022E': 'etc/config/settings_ele_ReReco2022E.py',
        'pho_122X_2023CD': 'etc/config/settings_pho_PromptReco2022CD.py',
        'ele_122X_2023CD': 'etc/config/settings_ele_PromptReco2022CD.py',
        }

idmap = {
        'pho_94X_2022F': photon_94X_ids,
        'pho_122X_2022F': photon_122X_ids, 
        'pho_94X_2022G': photon_94X_ids,
        'pho_122X_2022G': photon_122X_ids,
        'pho_122X_2022FG': photon_122X_ids,
        'ele_94X_2022F': electron_94X_ids,
        'ele_122X_2022F': electron_122X_ids,
        'ele_94X_2022G': electron_94X_ids,
        'ele_122X_2022G': electron_122X_ids,
        'ele_122X_2022FG': electron_122X_ids,
        }

idmap = {
#        'pho_122X_2022BCD': photon_122X_ids,
#        'ele_122X_2022BCD': electron_122X_ids,       
#        'pho_122X_2022E': photon_122X_ids,
#        'ele_122X_2022E': electron_122X_ids,       
        'pho_122X_2023CD': photon_122X_ids,
        'ele_122X_2023CD': electron_122X_ids,       
        }

def generate_jobs(cfgfile, jobtag, ids):
   '''
   generates crab job for computation of scale factor for given id;
   returns a list containing the names of files to be submitted
   '''
   jobs = []
   for id_ in ids:
        with open(condor_template,'r') as f0:
           lines = f0.readlines()
        jobfile = 'condor_{}_{}.sub'.format(id_, jobtag)
        with open(jobfile,'w') as f0:
           for l in lines:
              if '<config>' in l: l = l.replace('<config>',cfgfile)
              if '<id>' in l: l = l.replace('<id>',id_)
              f0.write(l)
        jobs.append(jobfile)
   return jobs


def main():
    print('------------------------------------------------')
    print("For submitting all jobs, run source SubmitAll.sh")
    print('------------------------------------------------')

    with open('SubmitAll.sh','w') as submitfile:
        for c in cfgfiles:
            joblist = generate_jobs(cfgfiles[c],c,idmap[c])
            for cj in joblist:
                submitfile.write('condor_submit %s\n' % cj)

if __name__=='__main__':
    main()

