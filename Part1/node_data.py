out = open('node_ip.txt', 'w')
with open('nodes_data.txt') as f:
    f.readline()
    line = f.readline().split()
    out.write('AGENT_NAME="' + line[0] + '"\n')
    out.write('AGENT_IP="' + line[5] + '"\n')
    line = f.readline().split()
    out.write('MEASURE_NAME="' + line[0] + '"\n')
    out.write('MEASURE_IP="' + line[5] + '"\n')
    line = f.readline().split()
    out.write('EUR_NAME="' + line[0] + '"\n')
    out.write('EUR_IP="' + line[5] + '"\n')
    line = f.readline().split()
    out.write('MEMCACHE_NAME="' + line[0] + '"\n')
    out.write('MEMCACHE_IP="' + line[5] + '"\n')
out.close()