import sys
from functools import reduce
from GameState import GameState
             
gameState = GameState(sys.argv[1])

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
            return False
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
        return True
    
    (eq, eqVars) = equations.pop(0)

    nodeName = 'root' if (_testAction == None) else f"{len(_solutionPath)}_{_testAction['varname'][0]}_{_testAction['varname'][1]}_{_testAction['value']}"

    varname = eqVars.pop()
    testedVal = set()
    for symIdx, symVal in _symbols.items():
        action = {'varname': varname, 'value':symVal, 'symIdx': symIdx}
        if symVal in testedVal:
            continue
        testedVal.add(symVal)

        childNodeName = f"{len(_solutionPath)+1}_{action['varname'][0]}_{action['varname'][1]}_{action['value']}"

        _travelHistory.write(f"{nodeName}-->{childNodeName}\n")
        
        if solve(_equations, _symbols, _travelHistory, _solutionPath,  action ):
            print(action)
            return True
        else:
            _travelHistory.write(f"{childNodeName}-->{nodeName}\n")
    
    # Reached invalid leaf on this path, undo solutionPath
    _solutionPath.pop(0)
    return False

with open('travel-history.txt', 'wt') as fp:
    solve(gameState.equations, gameState.variablesWithPos.symbols, fp)