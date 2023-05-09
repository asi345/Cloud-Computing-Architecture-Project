source node_vars.txt
cd memcache-perf-dynamic
./mcperf -s $MEMCACHED_INT_IP --loadonly
./mcperf -s $MEMCACHED_INT_IP -a $AGENT_INT_IP --noload -T 1 -C 1 -D 4 -Q 1000 -c 4 -t 5 --scan 5000:125000:5000 > memcached_output.txt