#!/bin/bash

# Output files to be copied back to the User Interface
# (the file path must be given relative to the working directory)

TOPWORKDIR=/scratch/`whoami`

# Basename of job sandbox (job workdir will be $TOPWORKDIR/$JOBDIR)
JOBDIR=sgejob-stage$1-par$2

##### MONITORING/DEBUG INFORMATION ###############################
DATE_START=`date +%s`
echo "Job started at " `date`


##### SET UP WORKDIR AND ENVIRONMENT ######################################
PWGDIR=/shome/peller/POWHEG-BOX-V2/HZ/
STARTDIR=$PWGDIR/batch/
WORKDIR=$TOPWORKDIR/$JOBDIR
if test -e "$WORKDIR"; then
   echo "ERROR: WORKDIR ($WORKDIR) already exists! Aborting..." >&2
   exit 1
fi
mkdir -p $WORKDIR
if test ! -d "$WORKDIR"; then
   echo "ERROR: Failed to create workdir ($WORKDIR)! Aborting..." >&2
   exit 1
fi

cd $WORKDIR

## YOUR FUNCTIONALITY CODE GOES HERE

source $VO_CMS_SW_DIR/cmsset_default.sh
export SCRAM_ARCH=slc5_amd64_gcc462
cd /shome/peller/CMSSW_5_3_21/src
eval `scramv1 runtime -sh`

export PATH=$PATH:/swshare/cms/slc5_amd64_gcc462/external/lhapdf/5.9.1/bin
export LHAPATH=/shome/peller/LHAPDFsets2

cd $WORKDIR


# argv $1 = par

cp $STARTDIR/pwgseeds.dat .
cp $STARTDIR/powheg.input-save .
cp $STARTDIR/pythia8ex7_cfg.py .
cp $STARTDIR/run_rivet_cfi.py .

echo "running stage 1"
for igrid in {1..2}
do
    cat powheg.input-save | sed "s/xgriditeration.*/xgriditeration $igrid/ ; s/parallelstage.*/parallelstage 1/" > powheg.input
    echo "xgrid $igrid"
    echo $1 | $PWGDIR/pwhg_main > $STARTDIR/log/run-st1-grid$igrid-$1.log 2>&1
done

for stage in {2..4}
do
    echo "running stage $stage"
    cat powheg.input-save | sed "s/parallelstage.*/parallelstage $stage/ " > powheg.input
    echo $1 | $PWGDIR/pwhg_main > $STARTDIR/log/run-st$stage-$1.log 2>&1
done

cp pwgevents-*.lhe $STARTDIR/
echo "running shower"
mv pwgevents-*.lhe pwgevents.lhe
cmsRun pythia8ex7_cfg.py

echo "running rivet"
export RIVET_ANALYSIS_PATH=`pwd`
export RIVET_REF_PATH=`pwd`
cp /shome/peller/gen_ana/rivet/MC_ZHBB.plot .
cp /shome/peller/gen_ana/rivet/MC_ZHBB.info .

echo "inclusive"
cp /shome/peller/gen_ana/rivet/RivetMC_ZHBB.so .
cmsRun run_rivet_cfi.py
cp powheg_pythia.aida $STARTDIR/rivet_inc_$1.aida

echo "selection"
cp /shome/peller/gen_ana/rivet/RivetMC_ZHBB_sel.so RivetMC_ZHBB.so
cmsRun run_rivet_cfi.py
cp powheg_pythia.aida $STARTDIR/rivet_sel_$1.aida

echo "Cleaning up $WORKDIR"
rm -rf $WORKDIR

DATE_END=`date +%s`
RUNTIME=$((DATE_END-DATE_START))
echo "################################################################"
echo "Job finished at " `date`
echo "Wallclock running time: $RUNTIME s"
exit 0
