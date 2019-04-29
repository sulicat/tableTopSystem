import os
import sys
import subprocess

board = [ [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0] ]

out = ['./engine']
for r in board:
    for piece in r:
        out.append(str(piece));

engine_path = "./build"
os.chdir(engine_path)


result = subprocess.Popen(out, stdout=subprocess.PIPE)
result = result.communicate()

print(result[0])
