import sys 
import re 
string = sys.argv[1]


LIST_TERM = ['*','/']
LIST_EXP = ['+','-']
LIST_PAREN = ['(',')']

class Node:
    
    def __init__(self, value):
        self.value = value
        self.children = []
        
    def evaluate(self):
        pass            
    

class BinOp(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        return self.children[0].evaluate() // self.children[1].evaluate()

class UnOp(Node):
    
    def  __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        return -1*self.children[0].evaluate()

class IntVal(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self):
        return self.value

class NoOp(Node):
    
    def __init__(self):
        self.value = None
    
    def evaluate(self):
        return 0

class Token:
    
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    
    def __init__(self, source, position):
        self.source = source
        self.position = position       
        
    def selectNext(self):
        value = ''
        
        while (1):           
            
            if (self.position < len(self.source)):
                if self.source[self.position] == ' ': 
                    self.position += 1
                    #se a string estiver com algo, precisa retornar
                    if (value != ''):
                        self.next = Token('NUMBER', value)
                        return
   
                    continue
                    
            if (self.position < len(self.source)):
                if self.source[self.position] == '*' or self.source[self.position] == '/' or self.source[self.position] == '+' or self.source[self.position] == '-' or self.source[self.position] == '(' or self.source[self.position] == ')':
                    if(value == ''):
                        self.next = Token('OPERATOR', self.source[self.position])
                        self.position += 1
                        return
                    else:
                        self.next = Token('NUMBER', value)
                        return

            if (self.position < len(self.source)):
                if (self.source[self.position].isdigit()):
                        
                    value += self.source[self.position]
                    self.position += 1
                
                #Não é numero, nem operador, nem espaço
                elif (self.source[self.position] != ' '):
                    sys.stderr.write('ERROR: INVALID CHARACTER')
                    sys.exit(1)
    
            else:
                if (value == ''): 
                    self.next = Token('EOF', None)
                    return
                
                self.next = Token('NUMBER', value)
                return
        
class Parse:
    
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        
    @staticmethod
    def parseFactor(tokenizer):
        if tokenizer.next.type == 'NUMBER':
            resultado = int(tokenizer.next.value)
            tokenizer.selectNext()
            intval = IntVal(resultado)
            return intval
            
        if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '+':
            tokenizer.selectNext()
            resultado = Parse.parseFactor(tokenizer)
            unop = UnOp("+", [resultado])
            return unop
        
        if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '-':
            tokenizer.selectNext()
            resultado = Parse.parseFactor(tokenizer)
            unop = UnOp("-", [resultado])
            return unop

        if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '(':
            tokenizer.selectNext()
            resultado = Parse.ParseExpression(tokenizer)
            
            if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == ')':
                tokenizer.selectNext()
                return resultado
            else:
                sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                sys.exit(1)
                
    @staticmethod
    def parseTerm(tokenizer):
        
        noUm = Parse.parseFactor(tokenizer)
        
        while tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_TERM:
            
            if tokenizer.next.value == '*':
                tokenizer.selectNext()
                noDois = Parse.parseFactor(tokenizer)
                noUm = BinOp("*", [noUm, noDois])    
                
            elif tokenizer.next.value == '/':
                tokenizer.selectNext()
                noDois = Parse.parseFactor(tokenizer)
                noUm = BinOp("/", [noUm, noDois])
        
        return noUm
        
    
    @staticmethod
    def ParseExpression(tokenizer):
        
        noUm = Parse.parseTerm(tokenizer)
        
        while tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_EXP:
            
            if tokenizer.next.value == '+':
                tokenizer.selectNext()
                noDois = Parse.parseTerm(tokenizer)
                noUm = BinOp("+", [noUm, noDois])
                
            elif tokenizer.next.value == '-':
                tokenizer.selectNext()
                noDois = Parse.parseTerm(tokenizer)
                noUm = BinOp("-", [noUm, noDois])
                
        return noUm
        
    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.selectNext()
        
        arvore = Parse.ParseExpression(tokenizer)

        if tokenizer.next.type != 'EOF':
            sys.stderr.write('ERROR: EOF NOT FOUND')
            sys.exit(1)
            
        return arvore

class PrePro:
    
    @staticmethod
    def filter(code):
        #code_filtered = re.sub(r"#.*\n", "", code, flags=re.MULTILINE)
        code_filtered = re.sub(r"#.*$", "", code)
        code_filtered = code_filtered.replace("\n", "")
        return code_filtered

def read_file(file):
    with open(file, 'r') as f:
        return f.read()

test_files = read_file(string)

print(Parse.run(PrePro.filter(test_files)).evaluate())

    
    
    
    