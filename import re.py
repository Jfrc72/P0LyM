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
    (r':(front|right|left|back)\b', 'DIRECTION'),
    (r':(north|south|west|east)\b', 'ORIENTATION'),
    (r'\b(Dim|myXpos|myYpos|myChips|myBalloons|balloonsHere|ChipsHere|Spaces)\b', 'CONSTANT'),
    (r'=', 'ASSIGNMENT'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'(facing\?|blocked\?|can-put\?|can-pick\?|can-move\?|isZero\?|not)', 'CONDITION'), 
    (r'\b(Dim|myXpos|myYpos|myChips|myBalloons|balloonsHere|ChipsHere|Spaces)\b', 'CONSTANT'),
    (r'\b(if|loop|repeat|defun)\b', 'CONTROL_STRUCTURE'),
    (r':(balloons|chips)\b', 'ITEM_TYPE'),
    (r'\b(skip|turn|face|put|pick|move-dir|run-dirs|move-face|null)\b', 'COMMAND'),
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
    while tokens:
        comando(tokens)

'holi'

def comando(tokens):
    if tokens[1][0] == 'DEFINITION_VARIABLE':
        analizeDefVariable(tokens)
    elif tokens[1][0] == 'ASSIGNMENT':
        analizeAsignacion(tokens)
    elif tokens[1][0] == 'COMMAND':
        analizeCommand(tokens)
    elif tokens[1][0] == 'CONTROL_STRUCTURE':
        control_estructura(tokens)
    elif tokens[1][0] == 'ELEMENT':
        funcion_llamada(tokens)
    elif tokens[0][0] and tokens[0][1] == "LPAREN":
        pass


def analizeDefVariable(tokens):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        if tokens[0][0] == 'DEFINITION_VARIABLE':
            tokens.pop(0)  # Consumir el token DEFINITION_VARIABLE
            if tokens[0][0] == 'ELEMENT':
                tokens.pop(0)  # Consumir el token ELEMENT
                if tokens[0][0] == 'NUMBER'  or "CONSTANT":
                    tokens.pop(0)
                    listaVariables.append(tokens[0])
                    if tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                        tokens.pop(0)  # Consumir el token NUMBER
                        if tokens[0][0] == "RPAREN":
                            tokens.pop(0)
                        else:
                            print("False")
                    else:
                        print("False")
                else:
                    print("False")
            else:
                print("False")
        else:
            print("False")
    else:
        print("False")

def analizeAsignacion(tokens):
    if tokens[0][0] == "LPAREN":
        tokens.pop(0)
        if tokens[0][0] == 'ASSIGMENT':
            tokens.pop(0)  # Consumir el token DEFINITION_VARIABLE
            if tokens[0][0] == 'ELEMENT':
                tokens.pop(0)  # Consumir el token ELEMENT
                if tokens[0][0] == 'NUMBER'  or "CONSTANT":
                    tokens.pop(0)
                    listaVariables.append(tokens[0])
                    if tokens[0][0] == "ELEMENT" and tokens[0][1] in listaVariables:
                        tokens.pop(0)  # Consumir el token NUMBER
                        if tokens[0][0] == "RPAREN":
                            tokens.pop(0)
                        else:
                            print("False")
                    else:
                        print("False")
                else:
                    print("False")
            else:
                print("False")
        else:
            print("False")
    else:
        print("False")

        


def analizeCommand():
    pass

def analizeConstant():
    pass






    


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