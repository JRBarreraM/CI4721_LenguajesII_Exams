
class Stack:
    pointer = 0
    stack = []
    tags = {}
    ids = {}

    def push(self, n):
        if (n == "true" or n == "false"):
            self.stack.append(eval(n.capitalize()))
        try: 
            self.stack.append(int(n))
        except ValueError:
            print("ERROR: Valor no es número entero o literal booleano")

    def pop(self):
        self.stack.pop()

    def arith_bin_op(self, op):
        if (len(self.stack) < 2):
            print("No hay suficientes elementos en la pila")
        elif (type(self.stack[-1]) is not int or type(self.stack[-2]) is not int):
            print("valores en pila no son enteros")
        else:
            rop = self.stack.pop()
            lop = self.stack.pop()
            self.stack.append(op(lop, rop))

    def arith_un_op(self, op):
        if (len(self.stack) < 1):
            print("ERROR: No hay suficientes elementos en la pila")
        elif (type(self.stack[-1]) is not int):
            print("ERROR: Valor en el tope de la pila no es entero")
        else:
            rop = self.stack.pop()
            lop = self.stack.pop()
            self.stack.append(op(lop, rop))

    def bool_bin_op(self, op):
        if (len(self.stack) < 2):
            print("ERROR: No hay suficientes elementos en la pila")
        elif (type(self.stack[-1]) is not bool or type(self.stack[-2]) is not bool):
            print("ERROR: Valores en el tope de la pila no son booleanos")
        else:
            self.stack.append(op(self.stack.pop(len(self.stack)-1), self.stack.pop()))

    def bool_un_op(self, op):
        if (len(self.stack) < 1):
            print("ERROR: No hay suficientes elementos en la pila")
        elif (type(self.stack[-1]) is not bool):
            print("ERROR: Valor en el tope de la pila no es booleano")
        else:
            self.stack.append(op(self.stack.pop()))

    def rvalue(self, id):
        if (id in self.ids):
            self.stack.append(self.ids[id])
        else:
            print(f'ERROR: Identificador \"{id}\" aún no tiene un valor asignado')

    def lvalue(self, id):
        self.stack.append("l " + id)

    def assign(self):
        if (len(self.stack) < 2):
            print("ERROR: No hay suficientes elementos en la pila")
        elif (type(self.stack[-1]) is int or type(self.stack[-1]) is bool or len(self.stack[-1].split()) != 2):
            print("ERROR: El valor en el tope de la pila no es un l-value")
        elif (type(self.stack[-2]) is not int and type(self.stack[-2]) is not bool and len(self.stack[-2].split()) == 2):
            print("ERROR: No se le puede asignar un l-value a un l-value")
        else:
            lval = self.stack.pop().split()[1]
            self.ids[lval] = self.stack.pop()

    def goto(self, tag):
        if (tag not in self.tags):
            print(f'ERROR: La etiqueta \"{tag}\" no esta asociada a ninguna instrucción')
            self.pointer += 1
        else:
            self.pointer = self.tags[tag]

    def go_true(self, tag):
        if (tag not in self.tags):
            print(f'ERROR: La etiqueta \"{tag}\" no esta asociada a ninguna instrucción')
        elif(len(self.stack) < 1):
            print("ERROR: No hay suficientes elementos en la pila")
        elif (type(self.stack[-1]) is not bool):
            print("ERROR: Valor en el tope de la pila no es booleano")
        elif (self.stack.pop()):
            self.pointer = self.tags[tag]
            return
        self.pointer += 1

    def go_false(self, tag):
        if (tag not in self.tags):
            print(f'ERROR: La etiqueta \"{tag}\" no esta asociada a ninguna instrucción')
        elif(len(self.stack) < 1):
            print("ERROR: No hay suficientes elementos en la pila")
        elif (type(self.stack[-1]) is not bool):
            print("ERROR: Valor en el tope de la pila no es booleano")
        elif (not self.stack.pop()):
            self.pointer = self.tags[tag]
            return
        self.pointer += 1

    def read(self, id):
        v = input(f'Introduzca valor de \"{id}\": ')
        if (v == "true" or v == "false"):
            self.ids[id] = eval(v.capitalize())
        else:
            try:
                self.ids[id] = int(v)
            except ValueError:
                print("ERROR: Valor no es un número entero o literal booleano")

    def custom_print(self, id):
        if (id in self.ids):
            print(self.ids[id])
        else:
            print(f'ERROR: Identificador \"{id}\" aún no tiene un valor asignado')

    def reset(self):
        self.stack = []
        self.ids = {}
        for i in self.tags:
            if (self.tags[i] <= self.pointer):
                self.tags.pop(i)