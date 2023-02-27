import sys 
import re 
#string = sys.argv[1]


LIST_TERM = ['*','/']
LIST_EXP = ['+','-']

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
                if self.source[self.position] == '*' or self.source[self.position] == '/' or self.source[self.position] == '+' or self.source[self.position] == '-':
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
    def parseTerm(tokenizer):
        resultado = 0
        
        if tokenizer.next.type == 'NUMBER':
            
            resultado += int(tokenizer.next.value)
            tokenizer.selectNext()
            
            while tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_TERM:
                
                if tokenizer.next.value == '*':
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == 'NUMBER':
                        if tokenizer.next.type == 'NUMBER':
                            resultado *= int(tokenizer.next.value)
                    else:
                        sys.stderr.write('ERROR: TWO OPERATORS IN A ROW')
                        sys.exit(1)
                    
                        
                elif tokenizer.next.value == '/':
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == 'NUMBER':
                        if tokenizer.next.type == 'NUMBER':
                            resultado = resultado//int(tokenizer.next.value)

                    else:
                        sys.stderr.write('ERROR: TWO OPERATORS IN A ROW')
                        sys.exit(1)
                        
                tokenizer.selectNext()
            
            return resultado
        
        else:
            sys.stderr.write('ERROR: NUMBER IS NOT THE FIRST TOKEN')
            sys.exit(1)
    
    @staticmethod
    def ParseExpression(tokenizer):
        resultado = 0
        
        resultado += Parse.parseTerm(tokenizer)
        
        while tokenizer.next.type == 'OPERATOR' and tokenizer.next.value in LIST_EXP:
            
            if tokenizer.next.value == '+':
                tokenizer.selectNext()
                resultado += Parse.parseTerm(tokenizer)
                
            elif tokenizer.next.value == '-':
                tokenizer.selectNext()
                resultado -= Parse.parseTerm(tokenizer)
                
        return resultado
        
        
    
    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.selectNext()
        
        result = Parse.ParseExpression(tokenizer)

        if tokenizer.next.type != 'EOF':
            sys.stderr.write('ERROR: EOF NOT FOUND')
            sys.exit(1)
            
        return result

class PrePro:
    
    @staticmethod
    def filter(code):
        #code_filtered = re.sub(r"#.*\n", "", code, flags=re.MULTILINE)
        code_filtered = re.sub(r"#.*$", "", code)
        return code_filtered
    

teste = "1+ * #abc"
        
print(Parse.run(PrePro.filter(teste)))

    
    
    
    