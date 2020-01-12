#!/bin/sh
echo $"Optimize like a boss"

NB_ITERATION=10

data1name=`ls data_1/*.txt`
data2name=`ls data_2/*.txt`

filenames="$data1name $data2name"

for eachfile in $filenames
do
   echo $eachfile
   for i in {0..1000}
   do
     python3 flowshop.py "$eachfile" "0"
   done
done






