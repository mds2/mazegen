mazegen
=======

Simple python program to generate postscript mazes.

Intended to entertain the author's child.

Inspired by Olin Shivers' description of an earlier Scheme program
with a nearly identical algorithm.

[ 
http://www.ccs.neu.edu/home/shivers/mazes.html
](http://www.ccs.neu.edu/home/shivers/mazes.html)

Example wired up to AppEngine at

[ 
https://maze-maker.appspot.com/
](https://maze-maker.appspot.com/ )
 
Files include
* MazeGen.py

  Generates random maze through variant of Kruskal's algorithm.
  Contains a class to output maze as postscript file.
  Can run as standalone application.

* GenerateExampleOutput.py

  Standalone program.
  Produces output like the examples in the directory "examples"

* ProduceMazeBook.py 

  Standalone program.
  Produces a small booklet of many distinct mazes.

* examples/

  Example output of MazeGen.py

