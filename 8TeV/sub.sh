while read filename; do
    bsub -q 1nh /afs/cern.ch/user/p/peller/work/private/rivet/job.sh $filename
    #python test.py $filename
done < DY_8TeV_NLO.txt
