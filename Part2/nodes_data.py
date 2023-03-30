out = open('node_vars.txt', 'w')
with open('nodes_data.txt') as f:
    f.readline()
    f.readline()
    line = f.readline().split()
    out.write('PARSEC_NAME="' + line[0] + '"\n')
    out.write('PARSEC_IP="' + line[6] + '"\n')
out.close()