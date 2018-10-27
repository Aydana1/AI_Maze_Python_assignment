import random
import math
import sys


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

    # MONSTER MOVING
    def moveMonster():

        monsterWaits = {}
        teleportWaits = {}

        for tick in range(0, tau):

            # MONSTER ARR
            monsters = []
            for i in range(0, totalNodes):
                if vertices[i].get_environ("monster") == 1:
                    monsters.append(i)

            tGates = []
            for i in range(0, len(monsters)):
              if vertices[monsters[i]].get_environ("teleport") == 1:
                    tGates.append(monsters[i])
              if vertices[monsters[i]].get_environ("monster") == 0:
                    monsters.remove(i)

            for i in range(0, len(monsters)):
                if monsterWaits.get(i) == "waits":
                    currMonsterAmount = vertices[monsters[i]].get_environ(
                        "monster")
                    vertices[monsters[i]].set_environ(
                        "monster", currMonsterAmount + 1)  #monster returns
                    monsterWaits.update({i: "NOTwaits"})
                if vertices[monsters[i]].get_environ("monster") == 0:
                    monsters.remove(i)

            for i in range(0, len(tGates)):
                if teleportWaits.get(i) == "waits":
                    tGates.remove(i)  # teleport gate except current
                    gateIndex = random.choice(tGates)
                    curr = vertices[gateIndex].get_environ("monster")
                    vertices[gateIndex].set_environ("monster", curr + 1)
                    tGates.append(i)  #put back
                    teleportWaits.update({i: "NOTwaits"})

            for i in range(0, len(monsters)):
                if vertices[monsters[i]].get_environ("monster") == 0:
                    monsters.remove(i)

                curr = vertices[monsters[i]].get_environ("monster")
                vertices[monsters[i]].set_environ("monster",
                                                  curr - 1)  # monster leaves

                # LONER: if own smell < curr smell
                if monsterType == "loner":
                    n = random.choice(vertices[monsters[i]].get_neihbors())
                    ncurr = vertices[n].get_environ("monster")
                    vertices[n].set_environ("monster",
                                            ncurr + 1)  #move to random node

                    maxSmell = 0
                    # CHOOSE MAX
                    for k in vertices[n].get_neihbors():
                        if maxSmell < vertices[k].get_factors("smell"):
                            maxSmell = vertices[k].get_factors("smell")
                        # update smell of this random node
                    vertices[n].set_factors("smell", maxSmell)
                    propagateSmell(vertices[n])

                    if vertices[n].get_factors(
                            "smell") < vertices[i].get_factors("smell"):
                        vertices[monsters[i]].set_environ(
                            "monster",
                            vertices[monsters[i]].get_environ("monster") +
                            1)  # return
                        vertices[n].set_environ(
                            "monster", vertices[n].get_environ("monster") - 1)

                # SOCIAL: if own smell > curr smell
                if monsterType == "social":
                    n = random.choice(vertices[monsters[i]].get_neihbors())
                    ncurr = vertices[n].get_environ("monster")
                    vertices[n].set_environ("monster",
                                            ncurr + 1)  #move to random node

                    # sum all smells of adj noes of this random node
                    totalSmell = 0
                    for k in vertices[n].get_neihbors():
                        totalSmell += vertices[k].get_factors("smell")

                    vertices[n].set_factors("smell", totalSmell)
                    propagateSmell(vertices[n])

                    if vertices[n].get_factors(
                            "smell") > vertices[i].get_factors("smell"):
                        vertices[monsters[i]].set_environ(
                            "monster",
                            vertices[monsters[i]].get_environ("monster") +
                            1)  # return
                        vertices[n].set_environ(
                            "monster", vertices[n].get_environ("monster") - 1)

                ######################################################
                if monsterType == "unknown":
                    neighbor = random.choice(
                        vertices[monsters[i]].get_neihbors())
                    curr = vertices[monsters[i]].get_environ("monster")
                    ncurr = vertices[neighbor].get_environ("monster")
                    vertices[monsters[i]].set_environ(
                        "monster", curr - 1)  #monster leaves
                    vertices[neighbor].set_environ("monster",
                                                   ncurr + 1)  # monster moves

                    propagateSmell(vertices[neighbor])  # update smell

                    if vertices[neighbor].get_environ("hole") == 1 or vertices[
                            neighbor].get_environ("wall") == 1:
                        monsterWaits.update({
                            i: "waits"
                        })  #monster must return in the enxt clock tick
                        vertices[neighbor].set_environ(
                            "monster",
                            vertices[neighbor].get_environ("monster") - 1)
                    elif vertices[neighbor].get_environ("teleport") == 1:
                        teleportWaits.update({i: "waits"})
                        vertices[neighbor].set_environ(
                            "monster",
                            vertices[neighbor].get_environ("monster") -
                            1)  #leave curr node to teleport at next tick
                        # update smell for all teleport gates as maximum
                        for g in range(0, len(tGates)):
                            vertices[tGates[g]].set_factors("smell", 1.0)

                # SUBTASK 2, LONER
                if monsterType == "loner2":
                  listt = vertices[monsters[i]].get_neihbors()
                  def moveLonerMonsterOnPairWiseBasis():
                      # base case: stop when there is only one pair left?
                      s = len(listt)

                      if s == 2:
                          return listt

                      pairs = []
                      for m in range(0, s):
                          j = m + 1
                          while (j != s):
                              pair = (listt[m], listt[j])
                              j += 1
                              pairs.append(pair)
                          j = 0
                          # print(pairs)
                          # print(" ")

                      # choose max val
                      maxVal = 0.0
                      for p in pairs:
                          if vertices[p[0]].get_factors("smell") > vertices[
                                  p[1]].get_factors("smell"):
                              if vertices[p[0]].get_factors("smell") > maxVal:
                                  maxVal = vertices[p[0]].get_factors("smell")
                          else:
                              if vertices[p[1]].get_factors("smell") > maxVal:
                                  maxVal = vertices[p[1]].get_factors("smell")
                      print(maxVal)

                      # map node indices to freq
                      freqs = {}
                      for d in range(0, len(listt)):
                          freqs.update({listt[d]: 0})

                      # iterate through pairs to see which nodes have this maxVal mostly
                      for p in pairs:
                          if maxVal == vertices[p[0]].get_factors("smell"):
                              currFreq = freqs.get(p[0])
                              maxFreq = currFreq + 1
                              freqs.update({p[0]: maxFreq})
                          elif maxVal == vertices[p[1]].get_factors("smell"):
                              currFreq = freqs.get(p[1])
                              maxFreq = currFreq + 1
                              freqs.update({p[1]: maxFreq})

                      print(freqs)

                      # eliminate this node from the list of potential places to move
                      maxF = 0
                      for f in range(0, len(listt)):
                          if maxF < freqs.get(listt[f]):
                              maxF = freqs.get(listt[f])
                              maxI = listt[f]  # max index

                      listt.remove(maxI)  # eliminate

                      moveLonerMonsterOnPairWiseBasis()  # search again

                      # print("List = ")
                      # print(listt)

                      # randomly go to one of nodes
                      room = random.choice(listt)
                      curr = vertices[monsters[i]].get_environ("monster")
                      if curr != 0:
                        vertices[monsters[i]].set_environ("monster", curr - 1)  # leave curr node
                        curr2 = vertices[room].get_environ("monster")
                        vertices[room].set_environ("monster",
                                                curr2 + 1)  # move to this node
                        propagateSmell(vertices[room])  # update the smell

                  moveLonerMonsterOnPairWiseBasis()
                
                if monsterType == "social2":
                  listt = vertices[monsters[i]].get_neihbors()
                  def moveSocialMonsterOnPairWiseBasis():
                      # base case: stop when there is only one pair left?
                      s = len(listt)

                      if s == 2:
                          return listt

                      pairs = []
                      for m in range(0, s):
                          j = m + 1
                          while (j != s):
                              pair = (listt[m], listt[j])
                              j += 1
                              pairs.append(pair)
                          j = 0
                          # print(pairs)
                          # print(" ")

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
                        vertices[maxInd].set_environ("monster", val1 - 1)
                        val2 = vertices[maxInd].get_environ("monster")
                        vertices[maxInd].set_environ("monster", val2 + 1)  #monster moves to max smell node
                        propagateSmell(vertices[maxInd])
                        # print(maxVal)

                  moveSocialMonsterOnPairWiseBasis()

    moveMonster()

    
    # WRITE FINAL CHANGE TO ANOTHER FILE
    file = open("final.txt", "w")

    for i in range(0, totalNodes):
        row = str(vertices[i].get_id()) + ":" + str(vertices[i].get_environ("wall")) + ","\
        + str(vertices[i].get_environ("hole")) + "," + str(vertices[i].get_environ("monster")) + ","\
        + str(vertices[i].get_environ("gold")) + "," + str(vertices[i].get_environ("teleport")) + ","\
        + str(vertices[i].get_factors("wind")) + ","\
        + str(vertices[i].get_factors("smell")) + " " + str(" ".join(map(str , vertices[i].get_neihbors())))

        file.write(row)
        file.write("\n")

    file.close()

    print("----------------after--------------------------")
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