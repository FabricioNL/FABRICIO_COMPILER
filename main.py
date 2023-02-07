import sys 
string = sys.argv[1]

def compiler(expression):  

    #PRIMEIRA VERIFICACAO
    if expression[0].isdigit() == False:
        sys.stderr.write('ERROR: FIRST CHARACTER IS NOT A NUMBER')
        sys.exit(1)
    
    if expression[-1].isdigit() == False:
        sys.stderr.write('ERROR: LAST CHARACTER IS NOT A NUMBER')
        sys.exit(1)

    #FLAGS
    operator_in_row = False

    split_expression = expression.split()
    new_expression = ''

    #SEGUNDA VERIFICACAO: DOIS NUMEROS SEGUIDOS
    for i in range(len(split_expression)-1):
            if (split_expression[i].isdigit() == True) and (split_expression[i+1].isdigit() == True):
                sys.stderr.write('ERROR: TWO NUMBERS IN ROW')
                sys.exit(1)

    for i in split_expression:
        new_expression += i

    val_numeric = ''
    expression_list = []

    for i in new_expression:
        if i.isdigit():
            val_numeric += i
        else:
            expression_list.append(val_numeric)
            expression_list.append(i)
            val_numeric = ''

    expression_list.append(val_numeric)

    #TERCEIRA VERIFICACAO: DOIS OPERADORES SEGUIDOS
    for i in range(len(expression_list)-1):
        if (expression_list[i].isdigit() == False) and (expression_list[i+1].isdigit() == False):
            sys.stderr.write('ERROR: TWO OPERATORS IN ROW')
            sys.exit(1)   

    res = eval(new_expression)
    #print(split_expression)
    #print(new_expression)
    #print(expression_list)
    print(res)
    

compiler(string)
    