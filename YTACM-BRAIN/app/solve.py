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
#equationsPrOptions

def solve(_options, _equationsToOptionMap, _variablesWithPos , _action = None ):
    # Test if the move we just made is good
    # _action should somehow represent setting a specific variable to a target
    # if the move is valid, update the equationsMap and continue if the are move variables
    # if not, return false
    
    if _action == None:
        newOptionMap = _equationsToOptionMap
        newVariablesWithPos = _variablesWithPos
    else:
        target = _action['target']
        eqToUpdate = _equationsToOptionMap[target]

        # Replace equations variable fields with value of tested action
        tRow, tCol = target
        def updateEquation(eq: str):
            return eq.replace(str.format('_{}:{}_', tRow, tCol), _action['value'])
        updatedEquations = list(map(updateEquation, eqToUpdate['eq']))
        
        # Evaluate that all equations without variables are true
        def equationCouldBeValid(eq: str):
            # If there is no more symbols to replace, the equation can be evaluated
            if eq.count('_') == 0:
                    return eval(eq.replace('=', '==').replace('x','*'))
            # Otherwise, if there is more stuff possible to replace, the equation might be possible to solve still
            return True    
        validMove = reduce(lambda a,b: a and equationCouldBeValid(b), updatedEquations, True )

        # Dead end in the tree, cancel path
        if not validMove:
            return (False, _action)
        print(( "valid:", _action))
        # Move was valid with local reference, loop over all equations and update
        oldCopy = _equationsToOptionMap
        
        newOptionMap={}
        for k, v in oldCopy.items():
            updatedEquations2 = list(map(updateEquation, v['eq']))
            v['eq']=updatedEquations2
            newOptionMap[k]=v
        # print(_variablesWithPos)
        newVariablesWithPos = _variablesWithPos.copy()
        del newVariablesWithPos[_action['from']]
            
    if len(_options)==0:
        return (True, _action)
    
    inputOptions = sorted(_options, key=lambda x:newOptionMap[x]['complexity'] + 0.1*len(newOptionMap[x]['eq']) )
    # Take the next option with lowest complexity
    # loop over all variables, and test, until solve return true
    
    opt = inputOptions.pop(0)
    
    # Find equations where this option is present
    print(_equationsToOptionMap[opt]['eq'])
    print(newVariablesWithPos)
    
    for pos, variable in newVariablesWithPos.items():
        move = {'target': opt, 'from': pos, 'value': variable}
        print(_equationsToOptionMap[opt]['eq'])
        print(move)
        
        s,m = solve(inputOptions, newOptionMap, newVariablesWithPos, move)
        r=input("step")
        if (r=='n'):
            exit()

        if s:
            print (m) 
            print (move) 
            return (True, move)
    
    return (False, move)
    

def solve2(_equations, _options, _solvedEquations = [] , _testAction = None ):
    if len(_equations)==0:
        return True
    

    
    


solve2(gameState.equations, gameState.inputOptions, gameState.variablesWithPos.symbols)