import re

def LeerArchivo(file):
    datos = []

    with open(file) as fileName:
        lineas = fileName.readlines()
        for linea in lineas:
           linea = linea.replace("\n", "")
           linea = linea.replace("\t", "")
           linea = linea.lower()
           if linea.__contains__("(") or linea.__contains__(")"):
                linea = espaciosParentesis(linea)
           if linea.__contains__("="):
                linea = linea.replace("=", " = ")
           if linea.__contains__(" ?"):
                linea = linea.replace(" ?", "?")  
           if linea.__contains__(": "):
               linea = linea.replace(": ", ":")
           listaLinea = linea.split()
           if listaLinea != []:
            datos.append(listaLinea)

    return datos

token_patterns = [
    (r'\bdefvar\b', 'DEFINITION_VARIABLE'),
    (r'\b\d+\b', 'NUMBER'),
    (r':(front|back)\b', 'DIRECTION1'),
    (r':(right|left)\b', 'DIRECTION2'),
    (r':(around)\b', 'DIRECTION3'),
    (r':(north|south|west|east)\b', 'ORIENTATION'),
    (r'\b(Dim|myxpos|myypos|mychips|myballoons|balloonshere|chipshere|spaces)\b', 'CONSTANT'),
    (r'=', 'ASSIGNMENT'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'(facing\?|blocked\?|can-put\?|can-pick\?|can-move\?|isZero\?|not)', 'CONDITION'), 
    (r'\b(if|loop|repeat|defun)\b', 'CONTROL_STRUCTURE'),
    (r':(balloons|chips)\b', 'ITEM_TYPE'),
    (r'\b(skip|turn|face|put|pick)\b', 'COMMAND1'),
    (r'\b(move-dir|run-dirs|move-face|null)\b', 'COMMAND2')
    ]


def lexer(datos):
    tokens = []
    for linea in datos:
        for palabra in linea:
            p = False
            if palabra == "move":
                tokens.append(("COMMAND1", palabra))
                p = True
            for pattern, token_type in token_patterns:
                match =  re.match(pattern, palabra)
                if match:
                    value = match.group(0).strip()
                    tokens.append((token_type, value))
                    p = True
            if p == False:
                tokens.append(("ELEMENT", palabra))
            
                    
    return tokens

def espaciosParentesis(linea):
    if linea.__contains__("("):
        linea = linea.replace("(", " ( ")

    if linea.__contains__(")"):
        linea = linea.replace(")", " ) ")

    
    return linea

listaVariables = []
listaFunciones = []

def programa(tokens):
    res = True
    while tokens and res == True:
        res, tokens = comando(tokens, res)
    print(res)

#PREGUNTAS
# en asignacion la variable es nueva o ya existía
# en run-dirs debo verificar que el primer elemento de la lista sea el mismo que el ultimo

def comando(tokens, res):
    if tokens[1][0] == "DEFINITION_VARIABLE":
        res, tokens = analizeDefVariable(tokens, res)
        print("definicion variable" + " ---> " + str(res))
    elif tokens[1][0] == "ASSIGNMENT":
        res, tokens = analizeAsignacion(tokens, res)
        print("asignacion ---> " + str(res))
    elif tokens[1][0] == "COMMAND2":
        res, tokens = analizeCommandComplejo(tokens, res)
        print("comando2 ---> " + str(res))
    elif tokens[1][0] == "COMMAND1":
        res, tokens = analizeCommandSimple(tokens, res)
        print("comando1 ---> " + str(res))
    elif tokens[1][0] == "CONTROL_STRUCTURE":
        res, tokens = control_estructura(tokens, res)
        print("estructura de control ---> " + str(res))
    elif tokens[1][0] == "ELEMENT":
        res = funcion_llamada(tokens, res)
        print("elemento ---> " + str(res))
    elif tokens[0][0] and tokens[1][0] == "LPAREN":
        tokens.pop(0)
        while tokens[0][0] != "RPAREN" and res == True:
            res,tokens = comando(tokens, res)
        if tokens[0][0] == "RPAREN":
            tokens.pop(0)
        else:
            res =False
    else:
        res = False

    return res, tokens


