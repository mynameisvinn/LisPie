################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010-16; See http://norvig.com/lispy.html

from __future__ import division
import math
import operator as op

################ Types

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    """Convert a string into a list of tokens.
    """
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    """Read an expression from a sequence of tokens.
    """
    # scenario 1: nothing inputted
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    
    # scenario 2: pop off tokens one at a time
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    """Numbers become numbers; every other token is a symbol.
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
    
    env = Env()

    # add math operations to env's namespace...
    # vars function extracts all methods/attributes from the math package, through math's namespace
    # update then adds math's namespace to the environment
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
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

    environment needs to track namespaces
    """
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))  # update merger two python dicts together https://www.tutorialspoint.com/python/dictionary_update.htm
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)

################ Interaction: A REPL
global_env = standard_env()  # a global environment is automatically initialized

def repl():
    """A prompt-read-eval-print loop.
    """
    while True:
        input_data = input(">>>")
        parsed_data = parse(input_data)  # construct ast from code
        val = eval(parsed_data)  # evaluate ast and return result
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
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))

################ eval

def eval(x, env=global_env):
    """Evaluate an expression in an environment.

    evaluation happens inside an environment, because it's the environment
    that provides namespace management, eg variables, pacakge methods, etc.
    """
    if isinstance(x, Symbol):      # variable reference
        return env.find(x)[x]
    elif not isinstance(x, List):  # constant literal
        return x                
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                          # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)

if __name__ == "__main__":

    repl()  # entry point is the repl