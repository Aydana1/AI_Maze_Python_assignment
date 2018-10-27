I have initMaze and loadMaze functions in one file "last.py".
There're also functions for smell&wind calculation, printing, monster moving, smell propagation.

Commands for running the program:
cd aidana_maze/proj
For initializing the maze, run:
python last.py initMaze N K k p M W H G T decay spreading
E.g: python last.py initMaze 30 10 2 4 6 5 3 2 3 0.5 2

For loading from the file, run:
python last.py loadMaze maze.txt decay spreading tau monsterType
E.g: python last.py loadMaze maze.txt 0.5 2 5 social

Note: There're 5 monster types: social, loner, unknown, social2, loner2
If input is "social2" or "loner2", smell is calculated on pairwise basis.
In case of "unknown" monster, configurations of previous assignment will be applied.

Final change of the maze is saved in "final.txt".
