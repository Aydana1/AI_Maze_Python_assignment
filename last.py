import random
import math

file = open("maze.txt","w")

totalNodes = int(input("Give total num of nodes: "))
borderNodes = int(input("Give num of border nodes: "))
nonborderNodes = totalNodes - borderNodes		
print("Num of non-border nodes: {}".format(nonborderNodes))
borderEdges = int(input("Give num of border edges: "))
nonborderEdges = int(input("Give num of non-border edges: "))

if borderNodes > totalNodes or borderEdges > nonborderEdges or borderEdges < 0:
  print("Invalid inputs")
  print("Right conditions: K < N, p > k > 0")
  exit()
if ((borderNodes*borderEdges + nonborderNodes*nonborderEdges) % 2) == 0:
  pass
else:
  print("Impossible to have a maze with such parameters")
  exit()

print("N is {}, K is {}, k is {}".format(totalNodes, borderNodes, nonborderNodes))

# if hole = 1 then wind = 1
# if monster = 1 then smell = 1
# if wall = 1 then you cannot go back but can smell wind and smell


while True:
  walls = int(input("Give num of walls: "))
  holes = int(input("Give num of holes: "))
  golds = int(input("Give num of golds: "))
  monsters = int(input("Give num of monsters: "))
  # dr = float(input("Give decay rate of smell: "))
  # spreading = int(input("Give spreading rate of smell & wind: "))

  if (walls + holes + golds + monsters) > totalNodes:
    print("Total sum of attributes shouldn't exceed total num of nodes")
  else:
    print("Total sum of attributes: {}\n".format(walls + holes + golds + monsters))
    break

class Vertex:
  def __init__(self, node_id, edges):
    self.id = node_id
    self.edges = edges
    self.environ = {}
    self.neighbors = []
    self.factors = {}
  def get_id(self):
    return(self.id)
  def set_id(self, node_id):
    self.id = node_id
  def set_edges(self, edges):
    self.edges = edges
  def get_edges(self):
    return(self.edges)
  def set_environ(self, environ, value):
    self.environ.update({environ:value})
  def get_environ(self, key):
    return(self.environ.get(key, 0))
  def add_neighbors(self, neighbor):
    self.neighbors.append(neighbor)
  def get_neihbors(self):
    return(self.neighbors)
  def set_factors(self, factor, value):
    self.factors.update({factor:value})
  def get_factors(self, key):
    return(self.factors.get(key, 0))
  def print_results(self):
    print("{}:{},{},{}\n".format(self.id, self.environ, self.factors, self.neighbors))

# INDEXING NODES AND ASSIGNING EDGES
vertices = []
node_id = 0
while node_id < borderNodes:
  vertices.append(Vertex(node_id, borderEdges))
  vertices[node_id].set_environ("wall", 0)
  vertices[node_id].set_environ("hole", 0)
  vertices[node_id].set_environ("monster", 0)
  vertices[node_id].set_environ("gold", 0)
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
      min_edges = vertices[t].get_edges() # save curr min num of edges
      min_ind = t # save index of node with min num of edges
    t += 1

  # loop through all nodes until you find the first node with max num of edges
  for y in range(0, totalNodes):
    if (y == min_ind) or (y in vertices[min_ind].get_neihbors()):
      pass
    elif vertices[y].get_edges() > max_edges:
      max_edges = vertices[y].get_edges() # save curr max num of edges
      max_ind = y # save index of node with max num of edges
    y += 1
  # border nodes are connected only with nonborder nodes
  vertices[min_ind].add_neighbors(max_ind)  # connect border node with nonborder node 
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

while len(room_attributes) != totalNodes:
	room_attributes.append("none")   # fill empty places in case sum of attributes < N

j = 0
while j < totalNodes:
  prop = random.choice(room_attributes)  # randomly assign envirnomnet to rooms
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
    # elif environ == "wall":
    #   if vertices[i].get_environ(environ) == 1:
    #     vertices[i].set_factors("wind", 1)
    #     vertices[i].set_factors("smell", 1)

#print(" ".join(map(str , vertices[0].get_neihbors())))

addFactors("monster")
addFactors("hole")
#addFactors("wall")

for i in range(0, totalNodes):
  #vertices[i].print_results()
  print("{}:{},{},{},{},{},{} {}\n".format(vertices[i].get_id(), vertices[i].get_environ("wall"), 
    vertices[i].get_environ("hole"), 
    vertices[i].get_environ("monster"),
    vertices[i].get_environ("gold"), vertices[i].get_factors("wind"), vertices[i].get_factors("smell"), 
    " ".join(map(str , vertices[i].get_neihbors()))))
  i += 1

# WRITE THE MAZE TO FILE
for i in range(0, totalNodes):
  row = str(vertices[i].get_id()) + ":" + str(vertices[i].get_environ("wall")) + ","\
  + str(vertices[i].get_environ("hole")) + "," + str(vertices[i].get_environ("monster")) + ","\
  + str(vertices[i].get_environ("gold")) + "," + str(vertices[i].get_factors("wind")) + ","\
  + str(vertices[i].get_factors("smell")) + " " + str(" ".join(map(str , vertices[i].get_neihbors())))
  file.write(row)
  file.write("\n")  


file.close()

