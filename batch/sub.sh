#!/bin/bash
for i in {1..100}
do
    qsub -V -cwd -q all.q -l h_vmem=6G -N powheg-$i -o ./log//sub-$i.out -e ./log/sub-$i.err pwg.sh $i
done
