# what is `env`?
an interpreter manipulates data through code - which is data that happens to be interpreted as instructions - with the help of an environment.[0]

an environment is a scratchpad for an interpreter: it tells an interpreter what is assigned to what or the values of variables at that moment.

## doing `python lispy.py` launches the environment
an interpreter creates a global `env` when it launches.[1]

```python
global_env = standard_env()  # helper function to instantiate Env and populate it with primitives
...
def standard_env():
    env = Env()

    # then, populate environment with primitives as key value pairs
    env.update(vars(math))
    env.update({
        '+': op.add, 
        '-': op.sub
        ...      
    })
    return env
```

## how is `Env` implemented?
a lisp environment is implemented by a python dict.

```python
class Env(dict):  # Env is a dict, no more no less
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))  # we could prepopulate Env with primitives
        self.outer = outer  # we will discuss outer shortly
```
## but why is there an `outer` parameter?
the `outer` parameter allows the interpreter distinguish between outer/global enviroments and inner/local environments.

### instantiating `Procedure` with the global `env`
we pass the global `env` when we instantiate a `Procedure` object:
```python
elif x[0] == 'lambda':
    (_, parms, body) = x
    return Procedure(parms, body, env)  # env is global env
```

### calling the `Procedure` creates a new `Env`
when we call that `Procedure` object, we construct a new `Env` with its original parameters as keys, `args` (defined at runtime) as the corresponding values, and `self.env` ( the global/outer environment, passed as an argument to the `outer` parameter). this `Env` is known as the inner environment.
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
class Env(dict):
    ...
    def find(self, var):
        return self if (var in self) else self.outer.find(var)
```
it returns the local `Env` if the symbol exists in the local `Env`'s dict. if it doesnt, it searches for the symbol in `self.outer`, the global/outer `Env`.

### scoping priorities
`find()`'s implementation means inner environments are searched first, then outer/global namepsaces. a consequence of this arrangement is that, when executing a function, an interpreter has access to both the function's local variables and global variables; however, the converse is not true, as a global function does not have access to local namespaces.

---
[0] "say your name" versus "say 'your name'" is evaluated differently by a human.

[1] cypthon instantiates a global environment too. this environment contains variable assignments, environment name (eg, {__name__:'__main__'}, imported modules, etc. you can inspect its environment with `global()`.