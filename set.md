# set
with the syntax `(set! *symbol exp*)`, the `set` special form triggers the following block:
```python
elif x[0] == 'set!':           # (set! var exp)
	(_, var, exp) = x
	env.find(var)[var] = eval(exp, env)
```
it evaluates `exp` and binds it to an existing variable/symbol. `set` cannot create a new symbol in the environment.

## what's the difference between `set` and `define`?
both `define` and `set` binds values to symbols in an environment. however, `set` cannot create new variable:value pairs in the environment, and can only update existing symbols. `define`, on the other hand, creates a new symbol in the environment.

```python
elif x[0] == 'define':         # (define var exp)
	(_, var, exp) = x
	env[var] = eval(exp, env)
```

## why have `set` and `define` at all?
`define` is used to construct new symbols in outer or inner environments. `set`, on the other hand, will update existing symbols, first in the inner environment, then outer. as nielsen discusses in detail: "having both `define` and `set!` gives us quite a bit of flexibiility and control over which environment is being used, at the expense of a complication in syntax."