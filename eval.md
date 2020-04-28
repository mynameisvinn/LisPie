# `eval`
lets step through an execution trace of `['*', ['+', 2, 3], 3]`. `2` and `3` are python integers, not strings. 

## frame 0: initial call
frame 0: `repl()` calls `eval()` on `x`, which points to `['*', ['+', 2, 3], 3]`. frame 1 is created.

## frame 1: evaluate `x[0]`, which is `"*"`
frame 1: `x` is a `list` that needs to be evaluated by this:
```python
else:
    proc = eval(x[0], env)
    args = [eval(exp, env) for exp in x[1:]]
    return proc(*args)
```
we call `eval()` on `x[0]`, which is `"*"`. we will bind that result (which points to the multiply operation) to the `proc` variable in frame 1. 

## frame 2
calling `eval("*")` returns `op.mul` to frame 1, which will bind that operation to `proc` in frame 1. frame 2 is destroyed.

## frame 1
`args` is the list comprehension containing the results of `eval()` on `x[1:]`, which is `[['+', 2, 3], 3]`:
```python
args = [eval(exp, env) for exp in x[1:]]
```
we call `eval()` on `['+', 2, 3]` which kicks off frame 2. the result of frame 2 will be bound to frame 1's `args` variable.

## frame 2 - frame 2 is responsible for evaluating `(['+', 2, 3])`
`eval(['+', 2, 3])`. we call `eval(x[0])`, which takes us to frame 3. 

## frame 3 - frame 3 evaluates eval("+") and returns `op.add` to frame 2
frame 3 searches for `"+"` in the namespace and returns `op.add` to frame 2. frame 3 exits.

## frame 2
now frame 2 needs to evaluate `args = [eval(exp, env) for exp in x[1:]]`. frame 2's `proc` has been assigned to `op.add` in the previous step.

frame 2's `arg` will be a list containing the results of calling `eval()` on each element of `x[1:]`, or `[eval(2), eval(3)]`. we start with `eval(2)` to create frame 3.

## frame 3
`2` is a constant literal so frame 3's `eval(2)` returns `2` to frame 2. 
```python
elif not isinstance(x, List):
    return x  # if x is not a list, return x
```
## frame 2
frame 2 receives int `2` from frame 3. frame 2's `arg` is now `[2, eval(3)]`. 

we call `eval(3)` and kick off frame 3. 

## frame 3 - eval(3)
frame 3: `eval(3)`. `3` is a constant literal so frame 3 returns python int `3` to frame 2.

## frame 2 - apply `proc` to `*args`
frame 2's `args` is now a python list consisting of `[2, 3]`. 

we can finally move onto the next line of code
```python
return proc(*args)
```
since frame 2's `proc` variable is bound to `op.add`, `proc([2, 3])` returns `5` to frame 1.

## frame 1
frame 1 receives `5` from frame 2. frame 1's `arg` is now the list `[5, eval(3)]`. 

frame 1 calls `eval(3)`.

## frame 2 - evaluate eval(3)
frame 2: `eval(3)`. `3` is a constant literal so frame 2 returns `3` to frame 1. frame 2 is destroyed.

## frame 1 - apply `proc` to `*args`
frame 1 receives `3` from frame 2 and appends it to its `arg`. frame 1's `arg` is now `[5, 3]`. 

in frame 1, we can move onto the next line of code, which is 
```python
proc(*args)
```
since frame 1's `proc` is assigned to `op.mul`, this line of code is equivalent to `op.mul([5, 3])`.

this returns the result `15` to the caller frame 0.