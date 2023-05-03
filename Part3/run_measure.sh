source memcached_ip.txt
source node_vars.txt
cd memcache-perf-dynamic
./mcperf -s $MEMCACHED_IP --loadonly
./mcperf -s $MEMCACHED_IP -a $AGENT_A_INT_IP -a $AGENT_B_INT_IP --noload -T 6 -C 4 -D 4 -Q 1000 -c 4 -t 10 --scan 30000:30500:5 > memcached_output.txt