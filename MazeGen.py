# Maze generation program inspired by Olin Shivers' maze algorithm
# http://www.ccs.neu.edu/home/shivers/mazes.html
#
# To run
# python MazeGen.py > my_output_maze.ps
#
# To get a maze of a different size, change the arguments
# to the constructor to MazeGen supplied at the end of this file

import random
import sys

class MazeGen:
    def __init__(self, w_, h_):
        self.numsets = w_ * h_
        self.w = w_
        self.h = h_
        # Uses disjoint-set unionfind
        # self.sets is the mapping from each grid cell
        # to its set representative.
        # Grid cells are indexed by integer
        self.sets = [i for i in range(0, self.numsets)]
        self.doorways = {}

    # Finds the set representative for a given cell
    def setrep(self, i):
        result = i
        while self.sets[result] != result:
            result = self.sets[result]
        trav = i
        while trav != result:
            nxt = self.sets[trav]
            self.sets[trav] = result
            trav = nxt
        return result

    # Merges two sets (for the purposes of tracking
    # connectivity)
    def merge(self, i, j):
        if (self.setrep(i) == self.setrep(j)):
            return self.setrep(i)
        self.numsets -= 1
        self.sets[self.setrep(i)] = self.setrep(j)
        return self.setrep(i)

    # Tries to knock down a wall between two grid cells.
    # Updates connected-item set information if successful.
    def make_door(self, i, j):
        if (i >= (self.w * self.h) or j >= (self.w * self.h) or i == j):
            return False
        if (self.setrep(i) == self.setrep(j)):
            return False
        (i,j) = sorted((i,j))
        self.doorways[(i,j)] = (i,j)
        self.merge(i,j)
        return True

    # Selects a neighbor either down or to the right of "node"
    def neighbor(self, node, up_or_down):
        if ((node + 1) % self.w == 0 and up_or_down == 0):
            return node # failure case, return self as neighbor
        return node + 1 + up_or_down * (self.w - 1)

    def get_walls(self):
        num_cells = self.w * self.h
        walls_lr = [(i, i + 1)
                    for i in range(num_cells) if (i % self.w) != self.w - 1]
        walls_ud = [(i, i + self.w)
                    for i in range(num_cells) if int (i / self.w) !=
                                                  self.h - 1]
        return [(i,j) for (i,j) in walls_lr + walls_ud
                if not self.doorways.has_key((i,j))]

    def get_coords(self, cell):
        return ((cell % self.w), int(cell / self.w))

    def make_maze(self):
        while (self.numsets > 1):
            cell = random.randrange (self.w * self.h)
            self.make_door(cell,
                           self.neighbor(cell,
                                         random.randrange(2)))
        return self

class MazeRender:
    def __init__(self, maze):
        self.maze = maze

    def wall_corners(self, cell):
        (i, j) = self.maze.get_coords(cell)
        return [(i + 1, j + 1), (i + 2, j + 1), (i + 1, j + 2), (i + 2, j + 2)]

    def cell_pair_2_wall(self, (cell1, cell2)):
        return [i for i in self.wall_corners(cell1) if
                i in self.wall_corners(cell2)]

    def spew(self, output_func = lambda pair: sys.stdout.write(str(pair))):
        for (i, j) in self.maze.get_walls():
            output_func(self.cell_pair_2_wall((i, j)))

class PsGen:
    def __init__(self, w, h, file = sys.stdout):
        self.out = file
        self.out.write("%!  mazes\n")
        self.out.write("/scal {" + str(int(min(720 / h, 540 / w))) +
                       " mul} def\n\n\n")
        self.dimensions = (w, h)

    def produce_border(self):
        (w, h) = self.dimensions
        self.out.write("0 setgray 3 setlinewidth newpath\n")
        self.out.write("2 scal 1 scal moveto\n")
        self.out.write(str(w + 1) + " scal 1 scal lineto\n")
        self.out.write(str(w + 1) + " scal " + str(h + 1) + " scal lineto\n")
        self.out.write("stroke\n " + str(w) + " scal " + str(h + 1) +
                       " scal moveto\n")
        self.out.write("1 scal " + str(h + 1) + " scal lineto\n")
        self.out.write("1 scal 1 scal lineto stroke\n\n 1 setlinewidth\n\n")

    def process(self, segment):
        self.out.write("0 setgray newpath\n")
        (i,j) = segment[0]
        self.out.write(str(i) + " scal " + str(j) + " scal moveto\n")
        (i, j) = segment[1]
        self.out.write(str(i) + " scal " + str(j) + " scal lineto\n")
        self.out.write("stroke\n")

    def finish(self):
        self.produce_border()
        self.out.write("showpage\n")


if __name__ == "__main__":
    (w, h) = (9, 12)
    #(w, h) = (30, 40)
    # ( w, h) = (18, 24)
    gen = MazeGen(w, h)
    maze = gen.make_maze()
    render = MazeRender(maze)
    ps = PsGen(w, h)
    render.spew(ps.process)
    ps.finish()






        
