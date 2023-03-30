cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part2
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
export PROJECT=`gcloud config get-value project`
kops create -f ../Part1/cloud-comp-arch-project/part2a.yaml
kops update cluster part2a.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide > nodes_data.txt
python3 nodes_data.py
source node_vars.txt
#gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$PARSEC_NAME --zone europe-west3-a
kubectl label nodes $PARSEC_NAME cca-project-nodetype=parsec

#BLACKSCHOLES NONE
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-blackscholes.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_interference_none.txt
kubectl delete jobs --all
kubectl delete pods --all

#BLACKSCHOLES CPU
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-blackscholes.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_interference_cpu.txt
kubectl delete jobs --all
kubectl delete pods --all

#BLACKSCHOLES L1D
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-blackscholes.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_interference_l1d.txt
kubectl delete jobs --all
kubectl delete pods --all

#BLACKSCHOLES L1I
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-blackscholes.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_interference_l1i.txt
kubectl delete jobs --all
kubectl delete pods --all

#BLACKSCHOLES L2
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-blackscholes.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_interference_l2.txt
kubectl delete jobs --all
kubectl delete pods --all

#BLACKSCHOLES LLC
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-blackscholes.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_interference_llc.txt
kubectl delete jobs --all
kubectl delete pods --all

#BLACKSCHOLES MEMBW
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-blackscholes.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_interference_membw.txt
kubectl delete jobs --all
kubectl delete pods --all

#CANNEAL NONE
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-canneal.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_interference_none.txt
kubectl delete jobs --all
kubectl delete pods --all

#CANNEAL CPU
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-canneal.yaml
sleep 120 #Duration was 101 seconds in my test run
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_interference_cpu.txt
kubectl delete jobs --all
kubectl delete pods --all

#CANNEAL L1D
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-canneal.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_interference_l1d.txt
kubectl delete jobs --all
kubectl delete pods --all

#CANNEAL L1I
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-canneal.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_interference_l1i.txt
kubectl delete jobs --all
kubectl delete pods --all

#CANNEAL L2
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-canneal.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_interference_l2.txt
kubectl delete jobs --all
kubectl delete pods --all

#CANNEAL LLC
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-canneal.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_interference_llc.txt
kubectl delete jobs --all
kubectl delete pods --all

#CANNEAL MEMBW
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-canneal.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_interference_membw.txt
kubectl delete jobs --all
kubectl delete pods --all

#DEDUP NONE
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_interference_none.txt
kubectl delete jobs --all
kubectl delete pods --all

#DEDUP CPU
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-dedup.yaml
sleep 120 #Duration was 101 seconds in my test run
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_interference_cpu.txt
kubectl delete jobs --all
kubectl delete pods --all

#DEDUP L1D
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_interference_l1d.txt
kubectl delete jobs --all
kubectl delete pods --all

#DEDUP L1I
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_interference_l1i.txt
kubectl delete jobs --all
kubectl delete pods --all

#DEDUP L2
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_interference_l2.txt
kubectl delete jobs --all
kubectl delete pods --all

#DEDUP LLC
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_interference_llc.txt
kubectl delete jobs --all
kubectl delete pods --all

#DEDUP MEMBW
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_interference_membw.txt
kubectl delete jobs --all
kubectl delete pods --all

#FERRET NONE
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-ferret.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_interference_none.txt
kubectl delete jobs --all
kubectl delete pods --all

#FERRET CPU
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-ferret.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_interference_cpu.txt
kubectl delete jobs --all
kubectl delete pods --all

#FERRET L1D
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-ferret.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_interference_l1d.txt
kubectl delete jobs --all
kubectl delete pods --all

#FERRET L1I
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-ferret.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_interference_l1i.txt
kubectl delete jobs --all
kubectl delete pods --all

#FERRET L2
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-ferret.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_interference_l2.txt
kubectl delete jobs --all
kubectl delete pods --all

#FERRET LLC
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-ferret.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_interference_llc.txt
kubectl delete jobs --all
kubectl delete pods --all

#FERRET MEMBW
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-ferret.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_interference_membw.txt
kubectl delete jobs --all
kubectl delete pods --all

#FREQMINE NONE
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-freqmine.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_interference_none.txt
kubectl delete jobs --all
kubectl delete pods --all

#FREQMINE CPU
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-freqmine.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_interference_cpu.txt
kubectl delete jobs --all
kubectl delete pods --all

#FREQMINE L1D
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-freqmine.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_interference_l1d.txt
kubectl delete jobs --all
kubectl delete pods --all

#FREQMINE L1I
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-freqmine.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_interference_l1i.txt
kubectl delete jobs --all
kubectl delete pods --all

#FREQMINE L2
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-freqmine.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_interference_l2.txt
kubectl delete jobs --all
kubectl delete pods --all

#FREQMINE LLC
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-freqmine.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_interference_llc.txt
kubectl delete jobs --all
kubectl delete pods --all

#FREQMINE MEMBW
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-freqmine.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_interference_membw.txt
kubectl delete jobs --all
kubectl delete pods --all

#RADIX NONE
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_interference_none.txt
kubectl delete jobs --all
kubectl delete pods --all

#RADIX CPU
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_interference_cpu.txt
kubectl delete jobs --all
kubectl delete pods --all

#RADIX L1D
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_interference_l1d.txt
kubectl delete jobs --all
kubectl delete pods --all

#RADIX L1I
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_interference_l1i.txt
kubectl delete jobs --all
kubectl delete pods --all

#RADIX L2
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_interference_l2.txt
kubectl delete jobs --all
kubectl delete pods --all

#RADIX LLC
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_interference_llc.txt
kubectl delete jobs --all
kubectl delete pods --all

#RADIX MEMBW
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_interference_membw.txt
kubectl delete jobs --all
kubectl delete pods --all

#VIPS NONE
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-vips.yaml
sleep 300
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_interference_none.txt
kubectl delete jobs --all
kubectl delete pods --all

#VIPS CPU
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-vips.yaml
sleep 300
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_interference_cpu.txt
kubectl delete jobs --all
kubectl delete pods --all

#VIPS L1D
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-vips.yaml
sleep 300
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_interference_l1d.txt
kubectl delete jobs --all
kubectl delete pods --all

#VIPS L1I
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-vips.yaml
sleep 300
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_interference_l1i.txt
kubectl delete jobs --all
kubectl delete pods --all

#VIPS L2
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-vips.yaml
sleep 300
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_interference_l2.txt
kubectl delete jobs --all
kubectl delete pods --all

#VIPS LLC
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-vips.yaml
sleep 300
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_interference_llc.txt
kubectl delete jobs --all
kubectl delete pods --all

#VIPS MEMBW
kubectl create -f ../Part1/cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2a/parsec-vips.yaml
sleep 300
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_interference_membw.txt
kubectl delete jobs --all
kubectl delete pods --all

kops delete cluster part2a.k8s.local --yes