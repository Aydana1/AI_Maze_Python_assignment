import sys
from last import *

def loadMaze(file, dr, spreading):
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
      wind = float(tokens[1].split(",")[4])
      pieces = tokens[1].split(",")[5].split(" ")
      smell = float(pieces[0])
      v.set_environ("wall", wall)
      v.set_environ("hole", hole)
      v.set_environ("monster", monster)
      v.set_environ("gold", gold)
      v.set_factors("wind", wind)
      v.set_factors("smell", smell)
      j = 1

      while(j != len(pieces)):
        v.add_neighbors(int(pieces[j]))
        j += 1

      vertices.append(v)

  # for i in range(0, len(vertices)):
  #   print(vertices[i].get_neihbors())

  totalNodes = len(vertices)
  # CALCULATE WIND AND SMELL 
  visited = []
  max_wind_vals = []
  max_smell_vals = []

  for i in range(0, totalNodes):
    visited.append(False)
    max_wind_vals.append(0.0)
    max_smell_vals.append(0.0)

  def spreadWindSmell(node, spreading, dr, dist, curr_wind, curr_smell):
    visited[node.get_id()] = True
    max_wind = max(curr_wind, max_wind_vals[node.get_id()])
    max_wind_vals[node.get_id()] = max_wind
    max_smell = max(curr_smell, max_smell_vals[node.get_id()])
    max_smell_vals[node.get_id()] = max_smell
    if dist == spreading:
      return
    else:
      for neighbor in node.get_neihbors():
        # print("node {} for vertex {}".format(neighbor, node.get_id()))
        if not visited[neighbor]:
          visited[neighbor] = True
          spreadWindSmell(vertices[neighbor], spreading, dr, dist+1, dr*curr_wind, dr*curr_smell)
          for j in range(0, totalNodes):
            visited[j] = False

  def calculateWindSmell():
    i = 0
    dist = 0
    while i < totalNodes:
      curr_smell = vertices[i].get_factors("smell")
      curr_wind = vertices[i].get_factors("wind")
      if vertices[i].get_environ("monster") == 1 or vertices[i].get_environ("hole") == 1:
        spreadWindSmell(vertices[i], spreading, dr, dist, curr_wind, curr_smell)
      for j in range(0, totalNodes):
        visited[j] = False
      i += 1

    for s in range(0, totalNodes):
      vertices[s].set_factors("wind", max_wind_vals[s])
      vertices[s].set_factors("smell", max_smell_vals[s])

  calculateWindSmell()

  # # PRINTING
  for i in range(0, totalNodes):
    print("{}:{},{},{},{},{},{} {}\n".format(vertices[i].get_id(), vertices[i].get_environ("wall"), 
      vertices[i].get_environ("hole"), 
      vertices[i].get_environ("monster"),
      vertices[i].get_environ("gold"), vertices[i].get_factors("wind"), vertices[i].get_factors("smell"), 
      " ".join(map(str , vertices[i].get_neihbors()))))
    i += 1


func = eval(sys.argv[1])
f = sys.argv[2]
spreading = int(sys.argv[3])
dr = float(sys.argv[4])

print(func(f, dr, spreading))
