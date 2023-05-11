import sys 
import re 
#string = sys.argv[1]

LIST_TERM = ['*','/', '&&']
LIST_EXP = ['+','-','||', "."]
LIST_PAREN = ['(',')']
LIST_ASSIGN = ['=']
LIST_REL = ['<','>','==']

LIST_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             '_']

LIST_NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

LIST_RESERVED_WORDS = ['println', 'if', 'else', 'while', 'for', 'int', 'float', 'char', 'string', 
                       'bool', 'true', 'false', 'return', 'break', 'continue', 'and', 'or', 'not']

codigo_fonte = ""

class Assembly:
    code = ""
    filename = ""

    footer = """; interrupcao de saida
    POP EBP
    MOV EAX, 1
    INT 0x80"""

    header = """; constantes
    SYS_EXIT equ 1
    SYS_READ equ 3
    SYS_WRITE equ 4
    STDIN equ 0
    STDOUT equ 1
    True equ 1
    False equ 0

    segment .data

    segment .bss  ; variaveis
      res RESB 1

    section .text
      global _start

    print:  ; subrotina print

      PUSH EBP ; guarda o base pointer
      MOV EBP, ESP ; estabelece um novo base pointer

      MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
      XOR ESI, ESI

    print_dec: ; empilha todos os digitos
      MOV EDX, 0
      MOV EBX, 0x000A
      DIV EBX
      ADD EDX, '0'
      PUSH EDX
      INC ESI ; contador de digitos
      CMP EAX, 0
      JZ print_next ; quando acabar pula
      JMP print_dec

    print_next:
      CMP ESI, 0
      JZ print_exit ; quando acabar de imprimir
      DEC ESI

      MOV EAX, SYS_WRITE
      MOV EBX, STDOUT

      POP ECX
      MOV [res], ECX
      MOV ECX, res

      MOV EDX, 1
      INT 0x80
      JMP print_next

    print_exit:
      POP EBP
      RET

    ; subrotinas if/while
    binop_je:
      JE binop_true
      JMP binop_false

    binop_jg:
      JG binop_true
      JMP binop_false

    binop_jl:
      JL binop_true
      JMP binop_false

    binop_false:
      MOV EBX, False
      JMP binop_exit
    binop_true:
      MOV EBX, True
    binop_exit:
      RET

    _start:

      PUSH EBP ; guarda o base pointer
      MOV EBP, ESP ; estabelece um novo base pointer
      
      ; codigo gerado pelo compilador
      """

    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def joinCode(string):
        Assembly.code += string + '\n'

    @staticmethod
    def getCode():
        return Assembly.code
    
    @staticmethod
    def setFileName(filename):
        Assembly.filename = filename.split('.')[0] + '.asm'
        #print(Assembly.filename)
    
    @staticmethod
    def compileCode():
        with open(Assembly.filename, 'a') as file:
            file.write(Assembly.header + '\n' + Assembly.code + '\n' + Assembly.footer + '\n')
    
    @staticmethod
    def printToFile(self, filename, code):
        with open(filename, 'a') as file:
            file.write(code + '\n')


class SymbolTable:
     
    table = {}
    addr = -4
                
    def getter(key):
        #verificar se a chave existe, senão, erro
        if key in SymbolTable.table:
            return SymbolTable.table[key]
        
        sys.stderr.write('ERROR: KEY NOT DECLARED')
        sys.exit(1)
        
    def setter(key, value):
        #printa o key e value
        
        #verificar se a o value[0] guardado tem o mesmo tipo do novo value a ser guardado, senao, erro
        if key in SymbolTable.table:
            if SymbolTable.table[key][0] != value[0]:
                sys.stderr.write('ERROR: VALUE TYPE NOT MATCHING')
                sys.exit(1)

            old_value_addr = SymbolTable.table[key][2]
            value.append(old_value_addr)
            SymbolTable.table[key] = value
            return

        sys.stderr.write('ERROR: KEY NOT DECLARED')
        sys.exit(1)
        
    def create(key, value):
        
        #verificar se a chave existe, senão, erro
        if key in SymbolTable.table:
            sys.stderr.write('ERROR: KEY ALREADY EXISTS')
            sys.exit(1)
            
        value.append(SymbolTable.addr)
        #print(value)
        SymbolTable.table[key] = value
        SymbolTable.addr -= 4

