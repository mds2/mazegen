# Generates a booklet of mazes
#
# Run as ProduceMazeBook.py width height pages > output_file
# e.g.
# python ProduceMazeBook.py 18 24 10 > booklet.ps
#
# Prints to standard out

import MazeGen
import sys

if __name__ == "__main__":
    try:
        (w, h) = [int(x) for x in sys.argv[1:][:2]]
    except:
        (w, h) = (18, 24)

    try:
        pages = int(sys.argv[3])
    except:
        pages = 10

    ps = MazeGen.PsGen(w, h, sys.stdout)
    for page in range (0, pages):
        gen = MazeGen.MazeGen(w, h)
        maze = gen.make_maze()
        render = MazeGen.MazeRender(maze)
        render.spew(ps.process)
        ps.finish()

