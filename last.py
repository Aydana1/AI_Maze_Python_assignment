import random
import math
import sys
import decimal

class Vertex:
    def __init__(self, node_id, edges):
        self.id = node_id
        self.edges = edges
        self.environ = {}
        self.neighbors = []
        self.factors = {}

    def get_id(self):
        return (self.id)

    def set_id(self, node_id):
        self.id = node_id

    def set_edges(self, edges):
        self.edges = edges

    def get_edges(self):
        return (self.edges)

    def set_environ(self, environ, value):
        self.environ.update({environ: value})

    def get_environ(self, key):
        return (self.environ.get(key, 0))

    def add_neighbors(self, neighbor):
        self.neighbors.append(neighbor)

    def get_neihbors(self):
        return (self.neighbors)

    def set_factors(self, factor, value):
        self.factors.update({factor: value})

    def get_factors(self, key):
        return (self.factors.get(key, 0))

    def print_results(self):
        print("{}:{},{},{}\n".format(self.id, self.environ, self.factors,
                                     self.neighbors))

class Agent:
    def __init__(self, node_id):
        self.id = node_id

    def get_position(self):
        return self.id
    
    def set_position(self, node_id):
        self.id = node_id
        

# INITIALIZING THE MAZE
def initMaze(totalNodes, borderNodes, borderEdges, nonborderEdges, monsters,
             walls, holes, golds, t_gates, dr, spreading):
    vertices = []
    node_id = 0
    while node_id < borderNodes:
        vertices.append(Vertex(node_id, borderEdges))
        vertices[node_id].set_environ("wall", 0)
        vertices[node_id].set_environ("hole", 0)
        vertices[node_id].set_environ("monster", 0)
        vertices[node_id].set_environ("gold", 0)
        vertices[node_id].set_environ("teleport", 0)
        vertices[node_id].set_factors("wind", 0.0)
        vertices[node_id].set_factors("smell", 0.0)
        node_id += 1

    i_id = node_id
    while i_id < totalNodes:
        vertices.append(Vertex(i_id, nonborderEdges))
        vertices[i_id].set_environ("wall", 0)
        vertices[i_id].set_environ("hole", 0)
        vertices[i_id].set_environ("monster", 0)
        vertices[i_id].set_environ("gold", 0)
        vertices[i_id].set_environ("teleport", 0)
        vertices[i_id].set_factors("wind", 0.0)
        vertices[i_id].set_factors("smell", 0.0)
        i_id += 1

    # CONNECTING ALL NODES
    increm = 0
    while increm != totalNodes:
        min_edges = 100
        max_edges = 0
        # loop through all nodes until you find the first node with min num of edges
        for t in range(0, totalNodes):
            if vertices[t].get_edges() == 0:
                pass
            elif vertices[t].get_edges() < min_edges:
                min_edges = vertices[t].get_edges(
                )  # save curr min num of edges
                min_ind = t  # save index of node with min num of edges
            t += 1

        # loop through all nodes until you find the first node with max num of edges
        for y in range(0, totalNodes):
            if (y == min_ind) or (y in vertices[min_ind].get_neihbors()):
                pass
            elif vertices[y].get_edges() > max_edges:
                max_edges = vertices[y].get_edges(
                )  # save curr max num of edges
                max_ind = y  # save index of node with max num of edges
            y += 1
        # border nodes are connected only with nonborder nodes
        vertices[min_ind].add_neighbors(
            max_ind)  # connect border node with nonborder node
        vertices[max_ind].add_neighbors(min_ind)
        # decrement max and min num of edges to exclude already connected nodes
        curr_min_edges = vertices[min_ind].get_edges()
        curr_max_edges = vertices[max_ind].get_edges()
        vertices[min_ind].set_edges(curr_min_edges - 1)
        vertices[max_ind].set_edges(curr_max_edges - 1)

        increm = 0
        i = 0
        while i < totalNodes:
            if vertices[i].get_edges() == 0:
                increm += 1
            i += 1

    room_attributes = []
    for i in range(0, walls):
        room_attributes.append("wall")
    for i in range(0, holes):
        room_attributes.append("hole")
    for i in range(0, golds):
        room_attributes.append("gold")
    for i in range(0, monsters):
        room_attributes.append("monster")
    for i in range(0, t_gates):
        room_attributes.append("teleport")

    while len(room_attributes) != totalNodes:
        room_attributes.append(
            "none")  # fill empty places in case sum of attributes < N

    j = 0
    while j < totalNodes:
        prop = random.choice(
            room_attributes)  # randomly assign envirnomnet to rooms
        room_attributes.remove(prop)
        vertices[j].set_environ(prop, 1)
        j += 1

    def addFactors(environ):
        for i in range(0, totalNodes):
            if environ == "hole":
                if vertices[i].get_environ(environ) == 1:
                    vertices[i].set_factors("wind", 1.0)
            elif environ == "monster":
                if vertices[i].get_environ(environ) == 1:
                    vertices[i].set_factors("smell", 1.0)

    addFactors("monster")
    addFactors("hole")

    # for i in range(0, totalNodes):
    #   print("{}:{},{},{},{},{},{},{} {}\n".format(vertices[i].get_id(), vertices[i].get_environ("wall"),
    #     vertices[i].get_environ("hole"),
    #     vertices[i].get_environ("monster"),
    #     vertices[i].get_environ("gold"), vertices[i].get_environ("teleport"),
    #     vertices[i].get_factors("wind"), vertices[i].get_factors("smell"),
    #     " ".join(map(str , vertices[i].get_neihbors()))))
    #   i += 1

    # WRITE THE MAZE TO FILE
    file = open("maze.txt", "w")

    for i in range(0, totalNodes):
        row = str(vertices[i].get_id()) + ":" + str(vertices[i].get_environ("wall")) + ","\
        + str(vertices[i].get_environ("hole")) + "," + str(vertices[i].get_environ("monster")) + ","\
        + str(vertices[i].get_environ("gold")) + "," + str(vertices[i].get_environ("teleport")) + ","\
        + str(vertices[i].get_factors("wind")) + ","\
        + str(vertices[i].get_factors("smell")) + " " + str(" ".join(map(str , vertices[i].get_neihbors())))

        file.write(row)
        file.write("\n")

    file.close()


