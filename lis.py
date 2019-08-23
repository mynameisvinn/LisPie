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

    for example, (* ( + 2 3 ) 3) is parsed to [*, [+, 2, 3], 3]

    # lets look at the trace...

    in frame 0: tokens is (* ( + 2 3 ) 3)
    
    in frame 0: we encounter "(", so we create a new list L0 in frame 0. tokens is [* ( + 2 3 ) 3)] because "(" has been popped.
    
    in frame 0: we enter into the while loop in frame 0 ("WL0"). we encounter * in tokens[0] and call read_from_tokens on tokens, which is "* ( + 2 3 ) 3)". this creates frame 1. whatever is returned by read_from_tokens will be appended to L0, which is currently empty.

    in frame 1: the 0th element ["*"] is popped from tokens and, since it is an atom, it is returned to frame 0. frame 1 is destroyed. 

    in frame 0: we receive "*" from frame 1 and append it to L0. L0 is now [*]. since "*" was previously popped by frame 1, tokens is now "( + 2 3 ) 3)". we are still in the while loop WL0. since tokens[0] is not ")", we continue in this while loop. we call read_from_tokens on tokens. frame 1 is created. 

    in frame 1: we pop "(" from tokens, such that tokens is now "+ 2 3 ) 3)". since we encounter "(", we create a second list L1. we enter into a second while loop WL1. since tokens[0] is not ")", we enter into a second while loop WL1. inside WL1, we call read_from_tokens on tokens, thus creating frame 2. whatever is returned by frame 2 will be appended to this second list L1.

    in frame 2: we pop "+" from tokens. tokens is now "2 3 ) 3)". since "+" is an atom, we return "+" to frame 1 and destroy frame 2.

    in frame 1: we've received "+" from frame 2 and append it to L1. L1 is now [+]. as a reminder, tokens is "2 3 ) 3)". we are still in the while loop WL1 in frame 1 and, since we havent encountered ")" in tokens[0], we will continue to append to L1. we call read_from_tokens, which creates frame 2.

    in frame 2: we pop "2" from tokens. tokens is now "3 ) 3)". since "2" is an atom, we return "2" to frame 1 and destroy frame 2. 

    in frame 1: we've received "2" from frame 2 and append it to L1. L1 is now [+, 2]. as a reminder, tokens is "3 ) 3 )". we are still in the while loop WL1 in frame 1 and, since tokens[0] is not ")", we will call read_from_tokens, thus creating frame 2. we will take frame 2's result and append it to L1.

    in frame 2: we pop "3" from tokens. tokens is now ") 3 )". since "3" is an atom, we return "3" to frame 1 and destroy frame 2.

    in frame 1: we've received "3" from frame 2. we append 3 to L1. L1 is now [+, 2, 3]. as a reminder, tokens is ") 3 )". since tokens[0] is ")", we break out of while loop WL1 in frame 1. we pop out the ")" from tokens. tokens is now "3 )". we return L1, which is [+, 2, 3], to frame 0. frame 1 is destroyed.

    in frame 0: L0 was [*]. we've received L1 from frame 1 and append to L0.  L0 is now [*, [+, 2, 3]]. as a reminder, tokens is "3 )". tokens[0] is not ")" and therefore we continue the while loop WH0. we call read_from_tokens on tokens, which creates frame 1. frame 1's result will be appended to L0.

    in frame 1: we pop out "3" from tokens. tokens is now ")". since it is an atom, we return "3" to frame 0 and destroy frame 1.

    in frame 0: we've received "3" from frame 1. we append "3" to L0, which is now [*, [+, 2, 3], 3]. tokens is now ")". tokens[0] is ")", so we break out of the while loop WH0. we pop ")" from tokens. tokens is now empty and return L1, which is [*, [+, 2, 3], 3], to the calling function (eg parser). 
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

    environment needs to track namespaces, which assigns symbols to 
    their respective objects.
    """
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))  # update merger two python dicts together https://www.tutorialspoint.com/python/dictionary_update.htm
        self.outer = outer

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
        print(parsed_data)
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

    As well as the input to execute, interpret() receives an execution 
    context. This is the place where variables and their values are stored. 
    When a piece of Lisp code is executed by interpret(), the execution context 
    contains the variables that are accessible to that code.
    """

    """
    if it's a symbol, find it's corresponding object/function
    in the environment's dict.
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