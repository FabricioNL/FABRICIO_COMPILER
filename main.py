import sys 
string = sys.argv[1]

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
                if self.source[self.position] == '+' or self.source[self.position] == '-':
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
    def parseExpression(tokenizer):
        resultado = 0
        
        if tokenizer.next.type == 'NUMBER':
            
            resultado += int(tokenizer.next.value)
            tokenizer.selectNext()
            
            while tokenizer.next.type == 'OPERATOR':
                
                if tokenizer.next.value == '+':
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == 'NUMBER':
                        if tokenizer.next.type == 'NUMBER':
                            resultado += int(tokenizer.next.value)
                    else:
                        sys.stderr.write('ERROR: TWO OPERATORS IN A ROW')
                        sys.exit(1)
                    
                        
                elif tokenizer.next.value == '-':
                    tokenizer.selectNext()
                    
                    if tokenizer.next.type == 'NUMBER':
                        if tokenizer.next.type == 'NUMBER':
                            resultado -= int(tokenizer.next.value)

                    else:
                        sys.stderr.write('ERROR: TWO OPERATORS IN A ROW')
                        sys.exit(1)
                        
                tokenizer.selectNext()
            
            return resultado
        
        else:
            sys.stderr.write('ERROR: NUMBER IS NOT THE FIRST TOKEN')
            sys.exit(1)
    
    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code, 0)
        tokenizer.selectNext()
        
        result = Parse.parseExpression(tokenizer)

        if tokenizer.next.type != 'EOF':
            sys.stderr.write('ERROR: EOF NOT FOUND')
            sys.exit(1)
            
        return result

print(Parse.run(string))
