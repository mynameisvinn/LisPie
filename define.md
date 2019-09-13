# what happens when we use `define`?
## `define` inserts a new key:value/symbol:value pair in the environment
lets examine what happens to `(define r 10)`.

the ast `['define', 'r', 10]` triggers the following block. (notice that `10` is a python integer, not a string. this conversion is handled by the `atom` function.)
```python
elif x[0] == 'define':
	(_, var, exp) = x
	env[var] = eval(exp, env)
```
`x` is unpacked: `var` is bound to `r` and `exp` is bound to `10`. 

`eval(10)` returns the value `10` since 10 is a constant literal. finally, a new symbol is created in the current environment (either inner or outer) and then paired with the value 10.

## how do we reference symbols, after it's been defined?
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