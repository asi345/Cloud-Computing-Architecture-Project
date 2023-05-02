#!/bin/bash
while getopts j:n:t:c: flag;
do
    case "$flag" in
        j) job=${OPTARG};;
        n) node=${OPTARG};;
        t) threads=${OPTARG};;
        c) core=${OPTARG};;
    esac
done

sudo sed -i "" -e "s/cca-project-nodetype: \"parsec\"/cca-project-nodetype: \"$node\"/" ./parsec-benchmarks/parsec-$job.yaml
sudo sed -i "" -e "s/native -n 1/native -n $threads/" ./parsec-benchmarks/parsec-$job.yaml
if [ "$name" != "" ]; then
    sudo sed -i "" -e "s/\"-c\", \"/\"-c\", \"taskset -c $core /" ./parsec-benchmarks/parsec-$job.yaml
fi

kubectl create -f ./parsec-benchmarks/parsec-$job.yaml

sudo sed -i "" -e "s/cca-project-nodetype: \"$node\"/cca-project-nodetype: \"parsec\"/" ./parsec-benchmarks/parsec-$job.yaml
sudo sed -i "" -e "s/native -n $threads/native -n 1/" ./parsec-benchmarks/parsec-$job.yaml
if [ "$name" != "" ]; then
    sudo sed -i "" -e "s/\"-c\", \"taskset -c $core /\"-c\", \"/" ./parsec-benchmarks/parsec-$job.yaml
fi