# LOADING THE MAZE
def loadMaze(file, dr, spreading, tau, monsterType):
    vertices = []

    with open(file) as f:
        for line in f:
            line = line.strip()
            tokens = line.split(':')
            idd = int(tokens[0])
            v = Vertex(idd, 2)
            wall = int(tokens[1].split(",")[0])
            hole = int(tokens[1].split(",")[1])
            monster = int(tokens[1].split(",")[2])
            gold = int(tokens[1].split(",")[3])
            teleport = int(tokens[1].split(",")[4])
            wind = float(tokens[1].split(",")[5])
            pieces = tokens[1].split(",")[6].split(" ")
            smell = float(pieces[0])
            v.set_environ("wall", wall)
            v.set_environ("hole", hole)
            v.set_environ("monster", monster)
            v.set_environ("gold", gold)
            v.set_environ("teleport", teleport)
            v.set_factors("wind", wind)
            v.set_factors("smell", smell)
            j = 1

            while (j != len(pieces)):
                v.add_neighbors(int(pieces[j]))
                j += 1

            vertices.append(v)

    # for i in range(0, len(vertices)):
    #   print(vertices[i].get_neihbors())

    totalNodes = len(vertices)

    # # PRINTING
    def printNode(node):
        print("{}:{},{},{},{},{},{},{} {}\n".format(
            node.get_id(), node.get_environ("wall"), node.get_environ("hole"),
            node.get_environ("monster"), node.get_environ("gold"),
            node.get_environ("teleport"), node.get_factors("wind"),
            node.get_factors("smell"), " ".join(map(str,
                                                    node.get_neihbors()))))

    # CALCULATE WIND AND SMELL
    visited = []
    max_wind_vals = []
    max_smell_vals = []

    for i in range(0, totalNodes):
        visited.append(False)
        max_wind_vals.append(0.0)
        max_smell_vals.append(0.0)

    def spreadSmell(node, spreading, dr, dist, curr_smell):
        visited[node.get_id()] = True
        max_smell = max(curr_smell, max_smell_vals[node.get_id()])
        max_smell_vals[node.get_id()] = max_smell
        if dist == spreading:
            return
        else:
            for neighbor in node.get_neihbors():
                if not visited[neighbor]:
                    visited[neighbor] = True
                    spreadSmell(vertices[neighbor], spreading, dr, dist + 1,
                                dr * curr_smell)
                    # print("Smell propagated to " + str(neighbor))
                    # printNode(vertices[neighbor])
                    for j in range(0, totalNodes):
                        visited[j] = False

    def spreadWind(node, spreading, dr, dist, curr_wind):
        visited[node.get_id()] = True
        max_wind = max(curr_wind, max_wind_vals[node.get_id()])
        max_wind_vals[node.get_id()] = max_wind
        if dist == spreading:
            return
        else:
            for neighbor in node.get_neihbors():
                if not visited[neighbor]:
                    visited[neighbor] = True
                    spreadWind(vertices[neighbor], spreading, dr, dist + 1,
                               dr * curr_wind)
                    for j in range(0, totalNodes):
                        visited[j] = False

    def calculateSmell():
        i = 0
        dist = 0
        while i < totalNodes:
            curr_smell = vertices[i].get_factors("smell")
            if vertices[i].get_environ("monster") == 1:
                spreadSmell(vertices[i], spreading, dr, dist, curr_smell)
            for j in range(0, totalNodes):
                visited[j] = False
            i += 1

        for s in range(0, totalNodes):
            vertices[s].set_factors("smell", max_smell_vals[s])

    def calculateWind():
        i = 0
        dist = 0
        while i < totalNodes:
            curr_wind = vertices[i].get_factors("wind")
            if vertices[i].get_environ("hole") == 1:
                spreadWind(vertices[i], spreading, dr, dist, curr_wind)
            for j in range(0, totalNodes):
                visited[j] = False
            i += 1

        for s in range(0, totalNodes):
            vertices[s].set_factors("wind", max_wind_vals[s])

    calculateSmell()
    calculateWind()

    def propagateSmell(node):
        curr_smell = node.get_factors("smell")
        # print("SMELL = " + str(curr_smell) + " of " + str(node.get_id()))
        spreadSmell(node, spreading, dr, 0, curr_smell)

    print("----------------before monsters move-------------------------")
    for i in range(0, totalNodes):
        print("{}:{},{},{},{},{},{},{} {}\n".format(
            vertices[i].get_id(), vertices[i].get_environ("wall"),
            vertices[i].get_environ("hole"),
            vertices[i].get_environ("monster"),
            vertices[i].get_environ("gold"),
            vertices[i].get_environ("teleport"),
            vertices[i].get_factors("wind"), vertices[i].get_factors("smell"),
            " ".join(map(str, vertices[i].get_neihbors()))))
        i += 1

    # INITIAL POSITION OF AGENT
    file = open("agent.txt", "w")

    random_node = random.choice(vertices)
    agent = Agent(random_node.get_id())
    print("Agent initial position: " + str(agent.get_position()))
    row = "Agent initial position: " + str(agent.get_position())
    file.write(row)
    file.write("\n")

    # DICTIONARY: key = [PERCEPT SEQUENCE], value =  [NEIGHBOR NODES]
    percepts = {}
    deaths = {}
    deaths_counts = []
    transitions = {}
    
    # RANDOM MONSTER MOVING
    def moveMonster():
        for y in range(0, 100):
            print("level: " + str(y))
            row = "level: " + str(y)
            file.write(row)
            file.write("\n")
            monsterWaits = {}
            teleportWaits = {}
            killed = False
            
            while killed == False:
                monsters = []
                for i in range(0, totalNodes):
                    if vertices[i].get_environ("monster") >= 1:
                        monsters.append(i)

                    for i in range(0, len(monsters)):
                        if monsterType == "social":
                            listt = vertices[monsters[i]].get_neihbors()
                            def moveSocialMonsterOnPairWiseBasis():
                            # base case: stop when there is only one pair left?
                                s = len(listt)
                                if s == 1:
                                    return listt

                                pairs = []
                                for m in range(0, s):
                                    j = m + 1
                                    while (j != s):
                                        pair = (listt[m], listt[j])
                                        j += 1
                                        pairs.append(pair)
                                    j = 0
                            
                                # choose max val
                                maxVal = 0.0
                                for p in pairs:
                                    if vertices[p[0]].get_factors("smell") > vertices[
                                        p[1]].get_factors("smell"):
                                        if vertices[p[0]].get_factors("smell") > maxVal:
                                            maxVal = vertices[p[0]].get_factors("smell")
                                            maxInd = p[0]
                                    else:
                                        if vertices[p[1]].get_factors("smell") > maxVal:
                                            maxVal = vertices[p[1]].get_factors("smell")
                                            maxInd = p[1]

                                val1 = vertices[monsters[i]].get_environ("monster")
                                if val1 != 0:
                                    vertices[monsters[i]].set_environ("monster", val1 - 1)   # MISTAKE FOUND!
                                    val2 = vertices[maxInd].get_environ("monster")
                                    vertices[maxInd].set_environ("monster", val2 + 1)  #monster moves to max smell node
                                    propagateSmell(vertices[maxInd])
                                    # print(maxVal)
                            moveSocialMonsterOnPairWiseBasis()

        
                #agent movement
                init_agent_pos = agent.get_position()
                              
                listt = vertices[init_agent_pos].get_neihbors()
                true_neighbors = []
                for p in range(0, len(listt)):
                    true_neighbors.append(listt[p])
                print("TRUE: " + str(true_neighbors))
                print("LIST: " + str(listt))
                count = 0
                max_smells = []
                # base case: stop when there is only one pair left?
                s = len(listt)
                print("SIZE=" + str(s))
                for u in range(0, s):
                    l = len(listt)

                    if l == 2:
                        break

                    pairs = []
                    for m in range(0, l):
                        j = m + 1
                        while (j != l):
                            pair = (listt[m], listt[j])
                            j += 1
                            pairs.append(pair)
                        j = 0
                    print("PAIRS=" + str(pairs))
                    
                    max_smell = 0.0
                    for p in pairs:
                        print("SMELLS=" + "(" + str(vertices[p[0]].get_factors("smell")) + ", " + str(vertices[p[1]].get_factors("smell")) + "),")
                        if count == 0:
                            if vertices[p[0]].get_factors("smell") >= vertices[p[1]].get_factors("smell"):
                                max_smell = vertices[p[0]].get_factors("smell")
                                max_smells.append(max_smell)
                                
                            else:
                                max_smell = vertices[p[1]].get_factors("smell")
                                max_smells.append(max_smell)
                    print("pairs " + str(max_smells))
                    # choose max val

                          
                    maxVal = 0.0
                    for p in pairs:
                        if vertices[p[0]].get_factors("smell") > vertices[p[1]].get_factors("smell"):
                            if vertices[p[0]].get_factors("smell") > maxVal:
                                maxVal = vertices[p[0]].get_factors("smell")
                        else:
                            if vertices[p[1]].get_factors("smell") > maxVal:
                                maxVal = vertices[p[1]].get_factors("smell")
                    #print(maxVal)

                    # map node indices to freq
                    freqs = {}
                    for d in range(0, len(listt)):
                        freqs.update({listt[d]: 0})

                    # iterate through pairs to see which nodes have this maxVal mostly
                    for p in pairs:
                        if maxVal == vertices[p[0]].get_factors("smell"):
                            currFreq = freqs.get(p[0])
                            minFreq = currFreq + 1
                            freqs.update({p[0]: minFreq})
                        elif maxVal == vertices[p[1]].get_factors("smell"):
                            currFreq = freqs.get(p[1])
                            minFreq = currFreq + 1
                            freqs.update({p[1]: minFreq})

                    #print(freqs)

                    # eliminate this node from the list of potential places to move
                    minF = 10000000
                    for f in range(0, len(listt)):
                        if minF > freqs.get(listt[f]):
                            minF = freqs.get(listt[f])
                            minI = listt[f]  # max index
                    if minI in listt:
                        listt.remove(minI)  # eliminate
                        print("LIST: " + str(listt))
                    count += 1
                
                #moveAgentOnPairWiseBasis(y, count)  # search again

                # randomly go to one of nodes
                random_node = random.choice(listt)
                agent.set_position(random_node)
                curr_agent_pos = agent.get_position()
                print("Agent moved to: " + str(curr_agent_pos))
                row = "Agent moved to: " + str(curr_agent_pos)
                file.write(row)
                file.write("\n")
                single_transition = (init_agent_pos, curr_agent_pos)
                curr_val = transitions.get(single_transition, 0)
                transitions.update({single_transition:curr_val+1})
                print("TRANSITIONS: " + str(transitions))
                #--------------------------------------------------#
                actions = ["killed", "found gold", "fall into a hole"]
                if vertices[curr_agent_pos].get_environ("monster") >= 1:
                    y += 1
                    print("{}, {}, {}, {}, {}, {}, {}: {}".format(curr_agent_pos, vertices[curr_agent_pos].get_environ("wall"), 
                        vertices[curr_agent_pos].get_environ("monster"), vertices[curr_agent_pos].get_environ("hole"), vertices[curr_agent_pos].get_environ("gold"),
                        vertices[curr_agent_pos].get_factors("wind"), vertices[curr_agent_pos].get_factors("smell"),
                        actions[0]))
                    row = str(vertices[curr_agent_pos].get_id()) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("hole")) + ", " + str(vertices[curr_agent_pos].get_environ("gold")) + ", " + str(vertices[curr_agent_pos].get_factors("wind")) + ", " + str(vertices[curr_agent_pos].get_factors("smell")) + ": " + actions[0]
                    file.write(row)
                    file.write("\n")
                    killed = True
                    
                    curr_counter = deaths.get(curr_agent_pos, 0)
                    deaths.update({curr_agent_pos:curr_counter+1})
                    print("DEATHS: " + str(deaths))

                    #return
                    #break
                # if hole, return
                elif vertices[curr_agent_pos].get_environ("hole") == 1:
                    agent.set_position(init_agent_pos)
                    print("Agent returned to: " + str(init_agent_pos))
                    print("{}, {}, {}, {}, {}, {}, {}: {}".format(curr_agent_pos, vertices[curr_agent_pos].get_environ("wall"), 
                        vertices[curr_agent_pos].get_environ("monster"), vertices[curr_agent_pos].get_environ("hole"), vertices[curr_agent_pos].get_environ("gold"),
                        vertices[curr_agent_pos].get_factors("wind"), vertices[curr_agent_pos].get_factors("smell"),
                        actions[2]))
                    y += 1
                    row = str(vertices[curr_agent_pos].get_id()) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("hole")) + ", " + str(vertices[curr_agent_pos].get_environ("gold")) + ", " + str(vertices[curr_agent_pos].get_factors("wind")) + ", " + str(vertices[curr_agent_pos].get_factors("smell")) + ": " + actions[2]
                    file.write(row)
                    file.write("\n")
                    #break
                    #killed = True
                    #return
                    #  if wall, return
                elif vertices[curr_agent_pos].get_environ("wall") == 1:
                    agent.set_position(init_agent_pos)
                    print("Agent returned to: " + str(init_agent_pos))
                    print("{}, {}, {}, {}, {}, {}, {}: {}".format(curr_agent_pos, vertices[curr_agent_pos].get_environ("wall"), 
                        vertices[curr_agent_pos].get_environ("monster"), vertices[curr_agent_pos].get_environ("hole"), vertices[curr_agent_pos].get_environ("gold"),
                        vertices[curr_agent_pos].get_factors("wind"), vertices[curr_agent_pos].get_factors("smell"),
                        actions[2]))
                    y += 1
                    row = str(vertices[curr_agent_pos].get_id()) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("hole")) + ", " + str(vertices[curr_agent_pos].get_environ("gold")) + ", " + str(vertices[curr_agent_pos].get_factors("wind")) + ", " + str(vertices[curr_agent_pos].get_factors("smell")) + ": " + actions[2]
                    file.write(row)
                    file.write("\n")
                    #killed = True
                    #break
                elif vertices[curr_agent_pos].get_environ("gold") == 1:
                    vertices[curr_agent_pos].set_environ("gold", 0)  # agent picks up the gold
                    print("{}, {}, {}, {}, {}, {}, {}: {}".format(curr_agent_pos, vertices[curr_agent_pos].get_environ("wall"), 
                        vertices[curr_agent_pos].get_environ("monster"), vertices[curr_agent_pos].get_environ("hole"), vertices[curr_agent_pos].get_environ("gold"),
                        vertices[curr_agent_pos].get_factors("wind"), vertices[curr_agent_pos].get_factors("smell"), 
                        actions[1]))
                    row = str(vertices[curr_agent_pos].get_id()) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("monster")) + ", " + str(vertices[curr_agent_pos].get_environ("hole")) + ", " + str(vertices[curr_agent_pos].get_environ("gold")) + ", " + str(vertices[curr_agent_pos].get_factors("wind")) + ", " + str(vertices[curr_agent_pos].get_factors("smell")) + ": " + actions[1]
                    file.write(row)
                    file.write("\n")
                    y += 1
                    #break
                    #killed = True

                percept_sequence = tuple(max_smells)                    
                nodes = {} # maps neighbor nodes to death counts
                # true_neighbors = vertices[init_agent_pos].get_neihbors()
                if len(true_neighbors) > 1:
                    for k in range(0, len(true_neighbors)):
                        count = deaths.get(true_neighbors[k], 0)
                        #print("FOR ID = " + str(true_neighbors[k]))
                        #print("COUNT= " + str(count))
                        nodes.update({true_neighbors[k]:count})
                        #print("NODES: " + str(nodes))
                    if len(percept_sequence) != 0:
                        percepts.update({percept_sequence:nodes})
                    print("percept sequence: " + str(percept_sequence))
                    print("PERCEPTS: " +str(percepts))

                
        #move_agent_randomly(y)
            print("-----------------------------")
            row = "-----------------------------"
            file.write(row)
            file.write("\n")
        file.close()

    moveMonster()
    
    # CONSTRUCT SENSOR TABLE
    for key, value in percepts.items():
        print(str(key) + " - " + str(value))

    def train_the_agent():
        total_trans = len(transitions)
        #trans_prob = []
        for trans_key, value in transitions.items():
            #print("trans = " + str(key) + " : " + str(value))
            #prob1 = decimal.Decimal(value) / decimal.Decimal(total_trans)
            prob1 = float(value) / float(total_trans)
            print("prob1 = " + str(prob1))
            #print(trans_key[1])
            #trans_prob.append(prob1)
        #print(trans_prob)
        
            for percepts_key, nodes in percepts.items(): 
                curr_neighbors = nodes
                total_deaths = 0
                for i in range(0, len(curr_neighbors)):
                    for node_key, deaths in curr_neighbors.items():
                        total_deaths += deaths
                    for node_key, deaths in curr_neighbors.items():
                        
                        if trans_key[1] == node_key:
                            print(curr_neighbors)
                            print(node_key)
                            if deaths == 0 or total_deaths == 0:
                                prob2 = 0
                            else:     
                                prob2 = float(deaths) / float(total_deaths)   # death / total_deaths
                            #print("prob2 = " + str(prob2))    
                            prob = prob1 * prob2
                            #print("TOTAL PROB = " + str(prob))
                

    
    #train_the_agent()


    # WRITE FINAL CHANGE TO ANOTHER FILE
    # file = open("final.txt", "w")

    # for i in range(0, totalNodes):
    #     row = str(vertices[i].get_id()) + ":" + str(vertices[i].get_environ("wall")) + ","\
    #     + str(vertices[i].get_environ("hole")) + "," + str(vertices[i].get_environ("monster")) + ","\
    #     + str(vertices[i].get_environ("gold")) + "," + str(vertices[i].get_environ("teleport")) + ","\
    #     + str(vertices[i].get_factors("wind")) + ","\
    #     + str(vertices[i].get_factors("smell")) + " " + str(" ".join(map(str , vertices[i].get_neihbors())))

    #     file.write(row)
    #     file.write("\n")

    # file.close()

    # print("----------------after--------------------------")
    # for i in range(0, totalNodes):
    #     print("{}:{},{},{},{},{},{},{} {}\n".format(
    #         vertices[i].get_id(), vertices[i].get_environ("wall"),
    #         vertices[i].get_environ("hole"),
    #         vertices[i].get_environ("monster"),
    #         vertices[i].get_environ("gold"),
    #         vertices[i].get_environ("teleport"),
    #         vertices[i].get_factors("wind"), vertices[i].get_factors("smell"),
    #         " ".join(map(str, vertices[i].get_neihbors()))))
    #     i += 1