def analizeDefVariable(tokens, res):
        
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        tokens.pop(0)
        if tokens[0][0] == "ELEMENT":
            if tokens[1][0] == "NUMBER"  or tokens[1][0] ==  "CONSTANT":
                listaVariables.append(tokens[0][1])
                tokens.pop(0)
                tokens.pop(0)
            elif tokens[1][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                tokens.pop(0)
            else:
                res = False
        else:
            res = False
    else:
        res = False

    if tokens[0][0] == "RPAREN":
        tokens.pop(0)
    else:
        res = False

    return res, tokens

def analizeAsignacion(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        tokens.pop(0)
        if tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
            if tokens[1][0] == "NUMBER"  or tokens[1][0] ==  "CONSTANT":
                listaVariables.append(tokens[0][1])
                tokens.pop(0)
                tokens.pop(0)
            elif tokens[1][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                tokens.pop(0)
            else:
                res = False
        else:
            res = False
    else:
        res = False

    if tokens[0][0] == "RPAREN":
        tokens.pop(0)
    else:
        res = False

    return res, tokens



def analizeCommandSimple(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        if tokens[0][1] == "move" or tokens[0][1] == "skip":
            tokens.pop(0)
            if tokens[0][0] == "NUMBER" or tokens[0][0] == "CONSTANT":
                tokens.pop(0)
            elif tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                tokens.pop(0)
            else:
                res = False
        elif tokens[0][1] == "turn" or tokens[0][1] == "face":
            if tokens[0][1] == "turn":
                instruction = ["DIRECTION2", "DIRECTION3"] 
            else:
                instruction = ["ORIENTATION"]
            tokens.pop(0)
            for ins in instruction:
                if tokens[0][0] == ins:
                    tokens.pop(0)
                else:
                    res = False
        elif tokens[0][1] == "put" or tokens[0][1] == "pick":
            tokens.pop(0)
            if tokens[0][0] == "ITEM_TYPE":
                tokens.pop(0)
                if tokens[0][0] == "NUMBER" or tokens[0][0] == "CONSTANT":
                    tokens.pop(0)
                elif tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                    tokens.pop(0)
                else:
                    res = False
            else:
                res = False
        else:
            res = False
    else:
        res = False
    
    if tokens[0][0]  == "RPAREN":
        tokens.pop(0)
    else:
        res = False

    return res, tokens
        


def analizeCommandComplejo(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        
        if tokens[0][1] == "move-dir" or tokens[0][1] == "move-face":
            if tokens[0][1] == "move-dir":
                instruction = ["DIRECTION1", "DIRECTION2"]
            else:
                instruction = ["ORIENTATION"]
            tokens.pop(0)
            if tokens[0][0] == "NUMBER" or tokens[0][0] == "CONSTANT":
                tokens.pop(0)
                for ins in instruction:
                    if tokens[0][0] == ins:
                        tokens.pop(0)
                    else:
                        res = False
            elif tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                tokens.pop(0)
                if tokens[0][0] == instruction:
                    tokens.pop(0)
                else:
                    res = False
            else:
               res = False
        elif tokens[0][1] == "run-dirs":
            tokens.pop(0)
            lista = True
            while lista == True:
                if tokens[0][0] != "DIRECTION1" or tokens[0][0] != "DIRECTION2" :
                    lista = False
                else: 
                    tokens.pop(0)
        elif tokens[0][1] == "null":
            tokens.pop(0)
        else:
            res = False
        
    else:
        res = False
    
    if tokens[0][0] == "RPAREN":
        tokens.pop(0)
    else:
        res = False
    
    return res, tokens

def analizeCondiciones(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        if tokens[0][0] == "CONDITION":
            if tokens[0][1] == "facing?" or tokens[0][1] == "can-move?":
                tokens.pop(0)
                if tokens[0][0] == "ORIENTATION":
                    tokens.pop(0)
                else:
                    res = False
            elif tokens[0][1] == "blocked?":
                tokens.pop(0)
            elif tokens[0][1] == "can-put?" or tokens[0][1] == "can-pick?":
                tokens.pop(0)
                if tokens[0][0] == "ITEM_TYPE":
                    tokens.pop(0)
                    if tokens[0][0] == "NUMBER" or tokens[0][0] == "CONSTANT":
                        tokens.pop(0)
                    elif tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                        tokens.pop(0)
                    else:
                        res = False
                else: 
                    res = False
            elif tokens[0][1] == "iszero?":
                tokens.pop(0)
                if tokens[0][0] == "NUMBER" or tokens[0][0] == "CONSTANT":
                    tokens.pop(0)
                elif tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                    tokens.pop(0)
                else:
                    res = False
            elif tokens[0][1] == "not":
                tokens.pop(0)
                analizeCondiciones(tokens, res)
            else:
                res = False
        else:
            res = False
    else:
        res = False

    if tokens[0][0] == "RPAREN":
        tokens.pop(0)
    else:
        res = False
    
    return res, tokens

def control_estructura(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        if tokens[0][0] == "CONTROL_STRUCTURE":
            tokens.pop(0)
            if tokens[0][1] == "if":
                tokens.pop(0)
                tokens, res = analizeCondiciones(tokens, res)
                comando(tokens, res)
            elif tokens[0][1] == "loop":
                tokens.pop(0)
                tokens, res = analizeCondiciones(tokens, res)
                comando(tokens, res)
            elif tokens[0][1] == "repeat":
                tokens.pop(0)
                if tokens[0][0] == "NUMBER" or tokens[0][0] == "CONSTANT" or tokens[0][0] in listaVariables:
                    tokens.pop(0)
                    comando(tokens, res)
                else:
                    res = False
            elif tokens[0][1] == "defun":
                tokens.pop(0)
                if tokens[0][0] == "ELEMENT":
                    if tokens[1][0] == "LPAREN":
                        funcion = tokens[0][1]
                        tokens.pop(0)
                        tokens.pop(0)
                        if tokens[0][0] == "ELEMENT":
                            elementos = 1
                            tokens.pop(0)
                            if tokens[0][0] == "ELEMENT":
                                elementos += 1
                                tokens.pop(0)
                                if tokens[0][0] == "ELEMENT":
                                    elementos += 1
                                    tokens.pop(0)
                                    if tokens[0][0] == "ELEMENT":
                                        elementos += 1
                                        tokens.pop(0)
                                        if tokens[0][0] == "ELEMENT":
                                            elementos += 1
                                            tokens.pop(0)
                                            listaFunciones.append((funcion, elementos))
                                        else:
                                            res = False
                                    else:
                                        res = False
                                else:
                                    res = False
                            else:
                                res = False
                        else:
                            res = False
                    else:
                        res = False
                else:
                    res = False
            else:
                res = False
        else:
            res = False
    else:
        res = False

    if tokens[0][0] == "RPAREN":
        tokens.pop(0)
    else:
        res = False

    return res, tokens

def funcion_llamada(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        if tokens[0][0] == "ELEMENT" and tokens[0][0] in listaFunciones:
            funcion = tokens[0][1]
            tokens.pop(0)
            n = funcionYparametros(listaFunciones, funcion)
            if tokens[0][0] == "LPAREN":
                tokens.pop(0)
                for i in range(0, n):
                    if tokens[i][0] == "NUMBER" or tokens[i][0] == "CONSTANT" or tokens[i][0] in listaVariables:
                        tokens.pop(0)
                    else:
                        res = False
            else:
                res = False
        else:
            res = False
    else:
        res = False

    if tokens[0][0] == "RPAREN":
        tokens.pop(0)
    else:
        res = False

    return res, tokens

def funcionYparametros(listaFunciones, funcion):
    n = 0
    while len(listaFunciones) > 0:
        if listaFunciones[0][0] == funcion:
            n = len(listaFunciones[0])
        else:
            listaFunciones.pop(0)
    return n

file = input("Por favor escriba la ruta del archivo .txt que desea revisar: ")
datos = LeerArchivo(file)
programa(lexer(datos))