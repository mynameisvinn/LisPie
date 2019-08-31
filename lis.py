################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010-16; See http://norvig.com/lispy.html

from __future__ import division
import math
import operator as op

################ Types

Symbol = str          # A Lisp Symbol is implemented as a Python str; think of a symbol as a python variable - it can point to a function or a value.
List   = list         # A Lisp List is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    """Read a Scheme expression from a string.

    from norvig's site: Our function parse will take a string representation of 
    a program as input, call tokenize to get a list of tokens, and then call 
    read_from_tokens to assemble an abstract syntax tree.
    """
    tokens = tokenize(program)
    return read_from_tokens(tokens)

def tokenize(s):
    """Convert a string into a list of tokens.
    """
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    """Read an expression from a sequence of tokens.

    for example, a list of tokens eg (* ( + 2 3 ) 3) is parsed to a list of 
    strings [*, [+, 2, 3], 3], which is also known as an ast. notice that 2 and
    3 are python integers, not strings "2" and "3". 
    """

    # scenario 1: nothing inputted
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    
    # scenario 2: pop off tokens one at a time
    token = tokens.pop(0)

    # whenever we encounter an open parenthesis, we create a new list
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    
    # this case behaves as the base case
    else:
        return atom(token)

def atom(token):
    """Numbers become numbers; every other token is a symbol.

    an atom is either a number or symbol. they are atoms because they cannot be
    broken down into simpler pieces.

    everything in lisp is either an atom or a list expression. 
    """
    try: 
        return int(token)
    except ValueError:
        try: 
            return float(token)
        except ValueError:
            return Symbol(token)  # return as a string

################ Environments

def standard_env():
    """An environment with some Scheme standard procedures.
    """
    
    # first, we'll create an env, then we'll update its namespace
    env = Env()

    # add math operations to env's namespace...
    # vars function extracts all methods/attributes from the math package, through math's namespace
    # update then adds math's namespace to the environment
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    
    env.update({
        '+': op.add, 
        '-': op.sub, 
        '*': op.mul, 
        '/': op.truediv, 
        '>': op.gt, 
        '<': op.lt, 
        '>=': op.ge, 
        '<=': op.le, 
        '=': op.eq, 
        'abs':     abs,
        'append':  op.add,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

class Env(dict):
    """An environment: a dict of {'var':val} pairs, with an outer Env.

    an environment tracks namespaces, which assigns symbols to their respective 
    objects and values. interpreters use environments to keep track of state.
    """
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))  # update merger two python dicts together https://www.tutorialspoint.com/python/dictionary_update.htm
        self.outer = outer  # outer refers to global environment or namespace

    def find(self, var):
        """Find the innermost Env where var appears.

        return self, which is a dict, if var is in self's keys.
        """
        return self if (var in self) else self.outer.find(var)

################ Interaction: A REPL
global_env = standard_env()  # a global environment is initialized before repl launches

def repl():
    """A prompt-read-eval-print loop.
    """
    while True:
        input_data = input(">>>")
        parsed_data = parse(input_data)  # construct ast from code
        print("parsed expression", parsed_data)  # usually this should be an ast
        val = eval(parsed_data)  # evaluate expression
        if val is not None: 
            print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

################ Procedures

class Procedure(object):
    def __init__(self, parms, body, env):
        """
        we create an inner env namespace, which effectively works as a local 
        variable scoping
        """
        self.parms = parms 
        self.body = body
        self.env = env
    def __call__(self, *args): 
        print("parms", self.parms)
        print("args", args)
        return eval(self.body, Env(self.parms, args, self.env))

################ eval

def eval(x, env=global_env):
    """Evaluate an expression in an environment.

	everything in lisp is either an atom (number or symbol) or a list expression.
	list expressions are evaluated in one of two ways, depending on the first
	element in the list. if the first element is a function (not a reserved
	keyword), then it is evaluated. otherwise, if it is a reserved keyword (eg
	define, lambda, etc.) then it is a special form, and therefore evaluated
	in a unique way.

    evaluation happens inside an environment, because it's the environment that 
    provides namespace management, eg variables, pacakge methods, etc.

    As well as the input to execute, interpret() receives an execution context. 
    This is the place where variables and their values are stored. When a piece 
    of Lisp code is executed by interpret(), the execution context contains the 
    variables that are accessible to that code.

    x is the ast created by the parser. for example, it might look like this: 
    [*, [+, 2, 3], 3].

    the simplest example is the ast [*, 2, 3]. the variable proc is bound to the
    multiply operation. 2 and 3 are constant literals, and are combined into a 
    single list [2, 3]. then proc(*args) is evaluated, which is the equivalent
    of evaluating multiply([2, 3]).
    """
    
    # if it's a symbol aka string, find it's corresponding function from env
    # think of a symbol as a python variable - it can point to a function or a value.
    # A symbol is interpreted as a variable name; its value is the variable's value. 
    # Example: r ⇒ 10 (assuming r was previously defined to be 10)
    if isinstance(x, Symbol):      # variable reference of strings (not numbers)
        return env.find(x)[x]
    
    elif not isinstance(x, List):  # constant literal eg numbers (not strings)
        return x

    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp

    # Evaluate test; if true, evaluate and return conseq; otherwise alt. 
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    
    # scenario: update env's dict, where var: exp is the key:value pair
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)

    # set! simply binds var, which exists in env, to a new value or method
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)

    # parms refer to parameter variables
    # body is a procedural list
    # an example is (lambda (r) (* r r))
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    
    # scenario: procedure... list of atoms where x[0] is a operator and x[1:] 
    # are arguments
    else:

        """
        do not confuse this eval() with the standard eval() method. 

        the 0th element in a list is always an operation. for example, the 
        parser gives us the following ast [*, [+, 2, 3], 3]. the 0th element * 
        is an operator and is bound to the variable name "proc".

        the dict in eval(arg1, dict) limits what types of expressions can be 
        evaluated by eval. 
        https://www.programiz.com/python-programming/methods/built-in/eval
        """
        proc = eval(x[0], env)

        """
        each list has the format [operator arg1 arg2]. x[0] refers to the 
        operator and x[1:] refers to arguments. we will extract arguments into a
        single python list (not to be confused with a lisp list.)
        """
        args = [eval(exp, env) for exp in x[1:]]

        """
        finally, we pass args (a single python list containing arguments) to 
        proc, which is the operator.
        """
        return proc(*args)

if __name__ == "__main__":

    repl()  # entry point is the repl