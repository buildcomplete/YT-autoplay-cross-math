import sys
from Solver import solve
from GameState import GameState

# usage
# python main.py inputStateFilename resultSwipesFilename travelHistoryFilename solutionStatistics

print(len(sys.argv))

print(f"Reading from:{sys.argv[1]}")
gameState = GameState(sys.argv[1])
with open('travel-history.txt', 'wt') as fp:
    (solutionFound, path, nodesVisited) = solve(gameState.equations, gameState.variablesWithPos.symbols, fp)

print (f"nodesVisited: {nodesVisited}")    
# store in image coordinates for applying to device and renderer
if solutionFound:
    with open('swipes.csv', 'wt') as fp:
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