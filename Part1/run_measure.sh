source some_memcached_ip.txt
source node_ip.txt
cd memcache-perf
./mcperf -s $SOME_MEMCACHED_IP --loadonly
./mcperf -s $SOME_MEMCACHED_IP -a $AGENT_IP -T 16 -C 4 -D 4 -Q 1000 -c 4 -w 2 -t 5 --scan 30000:110000:5000 > memcached_no_interference.txt