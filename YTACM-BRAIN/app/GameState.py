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
                if line.startswith("fieldCenters_r="):
                    self.fieldMappingR = list(map(int, fp.readline().strip().split()))
                if line.startswith("fieldCenters_c="):
                    self.fieldMappingC = list(map(int, fp.readline().strip().split()))
                if line.startswith("varCenters_r="):
                    self.symbolMappingR = list(map(int, fp.readline().strip().split()))
                if line.startswith("varCenters_c="):
                    self.symbolMappingC = list(map(int, fp.readline().strip().split()))

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