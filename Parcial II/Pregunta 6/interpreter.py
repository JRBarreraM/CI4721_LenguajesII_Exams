import sys, operator
from stack import Stack

program = []

stack = Stack()

if len(sys.argv) < 2:
    print("Debe especificar el archivo")

with open (sys.argv[1]) as f:
    for line in f:
        if (len(line.split()) > 0):
            program.append(line)

# Añadir los tags
for line in program:
    inst = line.split()
    if (inst[0][-1] == ":"):
        stack.tags[inst.pop(0)[:-1]] = stack.pointer
    stack.pointer += 1

stack.pointer = 0

# Corrida
while(stack.pointer < len(program)):
    line = program[stack.pointer]
    inst = line.split()

    if (inst[0][-1] == ":"):
        inst.pop(0)

    if (len(inst) == 0):
        pass

    elif (inst[0] == "PUSH"):
        stack.push(inst[1])
    elif (inst[0] == "POP"):
        stack.pop()

    elif (inst[0] == "ADD"):
        stack.arith_bin_op(operator.add)
    elif (inst[0] == "SUB"):
        stack.arith_bin_op(operator.sub)    
    elif (inst[0] == "MUL"):
        stack.arith_bin_op(operator.mul)
    elif (inst[0] == "DIV"):
        stack.arith_bin_op(operator.floordiv)

    elif (inst[0] == "AND"):
        stack.bool_bin_op(operator.and_)
    elif (inst[0] == "OR"):
        stack.bool_bin_op(operator.or_)

    elif (inst[0] == "LT"):
        stack.arith_bin_op(operator.lt)
    elif (inst[0] == "LE"):
        stack.arith_bin_op(operator.le)
    elif (inst[0] == "GT"):
        stack.arith_bin_op(operator.gt)
    elif (inst[0] == "GE"):
        stack.arith_bin_op(operator.ge)
    elif (inst[0] == "EQ"):
        stack.arith_bin_op(operator.eq)
    elif (inst[0] == "NEQ"):
        stack.arith_bin_op(operator.ne)

    elif (inst[0] == "UMINUS"):
        stack.arithUnOp(operator.neg)
    elif (inst[0] == "NOT"):
        stack.bool_un_op(operator.not_)

    elif (inst[0] == "RVALUE"):
        stack.rvalue(inst[1])
    elif (inst[0] == "LVALUE"):
        stack.lvalue(inst[1])
    elif (inst[0] == "ASSIGN"):
        stack.assign()

    elif (inst[0] == "GOTO"):
        stack.goto(inst[1])
        continue
    elif (inst[0] == "GOTRUE"):
        stack.go_true(inst[1])
        continue
    elif (inst[0] == "GOFALSE"):
        stack.go_false(inst[1])
        continue

    elif (inst[0] == "READ"):
        stack.read(inst[1])
    elif (inst[0] == "PRINT"):
        stack.custom_print(inst[1])

    elif (inst[0] == "RESET"):
        stack.reset()

    elif (inst[0] == "EXIT"):
        sys.exit()

    stack.pointer += 1