#!/bin/bash

export RIVET_ANALYSIS_PATH=`pwd`
export RIVET_REF_PATH=`pwd`

g++ -o "RivetATLAS_2014_I1279489.so" -shared -fPIC \
-I/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/rivet/2.1.2-cms4/include \
-L/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/rivet/2.1.2-cms4/lib \
-I/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/hepmc/2.06.07-cms/include \
-L/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/hepmc/2.06.07-cms/lib \
-I/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/fastjet/3.1.0/include \
-L/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/fastjet/3.1.0/lib \
-I/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gsl/1.10-cms/include \
-I/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/boost/1.57.0/include \
-L/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_0_pre1/lib/slc6_amd64_gcc491 \
-I/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/yoda/1.1.0-cms2/include \
-L/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/yoda/1.1.0-cms2/lib \
-pedantic -ansi -Wall -Wno-long-long -std=c++0x ATLAS_2014_I1279489.cc

