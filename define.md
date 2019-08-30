# `define` expression: an execution trace
lets examine what happens to `(define r 10)`.

the parser returns the ast `['define', 'r', 10]`. it is evaluated by the following code block:
```python
elif x[0] == 'define':
	(_, var, exp) = x
	env[var] = eval(exp, env)
```
the 0th element of the ast `x` - which is `['define', 'r', 10]` - is  `define` and the code block is executed. (notice that `10` is a python integer, not a string. this conversion is handled by the `atom` function.)

`x` is unpacked such that `var` is bound to the string `r` and `exp` is bound to the value `10`. since 10 is a constant literal, `eval(10)` returns the value `10`. `env` is the environment, represented as a python dictionary, and is updated such that `env[var] = 10`. 

what happens if we evaluate `(* r r)`?. this expression doesnt satisfy any conditions so we execute the `else` block. 
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
`proc` is bound to the `multiply` operator. `r` is passed to `eval(r)`. since `r` is a str (aka symbol), we jump to this code block:
```python
if isinstance(x, Symbol):
    return env.find(x)[x]
```
from the previous step, `r` is mapped to `10` in the environment, which is really just a python dictionary masquerading as a namespace. as result, the string `10` is returned, and `args` is now a python list of `[10, 10]`.

finally, we evaluate `proc(*[10, 10])`, which is equivalent to evaluating `op.mul(10, 10)`. 