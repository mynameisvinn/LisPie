## `lambda`: an execution trace
lets step through the following scheme code:
```scheme
(define circle-area (lambda (r) (* pi (* r r))))
(circle-area (+ 5 5))
```
### defining a lambda function
we have source code `(define circle-area (lambda (r) (* pi (* r r))))`, which is parsed to `['define', 'circle-area', ['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`.

since `x[0]` is `define`, we execute the following code block in frame 1:
```python
elif x[0] == 'define':
    (_, var, exp) = x
    env[var] = eval(exp, env)
```
`var` is bound to `circle-area` and `exp` is set to `['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`. in the subsequent line, we execute `eval(exp)`, which triggers the following code block in frame 2:
```python
elif x[0] == 'lambda':
    (_, parms, body) = x
    return Procedure(parms, body, env)
```
in frame 2, `x` is `['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`. `parms` is set to `['r']` and `body` is set to `['*', 'pi', ['*', 'r', 'r']]`, and then used to instantiate a `Procedure` object.

### creating a `Procedure` object
a `Procedure` object is defined by:
```python
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms = parms 
        self.body = body
        self.env = env  # a local env for local namespace
    def __call__(self, *args):  # http://hplgit.github.io/primer.html/doc/pub/class/._class-solarized003.html
        return eval(self.body, Env(self.parms, args, self.env))
```
the special method `__call__` allows us to treat this object as a function.

### update global env with the `Procedure` object
frame 2 returns a `Procedure` object, instantiated with `parms`, `body`, and `env` (referring to the global env), to frame 1, where it is bound to `env[var]`. in other words, the symbol `circle-area` is bound to a `Procedure` object that has been instantiated with `['r']` as its parameter, `['*', 'pi', ['*', 'r', 'r']]` as its body, and the global env as its env.

### calling our lambda function
in norvig's example, the next line to be executed is `(circle-area (+ 5 5))`. 

it doesnt satisfy any of the conditional statements so we execute the following code block:
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
`x[0]` is `circle-area`, which means the variable `proc` is now bound to `Procedure` object that was previously created. `args` is set to `[5, 5]` in frame 1.

we now want to execute `proc(*args)`. this passes `[5, 5]` to the `Procedure`, which executes its internal special method `__call__`. this special method is defined as:
```python
return eval(self.body, Env(self.parms, args, self.env))
```
`eval` is called with the `Procedure` object's internal environment.

since `self.body` is `['*', 'pi', ['*', 'r', 'r']]`, we kick off execution in a new frame, frame 2. `x` is now `['*', 'pi', ['*', 'r', 'r']]`. since `x[0]` is a procedure `["*"]`, we execute the following code block in frame 2:
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
`proc` is set to `op.mul` and `args` is bound to `['pi', eval(['*', 'r', 'r'])`. we need to `eval(['*', 'r', 'r']`