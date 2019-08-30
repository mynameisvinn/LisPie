# how does it work?
## `eval`: an execution trace
frame 0: `repl()` calls `eval()` on `x`, which points to `['*', ['+', 2, 3], 3]`. frame 1 is created.

frame 1: `x` is a `list` so we call `eval()` on `x[0]`, which corresponds to `"*"` and bind that result to `proc` variable. the corresponding line is:
```python
proc = eval(x[0], env)
```

frame 2: `eval("*")`. `"*"` is a symbol so frame 2 returns the corresponding operator "multiply" to frame 1. (through the `env` namespace, which contains methods.) the corresponding line of code is:
```python
if isinstance(x, Symbol):
	return env.find(x)[x]
```

frame 1: the variable `proc` is now bound to multiply. 

frame 1: we have the variable `args`, which is a list containing the results of calling `eval()` on `x[1:]`, which is `[['+', 2, 3], 3]`. (remember `x[0]` points to `"*"`.) the corresponding line of code is:
```python
args = [eval(exp, env) for exp in x[1:]]
```
in general, every list in lisp is of the form `(operator argument argument)`.

frame 1: we call `eval()` on `['+', 2, 3]` to create frame 2. its result will be appended to frame 1's `args`. we will call `eval()` on 3 afterwards.

frame 2: `eval(['+', 2, 3])`. since `x` is a list, we call `eval()` on `x[0]`, which is "+", and bind that result to frame 2's `proc` variable. frame 2's `proc` is the addition method.

frame 2: we now have the variable `args` in frame 2. it is distinct from frame 1's `arg`. frame 2's `arg` will be a single list containing the results of calling `eval()` on `x[1:]`, which is `[2, 3]`. (we've combined two objects into a single object, a list consisting of two objects.) we call `eval()` on `2` to create frame 3. (we will call `eval()` on `3` later.)

frame 3: `eval(2)`. `2` is a constant literal so frame 3 returns `2` to frame 2. the corresponding line of code is:
```python
elif not isinstance(x, List):
	return x
```

frame 2: frame 2's `arg` list is now `[2]`. we call `eval()` on `3`, which launches frame 3. 

frame 3: `eval(3)`. `3` is a constant literal so frame 3 returns `3` to frame 2.

frame 2: frame 2's `args` is now a list consisting of `[2, 3]`. 

frame 2: frame 2 evaluates `proc([2, 3])`. since frame 2's `proc` is addition, `proc([2, 3])` returns `5` to frame 1.

frame 1: frame 1 receives `5` from frame 2. this is collected by frame 1's `arg`, which is the list `[5, eval(3)]`. frame 1 calls `eval(3)`.

frame 2: `eval(3)`. `3` is a constant literal so frame 2 returns `3` to frame 1. frame 2 is destroyed.

frame 1: frame 1 receives `3` from frame 2, and appends it to frame 1's `arg`, which is now `[5, 3]`. 

frame 1: we want to do `proc([5, 3])`. frame 1's `proc` is bound to a multiply operation. `multiply([5, 3])` returns `15` to frame 0.