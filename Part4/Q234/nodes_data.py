out = open('node_vars.txt', 'w')
with open('nodes_data.txt') as f:
    f.readline()
    line = f.readline().split()
    out.write('AGENT_NAME="' + line[0] + '"\n')
    out.write('AGENT_INT_IP="' + line[5] + '"\n')
    line = f.readline().split()
    out.write('MEASURE_NAME="' + line[0] + '"\n')
    out.write('MEASURE_INT_IP="' + line[5] + '"\n')
    f.readline()
    line = f.readline().split()
    out.write('MEMCACHED_NAME="' + line[0] + '"\n')
    out.write('MEMCACHED_INT_IP="' + line[5] + '"\n')
out.close()