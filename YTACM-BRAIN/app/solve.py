import sys
from functools import reduce

# Class that contains all the fieldTypes and a method to get a field in the internal structure
class FieldTypes:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.fields = []
    
    # fieldTypes, 0=bg, 1=input, 2= symbol or operator
    def getField(self, r,c):
        return self.fields[c+r*self.cols]
    
    def isBg(self, r,c):
        return self.getField(r,c)==0
    
    def isInput(self, r,c):
        return self.getField(r,c)==1
    
    def isSymbol(self, r,c):
        return self.getField(r,c)==2
    
    # Create field types expecting filePointer to be matching octave output
    def BuildFieldTypes(fp):
        Y = FieldTypes()
        Y.rows, Y.cols = map(int, fp.readline().strip().split())

        for i in range(Y.rows):
            for t in list(map(int, fp.readline().strip().split())):
                Y.fields.append(t)
        return Y
    
class SymbolsWithPos:
    def __init__(self):
        self.symbols = {}
    
    def BuildSymbolsWithPos(fp):
        Y = SymbolsWithPos()
        nSymbols = int(fp.readline().strip())
        for i in range(nSymbols):
            pos, sym = fp.readline().strip().split(":")
            Y.symbols[pos] = sym
        return Y
    
    # Gets symbol at row, column,
    def getSymbol(self, r, c):
        return self.symbols[str.format("{},{}",r+1,c+1)] # Adding one to match Octave indices
    

class GameState:
    def __init__(self, filename: str):
        with open(filename) as fp:
            for line in fp:
                if line.startswith("fieldTypes="):
                    self.fieldTypes = FieldTypes.BuildFieldTypes(fp)
                if line.startswith("symbolsAtPositions="):
                    self.symbolWithPos = SymbolsWithPos.BuildSymbolsWithPos(fp)
                if line.startswith("variables_with_pos="):
                    self.variablesWithPos = SymbolsWithPos.BuildSymbolsWithPos(fp)
        self.CreateEquations()
    
    def _rowAndColIter(self):
        if (self.fieldTypes.cols>1):
            for r in range(self.fieldTypes.rows) :
                for c in range(self.fieldTypes.cols) :
                    yield r,c
                yield (-1, -1)
        if (self.fieldTypes.rows>1):
            for c in range(self.fieldTypes.cols) :
                for r in range(self.fieldTypes.rows) :
                    yield r,c
                yield (-1, -1)
        
    def CreateEquations(self):
        T = self.fieldTypes
        S = self.symbolWithPos
        
        self.equations = []
        self.inputOptions = set()
        currentEquation = ""
        currentEquationVariables = set()
        i = 0
        for r,c in self._rowAndColIter() :
            if r==-1: # Special value for wrap around, or finish
                if i>1:
                    self.equations.append((currentEquation, currentEquationVariables))
                currentEquation=""
                currentEquationVariables=set()
                i=0
            elif T.isSymbol(r,c):
                i+=1
                currentEquation =  currentEquation+ S.getSymbol(r,c)
            elif T.isInput(r,c):
                i+=1
                currentEquation = currentEquation + str.format('_{}:{}_', r,c)
                currentEquationVariables.add((r,c))
                self.inputOptions.add((r,c))
            elif i>1:
                self.equations.append((currentEquation, currentEquationVariables))
                currentEquation=""
                currentEquationVariables=set()
                i=0
            elif i==1:
                currentEquation=""
                currentEquationVariables=set()
                i=0


             
gameState = GameState(sys.argv[1])

# print("inputs to solve an equation from set")
equationsPrOption = {}
for opt in gameState.inputOptions:
    eqFound = []
    for eqWithOpts in gameState.equations:
        if (opt in eqWithOpts[1]):
            eqFound.append(eqWithOpts[0])
    equationsPrOption[opt] = {
        'eq':eqFound, 
        'complexity': (min(map(lambda x:x.count('_')/2, eqFound)))}

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
    
def solve(_equations, _symbols, _solutionPath = [] , _testAction = None):
    
    # At first iteration, move equations to _solutionPath
    if (_testAction == None):
        _solutionPath.insert(0,_equations)

    # If we are making a testAction, update all equations and test if they can still be solved
    if (_testAction != None):
        _equations = _solutionPath[0]
        updatedEquations = updateEquations(_equations, _testAction['varname'], _testAction['value'])
        validMove = validateEquations(updatedEquations)
        if not validMove:
            print('undo', _testAction)
            return False
        else:
            print('proceed with', _testAction)
            _solutionPath.insert(0,updatedEquations)
            newSymbols = _symbols.copy()
            del newSymbols[_testAction['symIdx']]
            _symbols = newSymbols

    # Sort equations and take simplest first
    equations = list(filter(lambda x: len(x[1])!=0, _solutionPath[0]))
    equations = sorted(equations, key=lambda x:len(x[1]))
    solvedEquations = list(filter(lambda x: len(x[1])==0, _solutionPath[0]))
    
    # If there are no more to solve, we can return true
    if len(equations)==0:
        print ('Solution:')
        print(_solutionPath[0])
        return True
    
    (eq, eqVars) = equations.pop(0)
    print(solvedEquations)
    print(equations)
    print (eq)
    print (eqVars)
    print(_symbols)
    varname = eqVars.pop()
    for symIdx, symVal in _symbols.items():
        action = {'varname': varname, 'value':symVal, 'symIdx': symIdx}
        if solve(_equations, _symbols, _solutionPath,  action ):
            print(action)
            return True 
    
    # Reached invalid on this path, undo solutionPath
    _solutionPath.pop(0)
    return False

solve(gameState.equations, gameState.variablesWithPos.symbols)