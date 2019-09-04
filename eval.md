# `eval`
lets go through an execution trace of `['*', ['+', 2, 3], 3]`. remember, 2 and 3 are represented as python integers. in general, every list in lisp is of the form `(operator argument argument)`.

frame 0: `repl()` calls `eval()` on `x`, which points to `['*', ['+', 2, 3], 3]`. frame 1 is created.

frame 1: `x` is a `list` that needs to be evaluated by this:
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
we call `eval()` on `x[0]`, which is `"*"`. we will bind that result to `proc` variable. 

frame 2: calling `eval("*")` creates frame 2. according to the global environment, `"*"` representing `op.mul`. frame 2 returns `op.mul` to frame 1, which is bound to `proc`.

frame 1: `args` is the list comprehension containing the results of `eval()` on `x[1:]`, which is `[['+', 2, 3], 3]`:
```python
args = [eval(exp, env) for exp in x[1:]]
```

frame 1: we call `eval()` on `['+', 2, 3]` to create frame 2. its result will be appended to frame 1's `args`. (we will execute `eval(3)` afterwards.)

frame 2: `eval(['+', 2, 3])`. we call `eval(x[0])`, which takes us to frame 3. 

frame 3: frame 3 searches for `"+"` in the namespace and returns `op.add` to frame 2. frame 3 exits.

frame 2: frame 2's `proc` is bound to `op.add`. we now have the variable `args` in frame 2. (it is different from frame 1's `arg`.) frame 2's `arg` will be a single list containing the results of calling `eval()` on each element of `x[1:]`, or `[eval(2), eval(3)]`. we start with `eval(2)` to create frame 3. (we will call `eval()` on `3` later.)

frame 3: `eval(2)`. `2` is a constant literal so frame 3 returns `2` to frame 2. 
```python
elif not isinstance(x, List):
	return x
```

frame 2: frame 2's `arg` is currently `[2]`. we call `eval(3)` and kick off frame 3. 

frame 3: `eval(3)`. `3` is a constant literal so frame 3 returns `3` to frame 2.

frame 2: frame 2's `args` is now a list consisting of `[2, 3]`. 

frame 2: frame 2 evaluates `proc([2, 3])`. 
```python
return proc(*args)
```
since frame 2's `proc` is `op.add`, `proc([2, 3])` returns `5` to frame 1.

frame 1: frame 1 receives `5` from frame 2. this is collected by frame 1's `arg`, which is the list `[5, eval(3)]`. frame 1 calls `eval(3)`.

frame 2: `eval(3)`. `3` is a constant literal so frame 2 returns `3` to frame 1. frame 2 is destroyed.

frame 1: frame 1 receives `3` and appends it to frame 1's `arg`, which is now `[5, 3]`. 

frame 1: we want to do `proc([5, 3])`. frame 1's `proc` is `op.mul`. `op.mul([5, 3])` returns `15` to frame 0.