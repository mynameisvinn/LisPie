# what happens when we use `define`?
## `define` inserts a new key:value pair in the namespace
lets examine what happens to `(define r 10)`.

the parser returns the ast `['define', 'r', 10]`. it is evaluated by the following code block:
```python
elif x[0] == 'define':
	(_, var, exp) = x
	env[var] = eval(exp, env)
```
the 0th element of the ast `x` - which is `['define', 'r', 10]` - is  `define` and the code block is executed. (notice that `10` is a python integer, not a string. this conversion is handled by the `atom` function.)

`x` is unpacked such that `var` is bound to the string `r` and `exp` is bound to the value `10`. since 10 is a constant literal, `eval(10)` returns the value `10`. `env` is the environment, represented as a python dictionary, and is updated such that `env[var] = 10`. 

## how do we reference symbols, following `define`?
we previously defined `r`. what happens if we evaluate `(* r r)`?. 

this expression is a regular list expression (as opposed to a special form) and therefore flows through the `else` block:
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
`proc` is bound to `op_mul`. `args` is equal to `[eval(r), eval(r)]`. `r` is a symbol, which means we use it as a key to fetch its corresponding value:
```python
if isinstance(x, Symbol):
    return env.find(x)[x]
```
since `r` is mapped to `10` in the global namespace in the previous step, `eval(r)` returns `10`. ultimately, `args` is `[10, 10]`. 

finally, we evaluate `proc(*[10, 10])`. this is the equivalent to evaluating `op.mul(10, 10)`, thus completing the evaluation of `(* r r)`.