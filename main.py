import sys 
import re 
string = sys.argv[1]

LIST_TERM = ['*','/', '&&']
LIST_EXP = ['+','-','||']
LIST_PAREN = ['(',')']
LIST_ASSIGN = ['=']
LIST_REL = ['<','>','==']

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
        if self.value == "==":
            return self.children[0].evaluate() == self.children[1].evaluate()
        if self.value == "<":
            return self.children[0].evaluate() < self.children[1].evaluate()
        if self.value == ">":
            return self.children[0].evaluate() > self.children[1].evaluate()
        if self.value == "&&":
            return self.children[0].evaluate() and self.children[1].evaluate()
        if self.value == "||":
            return self.children[0].evaluate() or self.children[1].evaluate()
        
        return self.children[0].evaluate() // self.children[1].evaluate()

class UnOp(Node):
    
    def  __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self):
        if self.value == "!":
            return not self.children[0].evaluate()
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

class Read(Node):
    
    def __init__(self):
        pass
        
    def evaluate(self):
        return int(input())
    
class Block(Node):
    
    def __init__(self, children):
        self.children = children

    def evaluate(self):
        for child in self.children:
            child.evaluate()

class While(Node):
    
    def __init__(self, children):
        self.children = children
    
    def evaluate(self):
        while self.children[0].evaluate():
            self.children[1].evaluate()
            
