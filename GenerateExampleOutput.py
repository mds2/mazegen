# Generates a set of examples like those in the "examples" directory.
# Stuffs them in the directory "my_examples"
# Has not been tested on Windows.

import MazeGen

import os

if __name__ == "__main__":
    try:
        os.mkdir("my_examples")
    except OSError:
        print "(directory \"my_examples\" already exists)"

    for ((w, h), basename) in [((9, 12), "small"), ((18, 24), "medium"),
                               ((30, 40), "large")]:
        for i in range(0, 2):
            out = open("my_examples/maze_" + basename +
                       "_" + str(i) + ".ps", "w")
            gen = MazeGen.MazeGen(w, h)
            maze = gen.make_maze()
            render = MazeGen.MazeRender(maze)
            ps = MazeGen.PsGen(w, h, out)
            render.spew(ps.process)
            ps.finish()
            out.close()