# READING FROM COMMAND LINE
if len(sys.argv) > 7:
    functionCall = eval(sys.argv[1])
    totalNodes = int(sys.argv[2])
    borderNodes = int(sys.argv[3])
    nonborderNodes = totalNodes - borderNodes
    borderEdges = int(sys.argv[4])
    nonborderEdges = int(sys.argv[5])
    monsters = int(sys.argv[6])
    walls = int(sys.argv[7])
    holes = int(sys.argv[8])
    golds = int(sys.argv[9])
    t_gates = int(sys.argv[10])
    dr = float(sys.argv[11])
    spreading = int(sys.argv[12])

    if borderNodes > totalNodes or borderEdges > nonborderEdges or borderEdges < 0:
        print("Invalid inputs")
        print("Right conditions: K < N, p > k > 0")
        exit()
    if ((borderNodes * borderEdges + nonborderNodes * nonborderEdges) %
            2) == 0:
        pass
    else:
        print("Impossible to have a maze with such parameters")
        exit()

    #print("N is {}, K is {}, k is {}".format(totalNodes, borderNodes, nonborderNodes))

    if (walls + holes + golds + monsters + t_gates) > totalNodes:
        print("Total sum of attributes shouldn't exceed total num of nodes")
        exit()
    #else:
    #print("Total sum of attributes: {}\n".format(walls + holes + golds + monsters))

    print(
        functionCall(totalNodes, borderNodes, borderEdges, nonborderEdges,
                     monsters, walls, holes, golds, t_gates, dr, spreading))

else:
    func = eval(sys.argv[1])
    f = sys.argv[2]
    spreading = int(sys.argv[4])
    dr = float(sys.argv[3])
    tau = int(sys.argv[5])
    monsterType = str(sys.argv[6])

    print(func(f, dr, spreading, tau, monsterType))