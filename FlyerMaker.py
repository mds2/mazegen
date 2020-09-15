# To use "python FlyerMaker.py textfile.txt"
# for instance "python FlyerMaker.py party.txt"
# produces output like that found in
# "party.txt.ps"

from MazeGen import *
from random import randrange
import sys

def make_flyer(lines, wh=(60, 80), outfile = sys.stdout):
    (w, h) = wh
    gen = MazeGen(w, h)
    ps = PsGen(w, h, file=outfile)
    _, height_blocks = ps.blocks_per_text(lines)
    stepsize = int(h / (len(lines) + 1))
    while stepsize < 2 + ps.blocks_per_text("hi")[1]:
        lines = lines[:(len(lines)/2)]
        _, height_blocks = ps.blocks_per_text(lines)
        stepsize = int(h / (len(lines) + 1))
    row = h - stepsize
    for line in lines:
        blocksize = ps.blocks_per_text([line])
        maxcol = w - blocksize[0] - 4
        startcol = randrange(maxcol)
        ps.add_text((startcol, row), line)
        gen.clear_block((startcol, row), blocksize)
        row -= stepsize
    maze = gen.make_maze()
    render = MazeRender(maze)
    render.spew(ps.process)
    ps.finish()


if __name__ == "__main__":
    text_in = open(sys.argv[1])
    lines = [l.strip() for l in text_in.readlines() if l.strip() != ""]
    make_flyer(lines, wh=(68, 88), outfile = open(sys.argv[1] + ".ps", "w"))
