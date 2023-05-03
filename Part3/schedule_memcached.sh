#!/bin/bash
while getopts n:t:c: flag;
do
    case "$flag" in
        n) node=${OPTARG};;
        t) threads=${OPTARG};;
        c) core=${OPTARG};;
    esac
done

sudo sed -i "" -e "s/cca-project-nodetype: \"memcached\"/cca-project-nodetype: \"$node\"/" ./memcache-t1-cpuset.yaml
sudo sed -i "" -e "s/memcached -t 1/memcached -t $threads/" ./memcache-t1-cpuset.yaml
if [ "$core" != "" ]; then
    sudo sed -i "" -e "s/taskset -c 0/taskset -c $core/" ./memcache-t1-cpuset.yaml
fi

kubectl create -f ./memcache-t1-cpuset.yaml
kubectl expose pod some-memcached --name some-memcached-11211 --type LoadBalancer --port 11211 --protocol TCP

sudo sed -i "" -e "s/cca-project-nodetype: \"$node\"/cca-project-nodetype: \"memcached\"/" ./memcache-t1-cpuset.yaml
sudo sed -i "" -e "s/memcached -t $threads/memcached -t 1/" ./memcache-t1-cpuset.yaml
if [ "$core" != "" ]; then
    sudo sed -i "" -e "s/taskset -c $core/taskset -c 0/" ./memcache-t1-cpuset.yaml
fi