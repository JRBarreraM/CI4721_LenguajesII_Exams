import sys

ruleList = {}
precedence = {}
terminals = set()
phraseSize = 0
precendeString = {'>' : 'mayor', '<' : 'menor', '=' : 'igual'}
initSymbol = ""
egraph = {}
f = {}
g = {}

class pnode():
    def __init__(self, name):
        self.childNodes = []
        self.names = [name]
        self.longestPath = None
    
    def getLongestPath(self, visited):
        if self in visited:
            print("ERROR: cycle found in equivalence graph")

            cycle = str(self.names)

            for node in reversed(visited):
                cycle = str(node.names) + ' -> ' + cycle
                if node.names == self.names:
                    break
            
            cycle = "cycle: " + cycle
            print(cycle)
            sys.exit()

        else:
            if self.longestPath is None:
                if self.childNodes:
                    self.longestPath = max([child.getLongestPath(visited + [self]) for child in self.childNodes]) + 1
                else:
                    self.longestPath = 0
            return self.longestPath


def checkNoTerminalsConsecutive(rule):
    if ((len(rule)>0 and not rule[-1].isascii()) or (len(rule)>0 and len(rule[-1])>1)):
            return False
    for i in range(len(rule)-1):
        if ((rule[i].isupper() and rule[i+1].isupper()) or (len(rule[i])>1) or (not rule[i].isascii())):
            return False
    return True

def phraseInTerminals(phrase):
    for i in range(len(phrase)):
        if phrase[i] not in terminals or phrase[i] == '$':
            print("ERROR: '" + phrase[i] + "' does not exist in the grammar")
            return False
    return True

def checkConsecutiveComparables(phrase):
    for i in range(len(phrase)-1):
        foundIt = False
        if phrase[i] in precedence:
            for term in precedence[phrase[i]]:
                if term[1] == phrase[i+1]:
                    foundIt = True
                    break
            if not foundIt:
                print("ERROR: " + phrase[i] + " not comparable with " + phrase[i+1])
                return False
        else:
            print("ERROR: No precedence set for "+ phrase[i])
    return True

def showParseStep(stack, phrase, indexPhrase, action, rule=None):
    global phraseSize
    spaceCount = phraseSize + 2 - len(stack)
    spaceWCount = phraseSize + 2 - len(phrase)

    left = " "*phraseSize
    left =  left[(indexPhrase+len(phrase[:indexPhrase])-1):] + " ".join(phrase[:indexPhrase])
    right = " "*phraseSize
    right =  " ".join(phrase[indexPhrase:]) + right[:(indexPhrase+len(phrase[:indexPhrase])-1)]

    print(" ".join(stack) + "  ", end="")
    print("  "*spaceCount, end="")
    print(left + " \033[92m.\033[0m " + right, end="")
    print("  "*spaceWCount, end="")
    if (rule != None):
        print(action + ": " + ruleList[rule] + " -> " + " ".join(rule))
    else:
        print(action)

def parser(phrase):

    global phraseSize
    phraseSize = len(phrase)
    print("\nStack" + "  "*(phraseSize) + "Input" + " "*(phraseSize*3) + "Action\n")

    stack = ["$"]
    indexPhrase = 1
    e = phrase[indexPhrase]

    while True:
        p = ""
        rule = ""
        for i in (stack):
            if (not i.isupper()):
                p = i

        if p == '$' and e == '$':
            if (stack == ["$", initSymbol]):
                showParseStep(stack, phrase, indexPhrase, "accept")
                return True
            elif "".join(stack[1:]) not in ruleList:
                showParseStep(stack, phrase, indexPhrase, "reject")
                return False
            else:
                rule = "".join(stack[1:])
                stack = [stack[0]] + [ruleList[rule]]
                showParseStep(stack, phrase, indexPhrase, "reduce", "".join(rule))
                continue

        if f[p] <= g[e]:
            showParseStep(stack, phrase, indexPhrase, "read")
            stack.append(e)
            indexPhrase += 1
            e = phrase[indexPhrase]
        else:
            while stack[-1] not in terminals:
                rule = stack.pop() + rule
            
            x = stack.pop()
            rule = x + rule
            erase = 1

            while stack[-1] not in terminals or f[stack[-1]] >= g[x]:
                rule =  stack.pop() + rule
                if rule[0] in terminals:
                    x = rule[0]
                    erase += 1

            if rule in ruleList:
                stack.append(ruleList[rule])
                showParseStep(stack, phrase, indexPhrase, "reduce", "".join(rule))
                phrase = phrase[:indexPhrase-erase] + phrase[indexPhrase:]
                indexPhrase = indexPhrase - erase
            else:
                print("ERROR: No rule found to reduce: '"+rule+"'")
                return False

