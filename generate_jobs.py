import os

# use the script to generate condor jobs
# this will generate a submission file that submits all the jobs to condor

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

cfgfiles = {
        'pho_94X_2022BC': 'etc/config/settings_pho_run2022BC_RunIIUL_binning.py',
        'pho_94X_2022EFG': 'etc/config/settings_pho_run2022EFG_RunIIUL_binning.py',
        'ele_94X_2022BC': 'etc/config/settings_ele_run2022BC_RunIIUL_binning.py',
        'ele_94X_2022EFG': 'etc/config/settings_ele_run2022EFG_RunIIUL_binning.py'
        }

idmap = {
        'pho_94X_2022BC': photon_94X_ids, 
        'pho_94X_2022EFG': photon_94X_ids,
        'ele_94X_2022BC': electron_94X_ids,
        'ele_94X_2022EFG': electron_94X_ids
        }

def generate_jobs(cfgfile, jobtag, ids):
   '''
   generates crab job for computation of scale factor for given id;
   returns a list containing the names of files to be submitted
   '''
   jobs = []
   for id_ in ids:
        with open('condor_bjoshi.sub','r') as f0:
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
