# environment
an interpreter manipulates data through code (which is just data that happens to be interpreted as instructions [0]) with the help of an environment.

the `env` is a scratchpad for an interpreter: it tells an interpreter what is assigned to what or the values of variables at that moment. every object thats available to an interpreter is tracked through the environment.

## what happens when we do `python lispy.py`?
when an interpreter creates a global `env` when it launches. (in python, you can see variables and other metadata in the global environment with `global()`.)

## how is the environment `env` implemented?
a lisp environment is implemented by a python dict. (cpython's env is also implemented with a python dict.)

```python
class Env(dict):
	def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)
```
## why is there an `outer` parameter?
the `outer` parameter helps the interpreter distinguish between global/outer enviroments and local/inner environments.

### instantiating `Procedure` with the global `env`
we pass the global `env` when we define a `Procedure`:
```python
elif x[0] == 'lambda':
	(_, parms, body) = x
	return Procedure(parms, body, env)  # env is global env
```

### calling the `Procedure` creates a new `Env`
when we call that `Procedure` we construct a new `Env` with its original parameters, `args` (supplied at runtime), and `self.env` ( the global/outer environment, passed as an argument to the `outer` parameter). this `Env` is known as the inner environment.
```python
def __call__(self, *args): 
	return eval(self.body, Env(self.parms, args, self.env))  # self.env is global/outer env, Env is the local/inner env
```

### evaluating `Procedure` with the new `Env`
`Procedure`'s body, a valid lisp expression, is evaluated with a new `Env`. assuming `self.body` is a valid lisp expression and its `x[0]` is a Symbol, `find()` is called on the inner `Env`.
```python
if isinstance(x, Symbol):
    return env.find(x)[x]
```

### `find` searches for Symbols in `Env`
`find()` is defined by:
```python
def find(self, var):
	return self if (var in self) else self.outer.find(var)
```
it returns the local `Env` if the symbol exists in the local `Env`'s dict. if it doesnt, it searches for the symbol in `self.outer`, the global/outer `Env`. (this sequential ordering is why functions/procedures/methods search inner scopes first.)


[0] "say your name" versus "say 'your name'" is evaluated differently by a human.