def rule_func(uinput):
    if (len(uinput[1]) == 1 and uinput[1].isupper() and checkNoTerminalsConsecutive(uinput[2:])):
        if ''.join(uinput[2:]) in ruleList.keys():
            print("Rule '" + uinput[1] + " -> " + ' '.join(uinput[2:]) +"' already exists")
        else:
            for i in uinput[2:]:
                if (not i.isupper()):
                    terminals.add(i)
            ruleList[''.join(uinput[2:])] = uinput[1]
            print("Rule '" + uinput[1] + " -> " + ' '.join(uinput[2:]) +"' added to grammar")
    else:
        print("ERROR: RULE not followed by <no-terminal>")

def init_func(uinput):
    global initSymbol
    if (len(uinput[1]) == 1 and uinput[1].isupper() and len(uinput) == 2):
        initSymbol = uinput[1]
        print(f'{initSymbol} is the initial symbol of the grammar')
    else:
        print("ERROR, " + uinput[1] + " is not a no-terminal symbol")

def prec_func(uinput):
    if (len(uinput) == 4 and ((uinput[1]).islower() or (uinput[1]).isascii() or  uinput[1] == '$') and uinput[2] in [">","<","="] and ((uinput[3]).islower() or (uinput[1]).isascii() or uinput[3] == '$')):
        if uinput[1] in precedence.keys():
            if uinput[2:] in precedence[uinput[1]]:
                print("This precedence already exist")
            else:
                precedence[uinput[1]].append(uinput[2:])
                terminals.add(uinput[1])
                terminals.add(uinput[3])
                print("'"+uinput[1]+"' tiene "+ precendeString[uinput[2]] + " precedencia que " + "'"+uinput[3]+"'")
        else:
            precedence[uinput[1]] = []
            precedence[uinput[1]].append(uinput[2:])
            terminals.add(uinput[1])
            terminals.add(uinput[3])
            print("'"+uinput[1]+"' tiene "+ precendeString[uinput[2]] + " precedencia que " + "'"+uinput[3]+"'")
    else:
        print("Bad syntax, expected PREC <terminal> >/</= <terminal>")

def build_func():
    egraph.clear()

    for terminal in precedence.keys():
        node = pnode("f_"+terminal)
        egraph["f_"+terminal] = node
        for prec in precedence[terminal]:
            if (prec[0] == '='):
                node.names.append("g_"+prec[1])
                egraph["g_"+prec[1]] = node
    
    for terminal in precedence.keys():
        node = egraph["f_"+terminal]
        for prec in  precedence[terminal]:
            if (prec[0] == '>'):
                if "g_"+prec[1] in egraph.keys():
                    node.childNodes.append(egraph["g_"+prec[1]])
                else:
                    gpnode = pnode("g_"+prec[1])
                    egraph["g_"+prec[1]] = gpnode
                    node.childNodes.append(egraph["g_"+prec[1]])
            elif (prec[0] == '<'):
                if "g_"+prec[1] in egraph.keys():
                    egraph["g_"+prec[1]].childNodes.append(node)
                else:
                    gpnode = pnode("g_"+prec[1])
                    egraph["g_"+prec[1]] = gpnode
                    gpnode.childNodes.append(node)

    for terminal in terminals:
        if ("g_"+terminal not in egraph.keys()):
            egraph["g_"+terminal] = pnode("g_"+terminal)
        if ("f_"+terminal not in egraph.keys()):
            egraph["f_"+terminal] = pnode("f_"+terminal)

    for terminal in terminals:
        f[terminal] = egraph["f_"+terminal].getLongestPath([])
        g[terminal] = egraph["g_"+terminal].getLongestPath([])

    print("Syntax Analyzer Constructed.")
    print("Values for f: ")
    for i in f:
        print("    "+i+": "+str(f[i]))
    print("Values for g: ")
    for i in g:
        print("    "+i+": "+str(g[i]))

