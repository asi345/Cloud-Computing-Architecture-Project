source node_vars.txt
cd memcache-perf-dynamic
./mcperf -s $MEMCACHED_INT_IP --loadonly
./mcperf -s $MEMCACHED_INT_IP -a $AGENT_INT_IP --noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 1200 --qps_interval 10 --qps_min 5000 --qps_max 100000 --qps_seed 3274 > memcached_output.txt