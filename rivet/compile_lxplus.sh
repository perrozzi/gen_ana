#!/bin/bash

#eval `scramv1 runtime -sh`
export RIVET_ANALYSIS_PATH=`pwd`
export RIVET_REF_PATH=`pwd`

g++ -o "RivetMC_ZHBB.so" -shared -fPIC \
-I/cvmfs/cms.cern.ch/slc6_amd64_gcc472/external/rivet/1.9.0-cms/include \
-L/cvmfs/cms.cern.ch/slc6_amd64_gcc472/cms/cmssw/CMSSW_5_3_21/lib/slc6_amd64_gcc472 \
-L/cvmfs/cms.cern.ch/slc6_amd64_gcc472/external/rivet/1.9.0-cms/lib \
-L/afs/cern.ch/user/p/peller/CMSSW_5_3_21/lib/slc6_amd64_gcc472 \
-I/afs/cern.ch/cms/slc5_amd64_gcc481/external/hepmc/2.06.07/include \
-I/afs/cern.ch/cms/slc5_amd64_gcc481/external/fastjet/3.0.3/include \
-L/afs/cern.ch/cms/slc5_amd64_gcc481/external/fastjet/3.0.3/lib \
-I/afs/cern.ch/cms/slc5_amd64_gcc481/external/gsl/1.10/include \
-I/afs/cern.ch/cms/slc5_amd64_gcc481/external/boost/1.51.0-cms2/include \
-pedantic -ansi -Wall -Wno-long-long -std=c++0x MC_ZHBB.cc


# rivet -q --analysis=CMS_2012_I941555 /nfsdisk/perrozzi/CMSSW_4_4_5/src/WMassNNLO/resbos/a1_scan_kc1/resbos_all.hep

# mv Rivet.aida rivet-CMS-EWK-10-010-2.aida

# rivet-mkhtml rivet-CMS-EWK-10-010-2.aida
