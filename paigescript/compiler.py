import os, sys

validCommands = ["scream!", "feed me", "mrow {", ""]

invalidCommands = ["def", "class", "print", "for", "while", "if", "elif", "else", "global", "return", "==", "+=", "-=", "**", "/=", "*=", ]

replacableValues = [["#", "."], ["nom ->", "+="], ["plp ->", "-="], ["omnom ->", "*="], ["plplp ->", "/="], ["->", "="], [">^n^<", "<"], [">^u^<", ">"], ["=^u^=", ">="], ["=^n^=", "<="], ["omnomnom", "**"], ["omnom", "*"], ["nom", "+"], ["my.", "self."], ["~", ""], ["plplp", "/"], ["plp", "-"], ["yee", "True"], ["nah", "False"], ["bleh", "return"], ["mewn't", "else"], ["mewt", "elif"], ["mew", "if"], ["make", "=="], ["my cats:", "global"]]

def checkInQuots(line, value):
    a = line.find(":")
    b = line.find(";")
    c = line.find(value)
    d = None
    if "=uwu=" in line:
        d = line.find("=uwu=")
    if c > a and c < b:
        return True
    if d != None and c > d:
        return True
    return False

def checkValid(line):
    for el in invalidCommands:
        if el in line:
            if not checkInQuots(line, el):
                return False, el
    return True, None


def main2():
    f = open("paigescript\paigeScript.txt", "r")
    code = f.readlines()
    f.close()

    validLine = True
    # inQuotes = False

    f = open("runner.py", "w")
    
    for line in code:
        validLine = checkValid(line)[0]
        if validLine == False:
            return "Invalid"
        
        for val in replacableValues:
            if not checkInQuots(line, val[0]):
                line = line.replace(val[0], val[1])
        if "=uwu=" in line:
            index = line.find("=uwu=")
            line = line[0:index]
        
        if "kitty" in line:
            a = line.find("{")
            b = line.find("}")
            name = line[a+1:b]
            params = None
            if "<" in line:
                c = line.find("<")
                d = line.find(">")
                params = line[c+1:d]
            if "am big" in line:
                line = "class " + name + "^^"
            if "boop" in line:
                e = line.find("kitty ")
                if params != None:
                    line = e * " " + "def __init__(self, " + params + ")^^\n"
                else:
                    line = e * " " + "def __init__(self)^^\n"
            if "am tiny" in line:
                e = line.find("am")
                if params != None:
                    line = e * " " + "def " + name + "(self," + params + ")^^\n"
                else:
                    line = e * " " + "def " + name + "(self)^^\n"
            if "am smol" in line:
                e = line.find("am")
                if params != None:
                    line = e * " " + "def " + name + "(" + params + ")^^\n"
                else:
                    line = e * " " + "def " + name + "()^^\n"
        
        if "m" in line and "ow" in line and "mrow" not in line:
            a = line.find("m")
            pos = a
            b = line.find("ow")
            range = line[a+1:b]
            var = None

            if line.strip()[0] != "m":
                var = line[:a].strip()
                pos = line.find(var[0])

            if var != None:
                line = pos  * " " + "for " + var + " in range(" + str(len(range)) + ")^^\n"
            else:
                line = pos * " " + "for someKindaVar in range(" + str(len(range)) + ")^^\n"
        
        if "scream!" in line:
            a = line.find("!")
            b = line.find("scream!")
            content = line[a+2:].strip()
            if "catcon(" in content:
                while "catcon(" in content:
                    content = content.replace("catcon(", "str(")
            line = b * " " + "print(" + content + ")\n"

        if "ok" in line and "?" in line:
            a = line.find("ok")
            b = line.find("?")
            params = None
            if "<" in line:
                c = line.find("<")
                d = line.find(">")
                params = line[c+1:d]
            if params == None:
                content = line[a+3:b]
                line = content + "()"
            else:
                content = line[a+3:c]
                line = content + "(" + params + ")\n"

        if "feed me" in line:
            y = line.find("feed")
            a = line.find("<")
            b = line.find(">")
            var = line[a+1:b]
            content = line[b+2:].strip()
            dataType = None
            if "(" in line:
                y, c = line.find("("), line.find("(")
                d = line.find(")")
                typ = line[c+1:d]
                if typ == "yarn":
                    dataType = "str"
                if typ == "num":
                    dataType = "int"
                if typ == "dot":
                    dataType = "float"
            if dataType != None:
                line = y * " " + var + " = " + dataType + "(input(" + content + "))\n"
            else:
                line = y * " " + var + " = input(" + content + ")\n"
        
        if "kitten" in line:
            a = line.find("kitten")
            b = line.find("{")
            className = line[:a-1].strip()
            name = line[a+6:b].strip()
            params = line[b+1:-2].strip()
            # print(className, name, params)
            pos = line.find(className[0])
            line = pos * " " + name + " = " + className + "(" + params + ")\n"
        
        if "pls" in line:
            a = line.find("pls")
            params = None
            b = len(line)
            if "<" in line:
                b = line.find("<")
                c = line.find(">")
                params = line[b+1:c]
            name = line[:a].strip()
            func = line[a+3:b].strip()
            pos = line.find(name[0])

            if params != None:
                line = pos * " " + name + "." + func + "(" + params + ")\n"
            else:
                line = pos * " " + name + "." + func + "()\n"

        if "mrow" in line:
            pos = line.find("mrow")
            a = line.find("{")
            b = line.find("}")
            condition = line[a+1:b]
            line = pos * " " + "while " + condition + "^^\n"

        while ":" in line:
            line = line.replace(":", "\"")
        while ";" in line:
            line = line.replace(";", "\"")

        line = line.replace("^^", ":")
        f.write(line)
    f.close()

    if __name__ == '__main__':
        try:
            os.system('python runner.py')
        except:
            print("SYNTAX ERROR AAAHH!!!")
            print("   Sad kitty ^;n;^")

    

yee = main2()

if yee == "Invalid":
    print("INVALID COMMAND AAAHHH\n\tMad kitty =^òwó^=")


sys.exit()