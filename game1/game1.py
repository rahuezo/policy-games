from matrix_to_network import matrix_to_network as m2n2
import networkx as nx
import matplotlib.pyplot as plt
import os
import csv
from collections import OrderedDict as OD

from imtovid import *

class Game1:
    def __init__(self, network, main_node, rl=3, gop=0.7, animate=False):
        self.network = network[0]
        self.network_name = network[1] 
        
        self.main_node = main_node # this is the main player that tries to infect the network
        self.og_node = self.main_node
        self.network.node[main_node]['infected'] = True
        self.network.node[main_node]['infected_by'] = 'A'
        
        self.pos = nx.spring_layout(self.network, scale=5)
        
        self.rounds = 0 # keep track of how many rounds         
        self.infected_percentage = 0 # keep track of what percentage has been infected        
        self.number_of_conversions = 0 # keep track of how many nodes have been converted
        self.number_of_like_minded = 0 # keep track of how many like-minded nodes were infected
        
        self.images_to_remove = []
        
        self.animate = animate
        
        self.resistance_level = rl
        self.game_over_percentage = gop
            
    def has_n_infected_neighbors(self, idea, node):
        infected_count = len([n for n in self.network.neighbors(node) if self.network.node[n]['infected_by'] == idea])        
        return infected_count >= self.resistance_level
    
    def infect(self, main_node, neighbor, stance, iterator):
        
        idea = self.network.node[main_node]['infected_by']
        
        if stance == 1:
            message = "({0}, {1}) Idea: {2} Status: {3}".format(main_node, neighbor, idea, 1)
            
            print
            print message
            print
            
            self.network.node[neighbor]['infected'] = True
            self.network.node[neighbor]['infected_by'] = idea
            
            self.number_of_like_minded += 1
            
            main_node = neighbor
            iterator = 0
            neighbors = self.network.neighbors(main_node)
            return [main_node, neighbors, iterator, message]
        
        elif stance == -1 and self.has_n_infected_neighbors(idea, neighbor):
            message = "({0}, {1}) Idea: {2} Status: {3}".format(main_node, neighbor, idea, '1C')
            
            print 
            print message
            print
            
            self.network.node[neighbor]['infected'] = True
            self.network.node[neighbor]['infected_by'] = idea
            
            self.number_of_conversions += 1
            
            main_node = neighbor
            iterator = 0
            neighbors = self.network.neighbors(main_node)
            return [main_node, neighbors, iterator, message]
        else:
            message = "({0}, {1}) Idea: {2} Status: {3}".format(main_node, neighbor, idea, stance)
            
            print
            print message
            print
            
            iterator += 1
            neighbors = self.network.neighbors(main_node)
            return [main_node, neighbors, iterator, message]
        
    def get_stance(self, main_node, neighbor):
        return int(self.network[main_node][neighbor]['stance'])
    
    def is_infected(self, node):
        infected = self.network.node[node]['infected']
        infected_by = self.network.node[node]['infected_by']
        
        return (infected, infected_by)
    
    def get_infected_percentage(self):
        number_infected = len([node for node in self.network.nodes() if self.network.node[node]['infected'] == True])
        
        return round(float(number_infected)/len(self.network.nodes()), 2)
        
    def play(self):
        main_node_a = self.main_node
        a = self.network.neighbors(main_node_a)
        max_loops = len(a)
        
        i = 0
        loops = 0
        counter = 0
        
        if self.animate:
            counter = self.save_frame(counter, "{0} is the main node".format(self.main_node))
        
        self.main_node_history = [main_node_a]
        
        while i < len(a):
            
            na = a[i] # loop through neighbors
            
            infected_a = self.is_infected(na)[0] # check if current neighbor is infected
            
            # If current neighbor is not infected
            
            if infected_a == False:
                sa = self.get_stance(main_node_a, na) # get the stance between the main node and the current neighbor
                
                main_node_a, a, i, message = self.infect(main_node_a, na, sa, i) # infect current neighbor, update the main node
                                                                                 # reset iterator, store infection message
                self.rounds += 1 # since a neighbor was infected, count this as a round
                
                # save the frame if animation if enabled
                
                if self.animate:
                    counter = self.save_frame(counter, message)
                
                self.main_node_history.append(main_node_a) # add the new main node into the main node history
                
                # if all neighbors have been visited
                
                if i >= len(a):
                    
                    last_main_node, self.main_node_history = self.get_last_main_node() # change main node from history
                    
                    # Stop the game if there are no more main nodes left
                    
                    if last_main_node == None:
                        print "\nNo more nodes left to infect!\n"
                        break
                    
                    main_node_a = last_main_node # the main node is now the last main node
                    
                    a = self.network.neighbors(main_node_a) # recompute the neighbors for the new main node
                    i = 0 # restart neighbor iterator
                    
                    self.main_node_history.append(main_node_a) # add this main node to the main node history
                    
                    print "\nCan't move forward anymore. Changing main node...\n\n"
                    
                    if self.check_game_over() == True: 
                        print "\nNo more solutions!\n"
                        break
            
            # if the current neighbor is infected
            
            elif infected_a:                
                i += 1 # increase iterator and look at next neighbor
                
                # if all neighbors have been visited
                
                if i >= len(a):                    
                    last_main_node, self.main_node_history = self.get_last_main_node() # change main node from history
                    
                    # Stop the game if there are no more main nodes left
                    
                    if last_main_node == None:
                        print "\nNo more nodes left to infect!\n"
                        break
                    
                    main_node_a = last_main_node # the main node is now the last main node
                    
                    a = self.network.neighbors(main_node_a) # recompute the neighbors for the new main node
                    i = 0 # restart the neighbor iterator
                    
                    self.main_node_history.append(main_node_a) # add this main node to the main node history
                    
                    print "\nCan't move forward anymore. Changing main node...\n\n"
            
                    if self.check_game_over() == True: 
                        print "\nNo more solutions!\n"
                        break

            infected_percentage = self.get_infected_percentage()
            
            if infected_percentage >= self.game_over_percentage:
                print "\n\n\nStopping the game because over {0}% of network is infected.\n".format(self.game_over_percentage*100)
                break
        
    def infectable_left(self, main_node):
        neighbors = self.network.neighbors(main_node)
        idea = self.network.node[main_node]['infected_by']
        
        infectables = [n for n in neighbors if self.get_stance(main_node, n) == 1
                       or self.get_stance(main_node, n) == -1 and self.has_n_infected_neighbors(idea, n) == True]
        
        infected = [n for n in neighbors if self.network.node[n]['infected'] == True]
        
        return len(infectables) == len(infected)
    
    def can_infect(self, main_node):
        neighbors = self.network.neighbors(main_node)
        idea = self.network.node[main_node]['infected_by']
        
        infectables = [n for n in neighbors if self.get_stance(main_node, n) == 1 and self.network.node[n]['infected'] == False
                       or self.get_stance(main_node, n) == -1 and self.network.node[n]['infected'] == False and self.has_n_infected_neighbors(idea, n) == True]
        
        return len(infectables) > 0 
    
    def check_game_over(self):
        can_infect = [self.can_infect(n) for n in self.main_node_history]
        
        game_over = False
        
        if can_infect.count(True) == 0:
            return True
        else:
            return False
    
    def get_last_main_node(self):
        unique_history = list(OD.fromkeys(self.main_node_history)) # creates a list of the unique main nodes
        
        unique_history.reverse()
        
        for n in range(len(unique_history) - 1, -1, -1):
            status = self.can_infect(unique_history[n]) # check if this main node can still infect
            
            # if current node can still infect
            
            if status == True:
                new_main_node = unique_history[n] # this becomes the new main node
                return [new_main_node, unique_history]

        if self.infectable_left(self.og_node):
            print "This happened"
            unique_history.pop(unique_history.index(self.og_node))
            return [None, unique_history]
        else:
            return [unique_history[0], unique_history]
                
    def save_frame(self, counter, message=None):
        images_path = "{0}_images".format(self.network_name)
        
        if not os.path.exists(images_path):
            os.mkdir(images_path)
            
        current_image = '{0}/image_{1}.png'.format(images_path, counter)
            
        self.images_to_remove.append(current_image)
        
        XY = self.position_text()
        
        if message:
            plt.annotate("Round: {0} -- {1}".format(counter+1, message), xy=XY, xytext=XY)
        else: 
            plt.annotate("Round: {0}".format(counter+1), xy=XY, xytext=XY)
        
        self.show_infections(current_image)
        
        counter += 1
        
        return counter
        
    def summary(self, wd, network_name):
        try:
            
            # Show number of rounds, number of conversions, number of like-minded nodes, number of uninfected and infected
            
            all_nodes = self.network.nodes()
            
            number_infected = len([i for i in all_nodes if self.network.node[i]['infected'] == True])
            number_uninfected = len([i for i in all_nodes if self.network.node[i]['infected'] == False])
            
            self.infected_percentage = round(float(number_infected) / len(all_nodes) * 100, 2)
            print "\n" + "*"*30
            print "\nNumber of Rounds: {0}\n".format(self.rounds)
            print "\nNumber of Conversions: {0}\n".format(self.number_of_conversions)
            print "\nNumber of like-minded infections: {0}\n".format(self.number_of_like_minded)
            print "\nNumber of infected nodes: {0}\n".format(number_infected)
            print "\nNumber of uninfected nodes: {0}\n".format(number_uninfected)
            
            print "\n\nInfected % = {0}%\n".format(self.infected_percentage)
            print "\n" + "*"*30
            
            data_row = [network_name, self.rounds, self.number_of_conversions, self.number_of_like_minded, number_infected, number_uninfected, self.infected_percentage]
        
            with open(wd + '/' + 'game_rounds.csv', 'ab') as f:
                writer = csv.writer(f)
                writer.writerow(data_row)
            
        except Exception, e:
            print e
    
    def show_infections(self, img_name):
        color_map = []
        size_map = []
        labels = {}
        
        for node in self.network.nodes():
            infected_by = self.network.node[node]['infected_by']
            
            if node == self.main_node:
                size_map.append(250)
            else:
                size_map.append(50)
                
            if infected_by == 'A':
                color = '#191970'
            else:
                color = '#92e0ec'
                
            color_map.append(color)
        
        for edge in self.network.edges():
            a = edge[0]
            b = edge[1]
            
            labels[edge] = self.get_stance(a,b)
        
        
        nx.draw(self.network, pos=self.pos, node_color=color_map, node_size=size_map, edge_color='black', width=0.5, font_size=6, font_color='#cd1076', alpha=0.9)#, with_labels=True)
        nx.draw_networkx_edge_labels(self.network, pos=self.pos, edge_labels=labels, font_size=4)
        
        plt.savefig(img_name, dpi=300)
        plt.clf()
        
    def position_text(self):
        xs = []
        ys = []
        
        for pos in self.pos:
            x,y = self.pos[pos]
            
            xs.append(x)
            ys.append(y)
        
        avg_x = sum(xs)/len(xs)
        avg_y = sum(ys)/len(ys)
        
        minx = min(xs)
        maxx = max(xs)        
        x_axis = (maxx - minx)/2
        
        miny = min(ys)
        maxy = max(ys)
        y_axis = (maxy - miny)/2
        
        
        del_x = avg_x - x_axis
        del_y = avg_y - y_axis
        
        if del_x > 0: 
            chosen_x = minx #x_axis + del_x
        elif del_x < 0:
            chosen_x = maxx #x_axis - del_x
        
        if del_y > 0: 
            chosen_y = miny #y_axis + del_y
        elif del_x < 0:
            chosen_y = maxy #y_axis - del_y
        
        return (-0.2, maxy + 0.2)

        
    def remove_images(self):        
        print "Removing temp images..."
        
        for img in self.images_to_remove:
            print "Removing {0}".format(img)
            os.remove(img)
        
        print "\tFinished removing images"
    
