# `lambda`: an execution trace
we will step through the following code:
```scheme
(define circle-area (lambda (r) (* pi (* r r))))
(circle-area (+ 5 5))
```
## parsing
in frame 1, the line `(define circle-area (lambda (r) (* pi (* r r))))` is parsed to `['define', 'circle-area', ['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`.

## defining a lambda function
since `x[0]` is `define`, we execute the following code block in frame 1:
```python
elif x[0] == 'define':
    (_, var, exp) = x
    env[var] = eval(exp, env)
```
`var` is bound to `circle-area` and `exp` is bound to the expression`['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`. 

we execute `eval(exp)`, which triggers the following code block in frame 2:
```python
elif x[0] == 'lambda':
    (_, parms, body) = x
    return Procedure(parms, body, env)
```
in frame 2, `x` is `['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`. `parms` is set to `['r']`, `body` is set to `['*', 'pi', ['*', 'r', 'r']]`, and `env` is set to the global environment. these elements are used to instantiate a `Procedure` object.

### creating a `Procedure` object
a `Procedure` object is defined by:
```python
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms = parms 
        self.body = body
        self.env = env  # instantiated with global environment
    def __call__(self, *args):  # http://hplgit.github.io/primer.html/doc/pub/class/._class-solarized003.html
        return eval(self.body, Env(self.parms, args, self.env))
```
a few observations:
* a `Procedure` is instantiated with the global environment. that means a procedure (aka function or method) has access to the global namespace, but not the other way around.
* the special method `__call__` allows us to call `Procedure` as it's a function, even though we've implemented it as an object.

### returning to frame 1 with a `Procedure` object
frame 2 returns a `Procedure` and is bound to `env[var]` in frame 1. 

in other words, the symbol `circle-area` is bound to a `Procedure` object that has been instantiated with `['r']` as its parameter, `['*', 'pi', ['*', 'r', 'r']]` as its body, and the global env as its environment.

## line 2: calling our lambda function
in norvig's example, the next line to be executed is `(circle-area (+ 5 5))` in frame 1. this expression is parsed to `['circle-area', ['+', 5, 5]]`.

it doesnt satisfy any of the conditional statements so we execute the following code block:
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
`x[0]` is `circle-area`, which is bound to `proc`. we evaluate the second expression `['+', 5, 5]`, which kicks off frame 2. frame 2's result will be bound to frame 1's `args`.

in frame 2, `x` is the expression `['+', 5, 5]`. `x[0]` is `'+'` and is therefore bound to `op.add`. `args` is evaluated as `[eval(5), eval(5)]`, or `[5,5]`. finally, `eval(*[5, 5])` evaluates to `10`, which is returned to frame 1. 

okay, back to frame 1. we have `proc` set to `circle-area` and `args` set to 10. evaluating `proc(*args)` is the same as calling `Procedure` with the `args=10`. calling `Procedure` triggers its internal special method `__call__`, defined as:
```python
def __call__(self, *args):
    return eval(self.body, Env(self.parms, args, self.env))
```
this special method evaluates `Procedure` body, which is `['*', 'pi', ['*', 'r', 'r']]`. `eval` will use a new `Env`, instantiated with `self.parms` (which is `['r']`), `args` (equal to `(10,)`), and `self.env` (the global namespace). 

calling `eval` takes us to frame 2. `x` is now `['*', 'pi', ['*', 'r', 'r']]`. since `x[0]` is a procedure `["*"]`, we execute the following code block:
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
`proc` is set to `op.mul` (`env.find(x)` searches in the inner/local env, then searches the outer/global env) and `args` is bound to `['pi', eval(['*', 'r', 'r'])` in frame 2. 

for `args` to be fully executed, we need to `eval(['*', 'r', 'r'])`. this kicks off frame 3, which will inherit the inner/local namespace from frame 2.

in frame 3, `x` is `['*', 'r', 'r']`. just as before, `x[0]` will be bound to `op.mul` and `args` is set to `'r', 'r']`. by searching through local environment, `proc(*args)` is the same as evaluating `op.mul(*[10, 10])`. frame 3 returns `100` to frame 2.

inside frame 2, `args` is now complete and equal to `['pi', 100]`. `proc(*args)` has the effect of `op.mul(*['pi', 100])`. thus, frame 2 returns 314 to frame 1. 