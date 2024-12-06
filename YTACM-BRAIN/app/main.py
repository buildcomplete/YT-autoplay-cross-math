import sys
import time
from pathlib import Path
from Solver import solve
from GameState import GameState

# usage
# python main.py inputStateFilename resultSwipesFilename travelHistoryFilename solutionStatistics
if len(sys.argv) != 5:
    print("Usage: python main.py inputStateFilename resultSwipesFilename travelHistoryFilename solutionStatistics")
    exit(-1)

inputStateFilename = sys.argv[1]
resultSwipesFilename = sys.argv[2]
travelHistoryFilename = sys.argv[3]
solutionStatistics = sys.argv[4]


print(f"Reading from:{inputStateFilename}")
gameState = GameState(sys.argv[1])

start = time.time()
with open(travelHistoryFilename, 'wt') as fp:
    (solutionFound, path, nodesVisited) = solve(gameState.equations, gameState.variablesWithPos.symbols, fp)
end = time.time()
sTimeMs = round((end-start)*1000)

# store in image coordinates for applying to device and renderer
if solutionFound:
    newFile = not Path(solutionStatistics).exists()
    with open(solutionStatistics, 'at') as fp:
        if newFile:
            fp.write("inputStateFilename, sTimeMs, nodesVisited, #Equations, #symbols\n")
        fp.write(f"{inputStateFilename}, {sTimeMs}, {nodesVisited}, {len(gameState.equations)}, {len(gameState.inputOptions)}\n")

    with open(resultSwipesFilename, 'wt') as fp:
        fp.write(f"src_r, src_c, dst_r, dst_c\n")
        path.reverse()
        for action in path:
            # action['varname'] is the position in the playfield to move to
            dst_r = gameState.fieldMappingR[action['varname'][0]]
            dst_c = gameState.fieldMappingC[action['varname'][1]]
            symR, symC = map(int, action['symIdx'].split(","))
            src_r = gameState.symbolMappingR[symR-1]
            src_c = gameState.symbolMappingC[symC-1]
            
            fp.write(f"{src_r}, {src_c}, {dst_r}, {dst_c}\n")
    print(f"Saved solution to:{resultSwipesFilename}")
else:
    print("No solution found")