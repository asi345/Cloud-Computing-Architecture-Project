cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part2
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
export PROJECT=`gcloud config get-value project`
kops create -f ../Part1/cloud-comp-arch-project/part2b.yaml
kops update cluster part2b.k8s.local --yes --admin
kops validate cluster --wait 10m

#n = 1
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sleep 180
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_threads_1.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_threads_1.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_threads_1.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_threads_1.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sleep 600
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_threads_1.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_threads_1.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_threads_1.txt
kubectl delete jobs --all
kubectl delete pods --all


sudo sed -i '' -e 's/native -n 1/native -n 2/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sudo sed -i '' -e 's/native -n 1/native -n 2/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sudo sed -i '' -e 's/native -n 1/native -n 2/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sudo sed -i '' -e 's/native -n 1/native -n 2/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sudo sed -i '' -e 's/native -n 1/native -n 2/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sudo sed -i '' -e 's/native -n 1/native -n 2/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sudo sed -i '' -e 's/native -n 1/native -n 2/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml

#n = 2
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sleep 180
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_threads_2.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_threads_2.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_threads_2.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_threads_2.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sleep 600
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_threads_2.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_threads_2.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_threads_2.txt
kubectl delete jobs --all
kubectl delete pods --all


sudo sed -i '' -e 's/native -n 2/native -n 4/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sudo sed -i '' -e 's/native -n 2/native -n 4/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sudo sed -i '' -e 's/native -n 2/native -n 4/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sudo sed -i '' -e 's/native -n 2/native -n 4/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sudo sed -i '' -e 's/native -n 2/native -n 4/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sudo sed -i '' -e 's/native -n 2/native -n 4/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sudo sed -i '' -e 's/native -n 2/native -n 4/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml

#n = 4
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sleep 180
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_threads_4.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_threads_4.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_threads_4.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_threads_4.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sleep 600
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_threads_4.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_threads_4.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_threads_4.txt
kubectl delete jobs --all
kubectl delete pods --all


sudo sed -i '' -e 's/native -n 4/native -n 8/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sudo sed -i '' -e 's/native -n 4/native -n 8/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sudo sed -i '' -e 's/native -n 4/native -n 8/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sudo sed -i '' -e 's/native -n 4/native -n 8/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sudo sed -i '' -e 's/native -n 4/native -n 8/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sudo sed -i '' -e 's/native -n 4/native -n 8/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sudo sed -i '' -e 's/native -n 4/native -n 8/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml

#n = 8
kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sleep 180
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_blackscholes_threads_8.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_canneal_threads_8.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_dedup_threads_8.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_ferret_threads_8.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sleep 600
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_freqmine_threads_8.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sleep 120
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_radix_threads_8.txt
kubectl delete jobs --all
kubectl delete pods --all

kubectl create -f ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml
sleep 360
kubectl get jobs > jobs.txt
python3 job_name.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$JOB_NAME --output=jsonpath='{.items[*].metadata.name}') > parsec_vips_threads_8.txt
kubectl delete jobs --all
kubectl delete pods --all


sudo sed -i '' -e 's/native -n 8/native -n 1/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-blackscholes.yaml
sudo sed -i '' -e 's/native -n 8/native -n 1/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-canneal.yaml
sudo sed -i '' -e 's/native -n 8/native -n 1/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-dedup.yaml
sudo sed -i '' -e 's/native -n 8/native -n 1/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-ferret.yaml
sudo sed -i '' -e 's/native -n 8/native -n 1/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-freqmine.yaml
sudo sed -i '' -e 's/native -n 8/native -n 1/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-radix.yaml
sudo sed -i '' -e 's/native -n 8/native -n 1/' ../Part1/cloud-comp-arch-project/parsec-benchmarks/part2b/parsec-vips.yaml

kops delete cluster part2b.k8s.local --yes