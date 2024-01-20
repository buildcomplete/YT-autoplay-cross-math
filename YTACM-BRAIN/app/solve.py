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
    
    def isBREdge(self, r,c):
        return r == (self.rows-1) or c == (self.cols-1)
    
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
        for r in range(self.fieldTypes.rows) :
            for c in range(self.fieldTypes.cols) :
                yield r,c
        
        for c in range(self.fieldTypes.cols) :
            for r in range(self.fieldTypes.rows) :
                yield r,c

    def CreateEquations(self):
        T = self.fieldTypes
        S = self.symbolWithPos
        
        self.equations = []
        self.inputOptions = set()
        
        currentEquation = ""
        currentEquationVariables = set()
        i = 0
        for r,c in self._rowAndColIter() :
            if T.isSymbol(r,c):
                i+=1
                currentEquation =  currentEquation+ S.getSymbol(r,c)
            elif T.isInput(r,c):
                i+=1
                currentEquation = currentEquation + str.format('_{},{}_', r,c)
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
            # Special case to make sure no wrap around and no missing equation
            if (T.isBREdge(r,c) and i>1):
                self.equations.append((currentEquation, currentEquationVariables))
                currentEquation=""
                currentEquationVariables=set()
                i=0
            if (T.isBREdge(r,c) and i==1):
                currentEquation=""
                currentEquationVariables=set()
                i=0

        # count minimum number of related input for a specific input coordinate
        #for opt in inputOptions:


    def PrintState(self):
        print(self.fieldTypes.fields)
        print(self.variablesWithPos.symbols)
        print(self.symbolWithPos.symbols)

                    
gameState = GameState('/shared/cross-math-scan-result.txt')
#gameState.PrintEquations()
# print("equations=")
# print(gameState.equations)

# print("inputOptions=")
# print(gameState.inputOptions)

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

        tRow, tCol = target

        def updateEquation(eq: str):
            return eq.replace(str.format('_{},{}_', tRow, tCol), _action['value'])

        # map(lambda eq: eq.replace('_{},{}_', _action['target']), _equationsToUpdate
        updatedEquations = list(map(updateEquation, eqToUpdate['eq']))

        def equationCouldBeValid(eq: str):
            # If there is no more symbols to replace, the equation can be evaluated
            if eq.count('_') == 0:
                    return eval(eq.replace('=', '=='))
            # Otherwhise, if there is more stuff possible to replace, the equation might be possible to solve still
            return True 
            
        validMove = reduce(lambda a,b: b and equationCouldBeValid(a), updatedEquations )
        if not validMove:
            return False
        
        # Move was valid with local reference, loop over all equations and update
        oldCopy = _equationsToOptionMap
        
        newOptionMap={}
        for k, v in oldCopy.items():
            updatedEquations2 = list(map(updateEquation, v['eq']))
            v['eq']=updatedEquations2
            newOptionMap[k]=v
        print(_variablesWithPos)
        newVariablesWithPos = _variablesWithPos.copy()
        del newVariablesWithPos[_action['from']]
            
    if len(_options)==0:
        print ("solution found")
        return True
    
    inputOptions = sorted(_options, key=lambda x:newOptionMap[x]['complexity'] - 0.1*len(newOptionMap[x]['eq']) )
    # Take the next option with lowest complexity
    # loop over all variables, and test, until solve return true
    
    opt = inputOptions.pop(0)
    # Find equations where this option is present
    print(_equationsToOptionMap[opt]['eq'])
    print(newVariablesWithPos)
    for pos, variable in newVariablesWithPos.items():
        move = {'target': opt, 'from': pos, 'value': variable}
        print('Apply')
        print (move)
        print(newOptionMap)
        if solve(inputOptions, newOptionMap, newVariablesWithPos, move):
            return True
        else:
            print('Undo')
    
    return False
    

solve(gameState.inputOptions, equationsPrOption, gameState.variablesWithPos.symbols)