def parse_func(uinput):
    global initSymbol
    if (f):
        if initSymbol != "":
            phrase = ''.join(uinput[1:])
            if phraseInTerminals(phrase):
                phrase = "$" + phrase + "$"
                if checkConsecutiveComparables(phrase):
                    return parser(phrase)
        else:
            print("ERROR: no initial symbol declared")
    else:
        print("ERROR: no syntax analyzer found")

def tester():
    print("\nTEST 1\n")
    funcCaller("INIT E")
    funcCaller("RULE E E + E")
    funcCaller("RULE E n")
    funcCaller("PREC n > +")
    funcCaller("PREC n > $")
    funcCaller("PREC + < n")
    funcCaller("PREC + > +")
    funcCaller("PREC + > $")
    funcCaller("PREC $ < n")
    funcCaller("PREC $ < +")
    funcCaller("BUILD")
    funcCaller("PARSE n+n")

    resetAll()

    print("\nTEST 2\n")
    funcCaller("PREC t = c ")
    funcCaller("PREC t < ;")
    funcCaller("PREC t < t ")
    funcCaller("PREC c < t")
    funcCaller("PREC t < i ")
    funcCaller("PREC c = f ")
    funcCaller("PREC c > c")
    funcCaller("PREC c < i ")
    funcCaller("PREC c < ; ")
    funcCaller("PREC f < t ")
    funcCaller("PREC c > $ ")
    funcCaller("PREC f > f")
    funcCaller("PREC f > c ")
    funcCaller("PREC f < i ")
    funcCaller("PREC f > ; ")
    funcCaller("PREC ; < t")
    funcCaller("PREC f > $ ")
    funcCaller("PREC ; > f ")
    funcCaller("PREC ; > c")
    funcCaller("PREC ; < i ")
    funcCaller("PREC ; > ; ")
    funcCaller("PREC i > c ")
    funcCaller("PREC ; > $")
    funcCaller("PREC i > ; ")
    funcCaller("PREC i > f ")
    funcCaller("PREC $ < t ")
    funcCaller("PREC i > $ ")
    funcCaller("PREC $ < i")
    funcCaller("PREC $ < ; ")
    funcCaller("RULE S I ")
    funcCaller("INIT S")
    funcCaller("RULE I t I c I ")
    funcCaller("RULE I t I c I f I")
    funcCaller("RULE I i ")
    funcCaller("RULE I I ; I ")
    funcCaller("PARSE ticifi")
    funcCaller("BUILD")
    funcCaller("PARSE i ; t i c i ; t i c i f i ; i")
    funcCaller("EXIT")

    resetAll()

def funcCaller(rawInput):
    uinput = rawInput.split()
    if len(uinput) == 0:
        print("Bad syntax, expected PREC <terminal> >/</= <terminal>")

    if uinput[0] == "RULE":
        rule_func(uinput)
    
    elif uinput[0] == "INIT":
        init_func(uinput)

    elif uinput[0] == "PREC":
        prec_func(uinput)

    elif uinput[0] == "BUILD":
        build_func()

    elif uinput[0] == "PARSE":
        parse_func(uinput)

    elif uinput[0] == "EXIT":
        print("Bye")
        sys.exit()
    else:
        print("Input not recognized try again")

#todo resetear todas la variables globales:
def resetAll():
    global ruleList
    ruleList = {}
    global precedence
    precedence = {}
    global terminals
    terminals = set()
    global initSymbol
    initSymbol = ""
    global egraph
    egraph = {}
    global f
    f = {}
    global g
    g = {}

def main(argv):
    if len(argv) == 1:
        if argv[1] == "-test":
            tester()
        else:
            print("ERROR: Expected -test")
    else:
        while (True):
            uinput = input("$> ").split()
            if len(uinput) == 0:
                print("Bad syntax, expected PREC <terminal> >/</= <terminal>")

            if uinput[0] == "RULE":
                rule_func(uinput)
            
            elif uinput[0] == "INIT":
                init_func(uinput)

            elif uinput[0] == "PREC":
                prec_func(uinput)

            elif uinput[0] == "BUILD":
                build_func()

            elif uinput[0] == "PARSE":
                parse_func(uinput)

            elif uinput[0] == "EXIT":
                print("Bye")
                break

            else:
                print("Input not recognized try again")

if __name__ == "__main__":
   main(sys.argv[1:])