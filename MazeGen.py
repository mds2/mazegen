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
    def __init__ (self, w_, h_):
        self.numsets = w_ * h_
        self.w = w_
        self.h = h_
        # Uses disjoint-set unionfind
        # self.sets is the mapping from each grid cell
        # to its set representative.
        # Grid cells are indexed by integer
        self.sets = [i for i in range(0, self.numsets)]
        self.max_horiz_edge = w_ * h_
        self.walls = []
        self.edges = [r * w_ + c for c in range (w_ - 1)
                      for r in range (h_)]
        self.edges += [r * w_ + c + self.max_horiz_edge
                       for c in range (w_)
                       for r in range (h_ - 1)]
        random.shuffle (self.edges)
        self.excluded_walls = {}

    # Finds the set representative for a given cell
    def setrep (self, i):
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
    def merge (self, i, j):
        if (self.setrep(i) == self.setrep(j)):
            return self.setrep(i)
        self.numsets -= 1
        self.sets[self.setrep(i)] = self.setrep(j)
        return self.setrep(i)

    def get_walls (self):
        return self.walls

    def get_coords (self, cell):
        return ((cell % self.w), int(cell / self.w))

    def edge_2_cells (self, edge):
        if (edge >= self.max_horiz_edge):
            edge -= self.max_horiz_edge
            return (edge, edge + self.w)
        return (edge, edge + 1)

    def clear_block(self, xy, wh):
        for i in range(xy[0], xy[0] + wh[0]):
            for j in range(xy[1], xy[1] + wh[1]):
                c = j * self.w + i
                self.merge(c, c + 1)
                self.merge(c, c + self.w)
                self.excluded_walls[(c, c+1)] = True
                self.excluded_walls[(c, c + self.w)] = True

    def make_maze (self):
        if self.walls != []:
            return self
        for edge in self.edges:
            (i, j) = self.edge_2_cells (edge)
            if self.setrep (i) == self.setrep (j):
                if (i,j) in self.excluded_walls:
                    continue
                self.walls.append ((i, j))
            else:
                self.merge (i, j)
        return self

class MazeRender:
    def __init__(self, maze):
        self.maze = maze

    def wall_corners(self, cell):
        (i, j) = self.maze.get_coords(cell)
        return [(i + 1, j + 1), (i + 2, j + 1), (i + 2, j + 2), (i + 1, j + 2)]

    def cell_pair_2_wall(self, (cell1, cell2)):
        return [i for i in self.wall_corners(cell1) if
                i in self.wall_corners(cell2)]

    def spew(self, output_func = lambda pair: sys.stdout.write(str(pair))):
        for (i, j) in self.maze.get_walls():
            if len (self.cell_pair_2_wall((i, j))) < 1:
                raise Exception ("Not adjacent " + str((i, j)))
            output_func(self.cell_pair_2_wall((i, j)))

class PsGen:
    def __init__(self, w, h, file = sys.stdout):
        self.out = file
        self.out.write("%!  mazes\n")
        self.out.write("/scal {" + str(self.get_scale(w,h)) +
                       " mul} def\n\n\n")
        self.dimensions = (w, h)

    def get_scale(self, w, h):
        return int(min(720 / h, 540 / w))

    def blocks_per_text(self, str_list):
        nlines = len(str_list)
        ncols = max([len(l) for l in str_list])
        s = self.get_scale(self.dimensions[0], self.dimensions[1])
        return (int(ncols * 12.0 /s + 1.0) + 1,
                int(nlines * 18.0 / s + 1.0))

    def add_text(self, cell, text):
        self.out.write("\ngsave\n")
        self.out.write("\n/Deja-Vu-Mono findfont 20 scalefont setfont\n")
        self.out.write(str(cell[0] + 2) + " scal " + str(cell[1] + 2) + " scal moveto (" +
                       text + " ) show grestore\n")

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
    # (w, h) = (9, 12)
    (w, h) = (30, 40)
    # ( w, h) = (18, 24)
    (w, h) = (60, 80)
    gen = MazeGen(w, h)
    ps = PsGen(w, h)
    ps.add_text((5,10), "Hello67890 There789")
    ps.add_text((10,30), " here is more text ")
    ps.add_text((2, 30), "hi")
    long_string = "llanfairpwllgwyngyllgogerychwyrndrobw" # + llllantysiliogogogoch"
    ps.add_text((2, 50), long_string)
    gen.clear_block((5,10), ps.blocks_per_text(["Hello67890 There789"]))
    gen.clear_block((10, 30), ps.blocks_per_text([" here is more text "]))
    gen.clear_block((2, 30), ps.blocks_per_text(["hi"]))
    gen.clear_block((2, 50), ps.blocks_per_text([long_string]))
    maze = gen.make_maze()
    render = MazeRender(maze)
    render.spew(ps.process)
    ps.finish()






        
