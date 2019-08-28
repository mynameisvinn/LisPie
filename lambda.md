## `lambda` procedure: an execution trace
we have source code `(define circle-area (lambda (r) (* pi (* r r))))`, which is parsed to `['define', 'circle-area', ['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`.

since `x[0]` is `define`, we execute the following code block in frame 1:
```python
elif x[0] == 'define':
    (_, var, exp) = x
    env[var] = eval(exp, env)
```
`var` is bound to `circle-area` and `exp` is set to `['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`. in the following line, we execute `eval(exp)`, which triggers the following code block in frame 2:
```python
elif x[0] == 'lambda':
    (_, parms, body) = x
    return Procedure(parms, body, env)
```
in frame 2, `x` is `['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`. `parms` is set to `['r']` and `body` is set to `['*', 'pi', ['*', 'r', 'r']]`, and then used to instantiate a `Procedure` object.

### creating a procedure object
a `Procedure` object is defined by:
```python
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms = parms 
        self.body = body
        self.env = env  # a local env for local namespace
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))
```




we execute the next line of code `(circle-area (+ 5 5))`. it doesnt satisfy any of the conditional statements so we execute this code block:
```python
else:
	proc = eval(x[0], env)
	args = [eval(exp, env) for exp in x[1:]]
	return proc(*args)
```
`x[0]` is `circle-area`, which means the variable `proc` is now bound to `['lambda', ['r'], ['*', 'pi', ['*', 'r', 'r']]]]`