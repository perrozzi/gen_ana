#!/bin/bash

#eval `scramv1 runtime -sh`
export RIVET_ANALYSIS_PATH=`pwd`
export RIVET_REF_PATH=`pwd`

g++ -o "RivetMC_ZHBB.so" -shared -fPIC \
-I/swshare/cms/slc6_amd64_gcc472/external/rivet/1.9.0-cms/include \
-L/swshare/cms/slc6_amd64_gcc472/cms/cmssw/CMSSW_5_3_21/lib/slc6_amd64_gcc472 \
-L/swshare/cms/slc6_amd64_gcc472/external/rivet/1.9.0-cms/lib \
-L/shome/peller/peller/CMSSW_5_3_21/lib/slc6_amd64_gcc472 \
-I/swshare/cms/slc6_amd64_gcc472/external/hepmc/2.06.07-cms//include \
-I/swshare/cms/slc6_amd64_gcc472/external/fastjet/3.0.1-cms2/include \
-L/swshare/cms/slc6_amd64_gcc472/external/fastjet/3.0.1-cms2/lib \
-I/swshare/cms/slc6_amd64_gcc472/external/gsl/1.10-cms/include \
-I/swshare/cms/slc6_amd64_gcc472/external/boost/1.47.0-cms/include \
-pedantic -ansi -Wall -Wno-long-long -std=c++0x MC_ZHBB.cc

g++ -o "RivetMC_ZHBB_sel.so" -shared -fPIC \
-I/swshare/cms/slc6_amd64_gcc472/external/rivet/1.9.0-cms/include \
-L/swshare/cms/slc6_amd64_gcc472/cms/cmssw/CMSSW_5_3_21/lib/slc6_amd64_gcc472 \
-L/swshare/cms/slc6_amd64_gcc472/external/rivet/1.9.0-cms/lib \
-L/shome/peller/peller/CMSSW_5_3_21/lib/slc6_amd64_gcc472 \
-I/swshare/cms/slc6_amd64_gcc472/external/hepmc/2.06.07-cms//include \
-I/swshare/cms/slc6_amd64_gcc472/external/fastjet/3.0.1-cms2/include \
-L/swshare/cms/slc6_amd64_gcc472/external/fastjet/3.0.1-cms2/lib \
-I/swshare/cms/slc6_amd64_gcc472/external/gsl/1.10-cms/include \
-I/swshare/cms/slc6_amd64_gcc472/external/boost/1.47.0-cms/include \
-pedantic -ansi -Wall -Wno-long-long -std=c++0x MC_ZHBB_sel.cc
# rivet -q --analysis=CMS_2012_I941555 /nfsdisk/perrozzi/CMSSW_4_4_5/src/WMassNNLO/resbos/a1_scan_kc1/resbos_all.hep

# mv Rivet.aida rivet-CMS-EWK-10-010-2.aida

# rivet-mkhtml rivet-CMS-EWK-10-010-2.aida
