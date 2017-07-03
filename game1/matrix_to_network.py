import csv
import networkx as nx
import matplotlib.pyplot as plt
import re

    
def clean_string(string):
    return ' '.join(re.findall(r'[aA-zZ\.]+', string))
    
def matrix_to_network(matrix_file):
    reader = [row for row in csv.reader(open(matrix_file))]
    
    hor_agents = [clean_string(' '.join(i.split())) for i in reader[0][1:]]
    ver_agents = [clean_string(' '.join(i[0].split())) for i in reader[1:]]
    
    vals = [i[1:] for i in reader[1:]]
    
    g = nx.Graph()
    nname = matrix_file.replace('\\', '/').split('/')[-1].split('.')[0]

    for i in range(len(hor_agents)):
        for j in range(len(ver_agents)):
            try: 
                value = vals[i][j]
                
                if value != '' and value != '0':
                    g.add_edge(hor_agents[i], ver_agents[j],stance=value)
                    
            
            except:
                continue
            
    for n in g.nodes():
        g.node[n]['infected'] = False
        g.node[n]['infected_by'] = ''
        
    return (g, nname)
    
