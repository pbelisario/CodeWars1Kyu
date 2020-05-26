import re
from numbers import Number
import operator as op

# Given function
def tokenize(expression):
    if expression == "":
        return []
    regex = re.compile(r"\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

def is_number(candidate):
    regular_expression = re.compile(r"\A[-]?\d+(?:\.\d+)?\Z")
    answer = regular_expression.search(candidate)
    return bool(answer)

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.operations = {
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            '%': op.mod,
            '=': self._assign_var
        }
        self.keywords = ['fn']
    
    def _assign_var(self, name, value):
        if name in self.functions:
            raise Exception('Cannot overwrite varible with function')
        self.variables[name] = value
        return value

    def input(self, expression):
        tokens = tokenize(expression)
        # No params
        if not tokens:
            return ''
        # if the first token is a key word
        if tokens[0] in self.keywords:
            
            # it is a  new function
            if tokens[0] == 'fn':
                # save the declared function's name
                func_name  = tokens[1]
                if func_name in self.variables:
                    raise Exception('Cannot overwrite varible with function')
                
                # parameters processing
                assign_index = tokens.index('=>')
                params = tokens[2:assign_index]
                if len(params) != len(set(params)):
                    raise Exception('Duplicate of parameters')

                # expression processing
                expression = tokens[assign_index+1:]
                for token in expression:
                    # check if the token is a variable (aphabetic) not declared
                    if token.isalpha() and token not in params:
                        raise Exception('Variable "{}" not declared in the function body '.format(token))
                
                # Create the declared function
                declared_func = Function(params, expression, self)
                self.functions[func_name] = declared_func
                return ''
        else:
            value = self.evaluate_expression(tokens)
        return value


    def evaluate_expression(self, tokens):
        return self.evaluate_function(self.calculate(tokens))
    
    def calculate(self, expression, interpreter = None):
        if interpreter is None:
            interpreter = self
        output = []
        operators = []
        for token in expression:
            # save the numbers
            if is_number(token):
                try:
                    output.append(int(token))
                except ValueError:
                    output.append(float(token))
            # save the functions operators
            elif token in interpreter.functions:
                operators.append(token)
            # save the variables
            elif token in interpreter.variables:
                output.append(token)
            # processing the operations precedence
            elif token in interpreter.operations:
                if operators and operators[-1] in interpreter.operations:
                    op1 = token
                    op2 = operators[-1]
                    while operators and op2 in interpreter.operations and (
                        (left_association(op1) and precedence(op1) <= precedence(op2)) or 
                        (not left_association(op1) and precedence(op1) < precedence(op2))):
                        
                        output.append(interpreter.operations[operators.pop()])
                        try:
                            op2 = operators[-1]
                        except IndexError:
                            break
                operators.append(token)
            
            # open parentesis
            elif token  == '(':
                operators.append(token)
            # close parentesis
            elif token == ')':
                while operators and operators[-1] != '(' and operators[-1] in interpreter.operations:
                    output.append(interpreter.operations[operators.pop()])
                try:
                    parentesis = operators.pop()
                except IndexError:
                    raise Exception('ERROR: Mismatched parentesis')
                if operators and operators[-1] in interpreter.functions:
                    output.append(interpreter.functions[operators.pop()])
            else:
                output.append(token)
        while operators:
            if operators[-1] in interpreter.operations:
                output.append(interpreter.operations[operators.pop()])
            elif operators[-1] in interpreter.functions:
                output.append(interpreter.functions[operators.pop()])
            else:
                raise Exception('Invalid function')
        return output
                        

        
        
    def evaluate_function(self, tokens, interpreter = None):
        if interpreter is None:
            interpreter = self
        if tokens is None:
            return ''
        output = []
        for _, token in enumerate(tokens):
            if isinstance(token, Number):
                output.append(token)
            elif isinstance(token, Function):
                try:
                    args = [interpreter.variables[output.pop()] if output[-1] in interpreter.variables else output.pop() for _ in range(token.count_params)]
                except IndexError:
                    raise Exception('Error: Incorrect number of arguments in the function')
                result = token(*args)
                output.append(result)
            elif callable(token):
                right = output.pop()
                left = output.pop()

                if right in interpreter.variables:
                    right = interpreter.variables[right]
                if isinstance(right, str):
                    raise Exception('Error: Variable referenced before assignment')
                if left in interpreter.variables and token != interpreter.operations['=']:
                    left = interpreter.variables[left]
                result = token(left, right)
                output.append(result)
            elif isinstance(token, str):
                output.append(token)
        if len(output) > 1:
            raise Exception('Error: Invalid sintax')
        try:
            if output[0] in interpreter.variables:
                return interpreter.variables[output[0]]
            elif isinstance(output[0], str):
                raise Exception('Undeclared Variable')
            else:
                return output[0]
        except IndexError:
            return ''

class Function:
    def __init__(self, params, expr, interp):
        self.parameters = params
        self.expression = expr
        self.interpreter = interp
        self.count_params = len(params)

    def __call__(self, *args):
        self.interpreter.variables.update(zip(self.parameters, args))
        return self.interpreter.evaluate_function(self.interpreter.calculate(self.expression, self.interpreter), self.interpreter)


def precedence(op):
    if op == '=':
        return 1
    elif op == '+' or op == '-':
        return 2
    elif op == '*' or op == '/' or op == '%':
        return 3
    else:
        raise Exception('{} is not a valid operator'.format(op))
        
def left_association(op):
    return not (op == '=')
    
# Test
interpreter = Interpreter()
    
# Basic arithmetic
print(interpreter.input("1 + 1"), 2)
print(interpreter.input("2 - 1"), 1)
print(interpreter.input("2 * 3"), 6)
print(interpreter.input("8 / 4"), 2)
print(interpreter.input("7 % 4"), 3)

# Variables
print(interpreter.input("x = 1"), 1)
print(interpreter.input("x"), 1)
print(interpreter.input("x + 3"), 4)


# Functions
interpreter.input("fn avg x y => (x + y) / 2")
print(interpreter.input("avg 4 2"), 3)