def play_rounds(network_folder):
    wd = network_folder + '/'
    networks = [f for f in os.listdir(network_folder) if f.endswith('.csv') and 'game_rounds.csv' not in f]
    
    players_file = open(wd + '/' + 'players.txt', 'r').readlines()
    
    players = {}
    
    for player in players_file:
        network_name = player.split(',')[0].strip()
        player_name = player.split(',')[1].strip()
        
        players[network_name] = player_name
    
    for n in networks:
        network = m2n2(wd + n)
        n_name = n.split('.')[0]
        
        if n_name == 'warwick': 
            main_node = players[n_name]
            
            print "\nNetwork: {0}\tPlayer A: {1}\n".format(n_name,main_node)
            
            game = Game1(network, main_node, True)
            game.play(network, main_node)
            
            if game.animate: 
                make_movie('images', 30, '{0} game 1'.format(n_name))
                print "Waiting before image deletion"
                
                # time.sleep(10)
            
                # game.remove_images()
                
            for n in network.neighbors(main_node):
                print n, network.node[n]['infected']
        
        # game.summary(wd, n_name)

wd = r'/home/rudyhuezo/Downloads/networks_for_game1'
g = m2n2(r'C:\Users\Rudy\Downloads\game1/covert.csv')

game1 = Game1(g, "Michael G. Reynolds", animate=True, gop=0.7)
game1.play()
game1.check_game_over()

# game1.summary(wd, g[1])
make_movie('covert_images', 30, 'Covert game 1')

# nx.draw(game1.network, with_labels=True)
# plt.show()
