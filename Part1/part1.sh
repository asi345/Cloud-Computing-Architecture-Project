#gsutil mb gs://cca-eth-2023-group-13-atinan/
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
cd ~/.ssh
ssh-keygen -t rsa -b 4096 -f cloud-computing
export PROJECT=`gcloud config get-value project`
cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part1
#cd to parent folder of cloud-comp-arch-project
kops create -f cloud-comp-arch-project/part1.yaml
kops create secret --name part1.k8s.local sshpublickey admin -i ~/.ssh/cloud-computing.pub
kops update cluster --name part1.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide > nodes_data.txt
python3 node_data.py
source node_ip.txt
kubectl create -f cloud-comp-arch-project/memcache-t1-cpuset.yaml
kubectl expose pod some-memcached --name some-memcached-11211 --type LoadBalancer --port 11211 --protocol TCP
sleep 60
kubectl get service some-memcached-11211
kubectl get pods -o wide > memcached_data.txt
python3 memcache_data.py
source some_memcached_ip.txt
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./init_vm.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./init_vm.sh
gcloud compute scp ./some_memcached_ip.txt ubuntu@$MEASURE_NAME:~/ --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
gcloud compute scp ./node_ip.txt ubuntu@$MEASURE_NAME:~/ --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh
sleep 75
gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf/memcached_no_interference.txt ./memcached_no_interference.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing

kubectl create -f cloud-comp-arch-project/interference/ibench-cpu.yaml
sleep 60
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh
sleep 75
gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf/memcached_no_interference.txt ./memcached_interference_ibench_cpu.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
kubectl delete pods ibench-cpu

kubectl create -f cloud-comp-arch-project/interference/ibench-l1d.yaml
sleep 60
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh
sleep 75
gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf/memcached_no_interference.txt ./memcached_interference_ibench_l1d.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
kubectl delete pods ibench-l1d

kubectl create -f cloud-comp-arch-project/interference/ibench-l1i.yaml
sleep 60
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh
sleep 75
gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf/memcached_no_interference.txt ./memcached_interference_ibench_l1i.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
kubectl delete pods ibench-l1i

kubectl create -f cloud-comp-arch-project/interference/ibench-l2.yaml
sleep 60
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh
sleep 75
gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf/memcached_no_interference.txt ./memcached_interference_ibench_l2.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
kubectl delete pods ibench-l2

kubectl create -f cloud-comp-arch-project/interference/ibench-llc.yaml
sleep 60
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh
sleep 75
gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf/memcached_no_interference.txt ./memcached_interference_ibench_llc.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
kubectl delete pods ibench-llc

kubectl create -f cloud-comp-arch-project/interference/ibench-membw.yaml
sleep 60
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh
sleep 75
gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf/memcached_no_interference.txt ./memcached_interference_ibench_membw.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
kubectl delete pods ibench-membw

kops delete cluster part1.k8s.local --yes