class If(Node):
    
    def __init__(self, children):
        self.children = children
    
    def evaluate(self):
        if self.children[0].evaluate():
            self.children[1].evaluate()
        else:
            self.children[2].evaluate()

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
        while (self.position < len(self.source)) and self.source[self.position] == " ": # se for espaço só pula
            self.position = self.position + 1

        if self.position == len(self.source):
            self.next = Token("EOF", None)

        elif self.source[self.position].isdigit():
            value = ""
            while (self.position < len(self.source)) and (self.source[self.position].isdigit()): # se for digito vai concatenando
                value = value + self.source[self.position]
                self.position = self.position + 1

            self.next = Token("NUMBER", value)
            return 

        elif self.source[self.position] == '*': # se for mult
            self.next =  Token("OPERATOR", "*")
            self.position = self.position + 1
            return

        elif self.source[self.position] == '/': # se for div
            self.next =  Token("OPERATOR", "/")
            self.position = self.position + 1
            return
        
        elif self.source[self.position] == '!': # se for not
            self.next =  Token("OPERATOR", "!")
            self.position = self.position + 1
            return
            
        elif self.source[self.position] == '+': # se for soma
            self.next =  Token("OPERATOR", "+")
            self.position = self.position + 1
            return
            
        elif self.source[self.position] == '-': # se for sub
            self.next = Token("OPERATOR", "-")
            self.position = self.position + 1
            return

        elif self.source[self.position] == '(': # se for abrir par
            self.next = Token("OPERATOR", "(")
            self.position = self.position + 1
            return

        elif self.source[self.position] == ')': # se for fechar par
            self.next = Token("OPERATOR", ")")
            self.position = self.position + 1
            return
        
        elif self.source[self.position] == '=': # se for igual
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token("OPERATOR", "==")
                self.position = self.position + 2
            else:
                self.next = Token("OPERATOR", "=")
                self.position = self.position + 1
            
            return
        
        elif self.source[self.position] == '&': # se for and
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
                self.next = Token("OPERATOR", "&&")
                self.position = self.position + 2
                return 
            
            sys.stderr.write('ERROR: ONLY ONE &')
            sys.exit(1)
            
        elif self.source[self.position] == '|': # se for or
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
                self.next = Token("OPERATOR", "||")
                self.position = self.position + 2
                return 
            
            sys.stderr.write('ERROR: ONLY ONE |')
            sys.exit(1)

        elif self.source[self.position] == '\n': # se for quebra de linha
            self.next = Token("QUEBRA_LINHA", "\n")
            self.position = self.position + 1

        elif self.source[self.position] == '>': # se for greather than
            self.next = Token("GREATER", ">")
            self.position = self.position + 1
            return

        elif self.source[self.position] == '<': # se for less than
            self.next = Token("LESS", "<")
            self.position = self.position + 1
            return

        elif self.source[self.position].isalpha():

            value = "" #se for palavra vai concatenando, precisa checar se chegou no final
            while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"): 
                value = value + self.source[self.position]
                self.position = self.position + 1

            if value == "while": 
                self.next = Token("WHILE", value)  
                return 
                      
            elif value == "if":
               self.next = Token("IF", value)
               return
            
            elif value == "else":
                self.next = Token("ELSE", value)
                return
            
            elif value == "println":
                self.next = Token("PRINTLN", value) 
                return
            
            elif value == "readline":
                self.next = Token("READLINE", value)
                return
        
            elif value == "end":
                self.next = Token("END", value)
                return
            
            else:
                self.next = Token("IDENTIFIER", value)
                return
        else:
            sys.stderr.write("Caractere inválido: {}.".format(self.source[self.position]))
            sys.exit(1)
        
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


        if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '!':
            tokenizer.selectNext()
            resultado = Parse.parseFactor(tokenizer)
            unop = UnOp("!", [resultado])
            return unop
        
        
        if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '(':
            tokenizer.selectNext()
            resultado = Parse.ParseRelExpression(tokenizer)
            
            if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == ')':
                tokenizer.selectNext()
                return resultado
            else:
                sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                sys.exit(1)
        
        if tokenizer.next.value == "readline":
            tokenizer.selectNext()
            if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '(':
                tokenizer.selectNext()
                if tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == ')':
                    tokenizer.selectNext()
                    readline = Read()
                    return readline
                else:
                        sys.stderr.write('ERROR: PARENTHESIS NOT CLOSED')
                        sys.exit(1)
            else:
                sys.stderr.write('ERROR: PARENTHESIS NOT OPENED')
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
                
            elif tokenizer.next.value == '&&':
                tokenizer.selectNext()
                noDois = Parse.parseFactor(tokenizer)
                noUm = BinOp("&&", [noUm, noDois])
                
        
        return noUm
        
    @staticmethod
    def ParseRelExpression(tokenizer):
        
        noUm = Parse.ParseExpression(tokenizer)
        
        while (tokenizer.next.type == "GREATER" or tokenizer.next.type == "LESS" or tokenizer.next.type == "OPERATOR")  and tokenizer.next.value in LIST_REL:
            
            if tokenizer.next.value == '<':
                tokenizer.selectNext()
                noDois = Parse.ParseExpression(tokenizer)
                noUm = BinOp("<", [noUm, noDois])
            
            elif tokenizer.next.value == '>':
                tokenizer.selectNext()
                noDois = Parse.ParseExpression(tokenizer)
                noUm = BinOp(">", [noUm, noDois])
            
            elif tokenizer.next.value == '==':
                tokenizer.selectNext()
                noDois = Parse.ParseExpression(tokenizer)
                noUm = BinOp("==", [noUm, noDois])
        
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
                
            elif tokenizer.next.value == '||':
                tokenizer.selectNext()
                noDois = Parse.parseTerm(tokenizer)
                noUm = BinOp("||", [noUm, noDois])
                
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
            return NoOp()
                
        if tokenizer.next.value in LIST_RESERVED_WORDS and tokenizer.next.type == 'PRINTLN':
            tokenizer.selectNext()
            
            if tokenizer.next.value == '(':
                tokenizer.selectNext()
                
                children = [Parse.ParseRelExpression(tokenizer)]
                
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
                
                children = [Parse.ParseRelExpression(tokenizer)]
                
                return Assignment(name, children)
            
            else:
                sys.stderr.write('ERROR: EQUALS NOT FOUND')
                sys.exit(1)
                
        if tokenizer.next.value in LIST_RESERVED_WORDS and tokenizer.next.type == 'IF':
            tokenizer.selectNext()
            
            expression = Parse.ParseRelExpression(tokenizer)
            
            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                tokenizer.selectNext()
                
                if_children = []
                
                while tokenizer.next.type != 'END' and tokenizer.next.type != 'ELSE':
                    if_children.append(Parse.ParseStatement(tokenizer))
                    tokenizer.selectNext()
                    
                block_if = Block(if_children)
                
                if tokenizer.next.value == 'else':
                    tokenizer.selectNext()
                    
                    if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                        tokenizer.selectNext()
                        
                        else_children = []	
                        
                        while tokenizer.next.type != 'END':
                            else_children.append(Parse.ParseStatement(tokenizer))
                            tokenizer.selectNext()
                        
                        block_else = Block(else_children)
                        
                        return If([expression, block_if, block_else])
                    
                    else:
                        sys.stderr.write('ERROR: \\n NOT FOUND (ELSE)')
                        sys.exit(1)
                
                if tokenizer.next.type == 'END':
                    tokenizer.selectNext()
                    return If([expression, block_if])
            
            else:
                sys.stderr.write('ERROR: \\n NOT FOUND (IF)')
                sys.exit(1)
                
        if tokenizer.next.type == "WHILE" and tokenizer.next.value in LIST_RESERVED_WORDS:
            tokenizer.selectNext()
            
            expression = Parse.ParseRelExpression(tokenizer)
            
            if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
                tokenizer.selectNext()
                
                while_children = []
                
                while tokenizer.next.type != 'END':
                    while_children.append(Parse.ParseStatement(tokenizer))
                    tokenizer.selectNext()
                
                #precisa consumir o END 
                tokenizer.selectNext()
                block_while = Block(while_children)
                return While([expression, block_while])
                
            else:
                sys.stderr.write('ERROR: \\n NOT FOUND (WHILE)')
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

#string = 'test.txt'

test_files = read_file(string)
Parse.run(PrePro.filter(test_files)).evaluate()

    
    
    
    