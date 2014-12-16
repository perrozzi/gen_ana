source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc491
cd /cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_0_pre1/src
cmsenv
export X509_USER_PROXY=/afs/cern.ch/user/p/peller/x509up_u32268
cd /afs/cern.ch/user/p/peller/work/private/rivet
export RIVET_REF_PATH=/afs/cern.ch/user/p/peller/work/private/rivet
export RIVET_ANALYSIS_PATH=/afs/cern.ch/user/p/peller/work/private/rivet
export TERM=""
cmsRun run_rivet_cfi.py $1
