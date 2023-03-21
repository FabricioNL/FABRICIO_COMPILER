import sys 
import re 
string = sys.argv[1]



LIST_TERM = ['*','/']
LIST_EXP = ['+','-']
LIST_PAREN = ['(',')']
LIST_ASSIGN = ['=']

LIST_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             '_']

LIST_NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

LIST_RESERVED_WORDS = ['println', 'if', 'else', 'while', 'for', 'int', 'float', 'char', 'string', 
                       'bool', 'true', 'false', 'return', 'break', 'continue', 'and', 'or', 'not']

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
        pass
    
    def evaluate(self):
        pass

class Identifier(Node):
    
    def __init__(self, value):
        self.value = value
    
    def evaluate(self):
        return SymbolTable.getter(self.value)
        
class SymbolTable:
     
    table = {}
                
    def getter(key):
        #verificar se a chave existe, senão, erro
        if key in SymbolTable.table:
            return SymbolTable.table[key]
        
        sys.stderr.write('ERROR: KEY NOT DECLARED')
        sys.exit(1)
        
    def setter(key, value):
        SymbolTable.table[key] = value
        
class Assignment(Node):
    
    def __init__(self, value, children):
        
        self.value = value
        self.children = children
    
    def evaluate(self):
        SymbolTable.setter(self.value, self.children[0].evaluate())

class Block(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self):
        for child in self.children:
            child.evaluate()

class Print(Node):
        def __init__(self, children):
            self.children = children
        
        def evaluate(self):
            print(self.children[0].evaluate())    
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
                if self.source[self.position] == ' ' or self.source[self.position] in LIST_PAREN or self.source[self.position] in LIST_ASSIGN or self.source[self.position] in LIST_TERM or self.source[self.position] in LIST_EXP or self.source[self.position] == '\n': 
                    if (self.source[self.position] == ' '):
                        self.position += 1
                        continue
                    #se a string estiver com algo, precisa retornar
                    if (value != ''):
                        
                        if (value.isdigit()):
                            self.next = Token('NUMBER', value)
                            return
   
                        if (value in LIST_RESERVED_WORDS):
                            self.next = Token('PRINTLN', value)
                            return 
                        
                        self.next = Token('IDENTIFIER', value)
                        return

                    if (value == '' and (self.source[self.position] in LIST_PAREN or self.source[self.position] in LIST_ASSIGN or self.source[self.position] in LIST_TERM or self.source[self.position] in LIST_EXP)):
                        self.next = Token('OPERATOR', self.source[self.position])
                        self.position += 1
                        return
                    
                    if (value == '' and self.source[self.position] == '\n'):
                        self.next = Token('QUEBRA_LINHA', self.source[self.position])
                        self.position += 1
                        return
   
                    continue
                    
            if (self.position < len(self.source)):
                if self.source[self.position] == '*' or self.source[self.position] == '/' or self.source[self.position] == '+' or self.source[self.position] == '-' or self.source[self.position] == '(' or self.source[self.position] == ')' or self.source[self.position] == '=':
                    if(value == ''):
                        self.next = Token('OPERATOR', self.source[self.position])
                        self.position += 1
                        return
                    else:
                        self.next = Token('NUMBER', value)
                        return

            if (self.position < len(self.source)):
                
                if ((value == '')):
                    #verifica se é uma letra do alfabeto, underscore ou numero
                    if (self.source[self.position] in LIST_LETTERS or self.source[self.position] in LIST_NUMBERS):
                        value += self.source[self.position]
                        self.position += 1
                    else:
                        if (self.source[self.position] == '\n'):
                            self.next = Token("QUEBRA_LINHA", self.source[self.position])
                            self.position += 1
                            return
                        
                        sys.stderr.write('ERROR: INVALID CHARACTER')
                        sys.exit(1)
                
                elif (value != ''):
                    if (value.isdigit()):
                        if (self.source[self.position] in LIST_NUMBERS):
                            value += self.source[self.position]
                            self.position += 1
                        if (self.source[self.position] not in LIST_NUMBERS):
                            self.next = Token('NUMBER', value)
                            return
                    elif (self.source[self.position] in LIST_LETTERS or self.source[self.position] in LIST_NUMBERS):
                            value += self.source[self.position]
                            self.position += 1
                    else:
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
        
        if tokenizer.next.type == 'IDENTIFIER':
            name = tokenizer.next.value
            tokenizer.selectNext()
            identi = Identifier(name)
            return identi
                
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
    def ParseBlock(tokenizer):
        children = []
        
        while tokenizer.next.type != 'EOF':
            children.append(Parse.ParseStatement(tokenizer))
            tokenizer.selectNext()
        
        return Block(children)
    
    @staticmethod
    def ParseStatement(tokenizer):
        if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
            #tokenizer.selectNext()
            return NoOp()
                
        if tokenizer.next.value in LIST_RESERVED_WORDS and tokenizer.next.type == 'PRINTLN':
            tokenizer.selectNext()
            
            if tokenizer.next.value == '(':
                tokenizer.selectNext()
                
                children = [Parse.ParseExpression(tokenizer)]
                
                if tokenizer.next.value == ')':
                    tokenizer.selectNext()
                    return Print(children)
                
                else:
                    sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                    sys.exit(1)
            else:
                sys.stderr.write('ERROR: PARENTHESIS NOT OPENED')
                sys.exit(1)
        
        if tokenizer.next.type == 'IDENTIFIER':
            name = tokenizer.next.value
            tokenizer.selectNext()
            
            if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_ASSIGN:
                tokenizer.selectNext()
                
                children = [Parse.ParseExpression(tokenizer)]
                
                return Assignment(name, children)
            
            else:
                sys.stderr.write('ERROR: EQUALS NOT FOUND')
                sys.exit(1)
        else:
            sys.stderr.write('ERROR: IDENTIFIER NOT FOUND')
            sys.exit(1)
       
        
        
    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.selectNext()
        
        arvore = Parse.ParseBlock(tokenizer)
        if tokenizer.next.type != 'EOF':
            sys.stderr.write('ERROR: EOF NOT FOUND')
            sys.exit(1)
            
        return arvore

class PrePro:
    
    @staticmethod
    def filter(code):
        code_filtered = re.sub(r'#.*\n', '', code, flags=re.MULTILINE).replace("\s", "")
        return code_filtered


def read_file(file):
    with open(file, 'r') as f:
        return f.read()

test_files = read_file(string)

Parse.run(PrePro.filter(test_files)).evaluate()

    
    
    
    