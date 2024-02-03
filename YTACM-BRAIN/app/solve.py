import sys
from functools import reduce
from GameState import GameState

def updateEquations(_equations, _varname, _value):
    # Replace equations variable fields with value of tested action
    tRow, tCol = _varname
    def updateEquation(eqWithOpts):
        return  (eqWithOpts[0].replace(str.format('_{}:{}_', tRow, tCol), _value), eqWithOpts[1] - {(tRow, tCol)} )
    return list(map(updateEquation, _equations))

def validateEquations(_equations):

    # Evaluate that all equations without variables are true
    def equationCouldBeValid(eq: str):
        # If there is no more symbols to replace, the equation can be evaluated
        if eq.count('_') == 0:
                return eval(eq.replace('=', '==').replace('x','*'))
        # Otherwise, if there is more stuff possible to replace, the equation might be possible to solve still
        return True    
    return reduce(lambda a,b: a and equationCouldBeValid(b[0]), _equations, True )
    
def solve(_equations, _symbols, _travelHistory, _solutionPath = [] , _testAction = None):
    
    # At first iteration, move equations to _solutionPath
    if (_testAction == None):
        _solutionPath.insert(0,_equations)
    
    # If we are making a testAction, update all equations and test if they can still be solved
    if (_testAction != None):
        
        _equations = _solutionPath[0]
        updatedEquations = updateEquations(_equations, _testAction['varname'], _testAction['value'])
        validMove = validateEquations(updatedEquations)
        if not validMove:
            return (False, None)
        else:
            _solutionPath.insert(0,updatedEquations)
            newSymbols = _symbols.copy()
            del newSymbols[_testAction['symIdx']]
            _symbols = newSymbols

    # Sort equations and take simplest first
    equations = list(filter(lambda x: len(x[1])!=0, _solutionPath[0]))
    equations = sorted(equations, key=lambda x:len(x[1]))
    
    # If there are no more to solve, we can return true
    if len(equations)==0:
        print ('Solution:')
        print(_solutionPath[0])
        return (True, []) # Return empty list, path will be appended in caller
    
    def cleanEqForMermaid(x):
        return x.replace(" ","_").replace('+','p').replace('-','m').replace('=','e').replace('/','s')

    def nameFromAction(act, parent = False):
        L = len(_solutionPath)- (1 if parent else 0)
        return f"L{L} {updateEquations([(act['eq'], {act['varname']})],act['varname'],act['value'])[0][0]}"
    
    nodeName = 'root' if (_testAction == None) else f"{cleanEqForMermaid(nameFromAction(_testAction, True))}(\"{nameFromAction(_testAction, True)}\")"
    
    (eq, eqVars) = equations.pop(0)
    
    varname = eqVars.pop()
    testedVal = set()
    for symIdx, symVal in _symbols.items():
        action = {'varname': varname, 'value':symVal, 'symIdx': symIdx, 'eq':eq}
        if symVal in testedVal:
            continue
        testedVal.add(symVal)

        childNodeName = f"{cleanEqForMermaid(nameFromAction(action))}(\"{nameFromAction(action)}\")"

        _travelHistory.write(f"{nodeName}-->{childNodeName}\n")
        solved, path = solve(_equations, _symbols, _travelHistory, _solutionPath,  action )
        if solved:
            path.append(action)
            return (True, path)
        else:
            _travelHistory.write(f"{childNodeName}-->{nodeName}\n")
    
    # Reached invalid leaf on this path, undo solutionPath
    _solutionPath.pop(0)
    return (False, None)

print(f"Reading from:{sys.argv[1]}")
gameState = GameState(sys.argv[1])
with open('travel-history.txt', 'wt') as fp:
    (solutionFound, path) = solve(gameState.equations, gameState.variablesWithPos.symbols, fp)
    
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