class Node:
    
    id = 0

    def __init__(self, value):
        self.value = value
        self.children = []
        
    def new_id():
        Node.id += 1
        return Node.id
    
    def evaluate(self):
        pass            
    

class BinOp(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.new_id()
    def evaluate(self):
        direita = self.children[0].evaluate()
        
        
        Assembly.joinCode("PUSH EBX")
        esquerda = self.children[1].evaluate()
        Assembly.joinCode("POP EAX")

        if self.value == "+":
            if direita[0] == "Int" and esquerda[0] == "Int":
                
                ##Assembly.printToFile(self, 'teseee.txt', "ADD EAX, EBX")
                Assembly.joinCode("ADD EAX, EBX")
                ##Assembly.printToFile(self, 'teseee.txt', "MOV EBX, EAX")
                Assembly.joinCode("MOV EBX, EAX")

                return ["Int", direita[1] + esquerda[1]]
        if self.value == "-":
            if direita[0] == "Int" and esquerda[0] == "Int":
                
                ##Assembly.printToFile(self, 'teseee.txt', "SUB EAX, EBX")
                Assembly.joinCode("SUB EAX, EBX")
                ###Assembly.printToFile(self, 'teseee.txt', "MOV EBX, EAX")
                Assembly.joinCode("MOV EBX, EAX")
                return ["Int", direita[1] - esquerda[1]]
        if self.value == "*":
            if direita[0] == "Int" and esquerda[0] == "Int":
                
                ##Assembly.printToFile(self, 'teseee.txt', "IMUL EAX, EBX")
                Assembly.joinCode("IMUL EAX, EBX")
                ##Assembly.printToFile(self, 'teseee.txt', "MOV EBX, EAX")
                Assembly.joinCode("MOV EBX, EAX")
                return ["Int", direita[1] * esquerda[1]]
        if self.value == "==":
            ##Assembly.printToFile(self, 'teseee.txt', "CMP EAX, EBX")
            Assembly.joinCode("CMP EAX, EBX")
            ##Assembly.printToFile(self, 'teseee.txt', "CALL binop_je")
            Assembly.joinCode("CALL binop_je")

            if direita[1] == esquerda[1]:
                return ["Int", 1]
            return ["Int", 0]
        if self.value == "<":
            ##Assembly.printToFile(self, 'teseee.txt', "CMP EAX, EBX")
            Assembly.joinCode("CMP EAX, EBX")
            ##Assembly.printToFile(self, 'teseee.txt', "CALL binop_jl")
            Assembly.joinCode("CALL binop_jl")
            if direita[1] < esquerda[1]:
                return ["Int", 1]
            return ["Int", 0]
                #return ["Int", direita[1] < esquerda[1]]
        if self.value == ">":
            ##Assembly.printToFile(self, 'teseee.txt', "CMP EAX, EBX")
            Assembly.joinCode("CMP EAX, EBX")
            #Assembly.printToFile(self, 'teseee.txt', "CALL binop_jg")
            Assembly.joinCode("CALL binop_jg")
            if direita[1] > esquerda[1]:
                return ["Int", 1]
            return ["Int", 0]
        if self.value == "&&":
            if direita[0] == "Int" and esquerda[0] == "Int":
                #Assembly.printToFile(self, 'teseee.txt', "AND EAX, EBX")
                Assembly.joinCode("AND EAX, EBX")
                #Assembly.printToFile(self, 'teseee.txt', "MOV EBX, EAX")
                Assembly.joinCode("MOV EBX, EAX")
                if direita[1] and esquerda[1]:
                    return ["Int", 1]
                return ["Int", 0]
                #return ["Int", direita[1] and esquerda[1]]
        if self.value == "||":
            if direita[0] == "Int" and esquerda[0] == "Int":
                #Assembly.printToFile(self, 'teseee.txt', "AND EAX, EBX")
                Assembly.joinCode("AND EAX, EBX")
                #Assembly.printToFile(self, 'teseee.txt', "OR EBX, EAX")
                Assembly.joinCode("OR EBX, EAX")
                if direita[1] or esquerda[1]:
                    return ["Int", 1]
                return ["Int", 0]
                #return ["Int", direita[1] or esquerda[1]]
        if self.value == ".":
                return ["String", str(direita[1]) + str(esquerda[1])]
        if self.value == "/":
            if direita[0] == "Int" and esquerda[0] == "Int":
                #Assembly.printToFile(self, 'teseee.txt', "POP EAX")
                Assembly.joinCode("POP EAX")
                #Assembly.printToFile(self, 'teseee.txt', "IDIV EAX, EBX")
                Assembly.joinCode("IDIV EAX, EBX")
                #Assembly.printToFile(self, 'teseee.txt', "MOV EBX, EAX")
                Assembly.joinCode("MOV EBX, EAX")
                return ["Int", direita[1] // esquerda[1]]

class UnOp(Node):
    
    def  __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.new_id()
    
    def evaluate(self):
        
        no = self.children[0].evaluate()
        
        if no[0] == "Int":
            if self.value == "!":
                var =  not no[1]
                return ["Int", var]
            if self.value == "+":
                return ["Int", no[1]]
            return ["Int", -1*no[1]]
    
        #QUEBRA AQUI =)
        sys.stderr.write('ERROR: TRIED UNOP WITH A STRING')
        sys.exit(1)

class IntVal(Node):
    
    def __init__(self, value):
        self.value = value
        self.id = Node.new_id()
    
    def evaluate(self):
        #utiliza a classe assembly para escrever em um arquivo
        #Assembly.printToFile(self, 'teseee.txt', 'MOV EBX, ' + str(self.value))
        Assembly.joinCode('MOV EBX, ' + str(self.value))

        return ["Int", int(self.value)]
    
class StringVal(Node):
    
    def __init__(self, value):
        self.value = value
        self.id = Node.new_id()
    
    def evaluate(self):
        return ["String", str(self.value)]

class NoOp(Node):
    
    def __init__(self):
        self.id = Node.new_id()
        pass
    
    def evaluate(self):
        pass

class Identifier(Node):
    
    def __init__(self, value):
        self.value = value
        self.id = Node.new_id()
    
    def evaluate(self):
        #Assembly.printToFile(self, 'teseee.txt', 'MOV EBX, [EBP' + str(SymbolTable.getter(self.value)[2]) + ']')
        Assembly.joinCode('MOV EBX, [EBP' + str(SymbolTable.getter(self.value)[2]) + ']')
        return SymbolTable.getter(self.value)        
        
class Assignment(Node):
    
    def __init__(self, value, children):
        
        self.value = value
        self.children = children
        self.id = Node.new_id()
    
    def evaluate(self):
        SymbolTable.setter(self.value, self.children[0].evaluate())
        #Assembly.printToFile(self, 'teseee.txt', 'MOV [EBP' + str(SymbolTable.getter(self.value)[2]) + '], EBX')
        Assembly.joinCode('MOV [EBP' + str(SymbolTable.getter(self.value)[2]) + '], EBX')

class VarDec(Node):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.new_id()
    
    def evaluate(self):
        if len(self.children) == 1:
            if self.value == "Int":
                SymbolTable.create(self.children[0], [self.value, 0])  
                #Assembly.printToFile(self, 'teseee.txt', 'PUSH DWORD 0')
                Assembly.joinCode('PUSH DWORD 0')
            elif self.value == "String":
                #Assembly.printToFile(self, 'teseee.txt', 'PUSH DWORD 0')
                Assembly.joinCode('PUSH DWORD 0')
                SymbolTable.create(self.children[0], [self.value, ""]) 
                
        elif len(self.children) == 2:
            if self.value == "Int" and self.children[1].evaluate()[0] == "Int":
                SymbolTable.create(self.children[0], [self.value, self.children[1].evaluate()[1]])
            if self.value == "String" and self.children[1].evaluate()[0] == "String":
                SymbolTable.create(self.children[0], [self.value, self.children[1].evaluate()[1]])
            
class Read(Node):
    
    def __init__(self):
        self.id = Node.new_id()
        pass
        
    def evaluate(self):
        return ["Int", int(input())]
    
class Block(Node):
    
    def __init__(self, children):
        self.children = children
        self.id = Node.new_id()

    def evaluate(self):
        for child in self.children:
            child.evaluate()

class While(Node):
    
    def __init__(self, children):
        self.children = children
        self.id = Node.new_id()
    
    def evaluate(self):
        #print(self.children[0].evaluate())
        #Assembly.printToFile(self, 'teseee.txt', 'LOOP_' + str(self.id) + ':')
        Assembly.joinCode('LOOP_' + str(self.id) + ':')
        self.children[0].evaluate()
        #Assembly.printToFile(self, 'teseee.txt', 'CMP EBX, False')
        Assembly.joinCode('CMP EBX, False')
        #Assembly.printToFile(self, 'teseee.txt', 'JE EXIT_' + str(self.id))
        Assembly.joinCode('JE EXIT_' + str(self.id))
        #while res_filho_0[1]:
        self.children[1].evaluate()
        #Assembly.printToFile(self, 'teseee.txt', 'JMP LOOP_' + str(self.id))
        Assembly.joinCode('JMP LOOP_' + str(self.id))
        #Assembly.printToFile(self, 'teseee.txt', 'EXIT_' + str(self.id) + ':')
        Assembly.joinCode('EXIT_' + str(self.id) + ':')

            
class If(Node):
    
    def __init__(self, children):
        self.children = children
        self.id = Node.new_id()
    
    def evaluate(self):
        #Assembly.printToFile(self, 'teseee.txt', 'IF_' + str(self.id) + ':')
        Assembly.joinCode('IF_' + str(self.id) + ':')
        if_condition = self.children[0].evaluate()[1]
        #Assembly.printToFile(self, 'teseee.txt', 'CMP EBX, False')
        Assembly.joinCode('CMP EBX, False')
        #Assembly.printToFile(self, 'teseee.txt', 'JE ELSE_' + str(self.id))
        Assembly.joinCode('JE ELSE_' + str(self.id))
        #if if_condition:
        self.children[1].evaluate()
        #Assembly.printToFile(self, 'teseee.txt', 'JMP END_IF_' + str(self.id))
        Assembly.joinCode('JMP END_IF_' + str(self.id))
        #Assembly.printToFile(self, 'teseee.txt', 'ELSE_' + str(self.id))
        Assembly.joinCode('ELSE_' + str(self.id))
        #else:
        if len(self.children) == 3:
                #basicamente verifica se tem um else, o if não obrigatoriamente vai ser verdade
            self.children[2].evaluate()
        #Assembly.printToFile(self, 'teseee.txt', 'END_IF_' + str(self.id))
        Assembly.joinCode('END_IF_' + str(self.id))
        

class Print(Node):
        def __init__(self, children):
            self.children = children
            self.id = Node.new_id()
        
        def evaluate(self):
            pt1 = self.children[0].evaluate()
            #Assembly.printToFile(self, 'teseee.txt', 'PUSH EBX')
            Assembly.joinCode('PUSH EBX')
            #Assembly.printToFile(self, 'teseee.txt', 'CALL print')
            Assembly.joinCode('CALL print')
            #Assembly.printToFile(self, 'teseee.txt', 'POP EBX')
            Assembly.joinCode('POP EBX')
            print(pt1[1])    
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


        elif self.source[self.position] == ".":
            self.next = Token("OPERATOR", ".")
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
        
        elif self.source[self.position] == ':':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == ':':
                self.next = Token("OPERATOR", "::")
                self.position = self.position + 2
                return
            else:
                self.next = Token("OPERATOR", ":")
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
        
        elif self.source[self.position] == '"': # se for string, vai concatenando até achar o fechamento
            self.position = self.position + 1
            value = ""
            
            while self.position < len(self.source) and self.source[self.position] != '"':
                value = value + self.source[self.position]
                self.position = self.position + 1
            
            #lembrete: colocar um std error :) 
            
            #para consumir o fechamento (") 
            self.position = self.position + 1
            self.next = Token("STRING", value)
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
            
            elif value == "Int":
                self.next = Token("TYPE", value)
                return 
            
            elif value == "String":
                self.next = Token("TYPE", value)
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
        
        if tokenizer.next.type == 'STRING':
            name = tokenizer.next.value
            tokenizer.selectNext()
            stringVal = StringVal(name)
            return stringVal
                
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
                
            if tokenizer.next.value == ".":
                tokenizer.selectNext()
                noDois = Parse.parseTerm(tokenizer)
                noUm = BinOp(".", [noUm, noDois])
                
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
            
        return Block(children)
    
    @staticmethod
    def ParseStatement(tokenizer):
        if tokenizer.next.value == '\n' and tokenizer.next.type == "QUEBRA_LINHA":
            tokenizer.selectNext()
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
            
            elif tokenizer.next.type == 'OPERATOR' and tokenizer.next.value == '::':
                
                tokenizer.selectNext()
                
                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "Int":
                    
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == "QUEBRA_LINHA" and tokenizer.next.value == '\n':
                        tokenizer.selectNext()
                        
                        children = [name]
                        
                        return VarDec("Int", children)
                    
                    elif tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                        tokenizer.selectNext()
                        
                        children = [name, Parse.ParseRelExpression(tokenizer)]
                        
                        return VarDec("Int", children)
                    
                    
                if tokenizer.next.type == "TYPE" and tokenizer.next.value == "String":
                    
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == "QUEBRA_LINHA" and tokenizer.next.value == '\n':
                        tokenizer.selectNext()
                        
                        children = [name]
                        
                        return VarDec("String", children)
                    
                    elif tokenizer.next.type == "OPERATOR" and tokenizer.next.value == "=":
                        tokenizer.selectNext()
                        
                        children = [name, Parse.ParseRelExpression(tokenizer)]
                        
                        return VarDec("String", children)
                    
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
                        
                        #novo trecho que faltava, consumir o end
                        tokenizer.selectNext()
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
            #printa o token que deu erro
            #sys.stderr.write('ERROR: NAO CONSEGUIU CONSUMIR O TOKEN')
            sys.stderr.write(codigo_fonte)
            sys.exit(1)
       
    @staticmethod
    def run(code, archive_name):

        tokenizer = Tokenizer(code, 0)
        tokenizer.selectNext()
        
        Assembly.setFileName(archive_name)

        arvore = Parse.ParseBlock(tokenizer)
        if tokenizer.next.type != 'EOF':
            sys.stderr.write('ERROR: EOF NOT FOUND')
            sys.exit(1)
            
        arvore.evaluate()
        
        Assembly.compileCode()
        
class PrePro:
    
    @staticmethod
    def filter(code):
        code_filtered = re.sub(r'#.*\n', '', code, flags=re.MULTILINE).replace("\s", "")
        codigo_fonte = code_filtered 
        return code_filtered


def read_file(file):
    with open(file, 'r') as f:
        return f.read()

#string = 'test142.txt'
#archive_name = string

string = sys.argv[1]
archive_name = sys.argv[0]

test_files = read_file(string)
Parse.run(PrePro.filter(test_files), archive_name)

    
    
    
    