import re

def LeerArchivo(file):
    datos = []

    with open(file) as fileName:
        lineas = fileName.readlines()
        for file in lineas:
           linea = linea.replace("\n", "")
           linea = linea.replace("\t", "")
           linea = linea.lower()
           if linea.__contains__("(") or linea.__contains__(")"):
                linea = espaciosParentesis(linea)
                datos.append(linea)
           if linea.__contains__("="):
                linea = linea.replace("=", " = ")
           if linea.__contains__(" ?"):
                linea = linea.replace(" ?", "?")  
           if linea.__contains__(": "):
               linea = linea.replace(": ", ":")
           
           listaLinea = linea.split()
           datos.append(listaLinea)

    return datos

token_patterns = [
    (r'\bdefvar\b', 'DEFINITION_VARIABLE'),
    (r'\b\d+\b', 'NUMBER'),
    (r':(front|right|left|back|around)\b', 'DIRECTION'),
    (r':(north|south|west|east)\b', 'ORIENTATION'),
    (r'\b(Dim|myXpos|myYpos|myChips|myBalloons|balloonsHere|ChipsHere|Spaces)\b', 'CONSTANT'),
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
        print(linea)
        for palabra in linea:
            p = False
            if palabra == "move":
                tokens.append(("COMMAND", palabra))
                p == True
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

def programa(tokens):
    res = True
    while tokens and res == True:
        res = comando(tokens, res)
    print(res)

#PREGUNTAS
# en asignacion la variable es nueva o ya existía
# en run-dirs debo verificar que el primer elemento de la lista sea el mismo que el ultimo

def comando(tokens, res):
    if tokens[1][0] == "DEFINITION_VARIABLE":
        res = analizeDefVariable(tokens, res)
    elif tokens[1][0] == "ASSIGNMENT":
        res= analizeAsignacion(tokens, res)
    elif tokens[1][0] == "COMMAND2":
        res = analizeCommandComplejo(tokens, res)
    elif tokens[1][0] == "COMMAND1":
        res = analizeCommandSimple(tokens, res)
    elif tokens[1][0] == "CONTROL_STRUCTURE":
        res = control_estructura(tokens)
    elif tokens[1][0] == "ELEMENT":
        res = funcion_llamada(tokens)
    elif tokens[0][0] and tokens[0][1] == "LPAREN":
        pass

    return res


def analizeDefVariable(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        tokens.pop(0)
        if tokens[0][0] == "ELEMENT":
            if tokens[1][0] == "NUMBER"  or "CONSTANT":
                listaVariables.append(tokens[0])
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
    return res



def analizeCommandSimple(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        if tokens[0][1] == "move" or "skip":
            tokens.pop(0)
            if tokens[0][0] == "NUMBER" or "CONSTANT":
                tokens.pop(0)
            elif tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                tokens.pop(0)
            else:
                res = False
        elif tokens[0][1] == "turn" or "face":
            if tokens[0][1] == "turn":
                instruction = "DIRECTION"
            else:
                instruction = "ORIENTATION"
            tokens.pop(0)
            if tokens[0][0] == instruction:
                tokens.pop(0)
            else:
                res = False
        elif tokens[0][1] == "put" or "pick":
            tokens.pop(0)
            if tokens[0][0] == "ITEM_TYPE":
                tokens.pop(0)
                if tokens[0][0] == "NUMBER" or "CONSTANT":
                    tokens.pop(0)
                elif tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                    tokens.pop(0)
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

    return res
        


def analizeCommandComplejo(tokens, res):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        
        if tokens[0][1] == "move-dir" or "move-face":
            if tokens[0][1] == "move-dir":
                instruction = "DIRECTION"
            else:
                instruction = "ORIENTATION"
            tokens.pop(0)
            if tokens[0][0] == "NUMBER" or "CONSTANT":
                tokens.pop(0)
                if tokens[0][0] == instruction:
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
        elif tokens[0][1] == "runs-dirs":
            tokens.pop(0)
            lista = True
            while lista == True:
                if tokens[0][0] != "DIRECTION":
                    lista = False
                else: 
                    tokens.pop(0)
        elif tokens[0][1] == "null":
            pass
        else:
            res = False
        
    else:
        res = False
    
    if tokens[0][0] == "RPAREN":
        tokens.pop(0)
    else:
        res = False
    
    return res



    


file = input("Por favor escriba la ruta del archivo .txt que desea revisar: ")
datos = []
file = file.replace("\n", "")
file = file.replace("\t", "")
file = file.lower()
if file.__contains__("(") or file.__contains__(")"):
    file = espaciosParentesis(file)
if file.__contains__("="):
    file = file.replace("=", " = ")
if file.__contains__(" ?"):
    file = file.replace(" ?", "?")  
if file.__contains__(": "):
    file = file.replace(": ", ":")
listaLinea = file.split()
datos.append(listaLinea)

listaTokens = lexer(datos)
print(listaTokens)

programa(lexer(datos))