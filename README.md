# lispy
an updated and heavily commented version of [norvig's lispy](http://norvig.com/lispy.html). it should be read in conjunction with [this](http://pythonpracticeprojects.com/lisp.html) and [this](http://www.michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/) and [this](https://maryrosecook.com/blog/post/little-lisp-interpreter).

## usage
to use, do `python lispy.py`.
```python
>>> python lispy.py
>>> (* (+ 2 3) 3)  # returns 15
```

## how does it work?
## creating tokens
tokenize() takes a string of lisp code, puts spaces around every parenthesis and splits on whitespace. for example, it takes something like ((lambda (x) x) "Lisp"), transforms it into ` ( ( lambda ( x ) x ) “Lisp” ) ` and transforms that into ['(', '(', 'lambda', '(', 'x', ')', 'x', ')', '"Lisp"', ')'].

## parsing - an execution trace
parsing converts an expression into something that can be sequentially evaluated. for example, the nested expression `(* (+ 2 3) 3)` is converted into `['*', ['+', 2, 3], 3]`.

lets look at an execution trace.

in frame 0: `tokens` is `(* ( + 2 3 ) 3)`. we encounter `(`, so we create a new list `L0` in frame 0. `tokens` is `* ( + 2 3 ) 3)` because `(` was popped. we enter into the while loop `WL0`. since we do not encounter `(` in `tokens[0]`, we call `read_from_tokens` on `tokens`, which creates frame 1. we will append the result of frame 1 and append it to list `L0`.

in frame 1: the 0th element `*` is popped from `tokens` and, since it is an atom, `*` is returned to frame 0. `tokens` is now `( + 2 3 ) 3)`. frame 1 is destroyed. 

in frame 0: we receive `*` from frame 1 and append it to `L0`. `L0` is now `[*]`. as a reminder, `tokens` is `( + 2 3 ) 3)`. we are still in the while loop `WL0` because we havent satisfied the break condition of `tokens[0] != ')'`. we continue in `WL0` and call `read_from_tokens` on `tokens`, thus creating frame 1. the results of frame 1 will be appended to `L0`. 

in frame 1: we pop `(` from `tokens`, such that `tokens` is now `+ 2 3 ) 3)`. since we encounter `(`, we create a second list `L1` in frame 1. since `tokens[0]` is not `)`, we enter into a second while loop `WL1`. inside `WL1`, we call `read_from_tokens` on `tokens`, thus creating frame 2. the result of frame 2 will be appended to list `L1`.

in frame 2: we pop `+` from `tokens`. `tokens` is now `2 3 ) 3)`. since `+` is an atom, we return `+` to frame 1 and destroy frame 2.

in frame 1: we've received `+` from frame 2 and append it to `L1`. `L1` is now `[+]`. as a reminder, `tokens` is `2 3 ) 3)`. we are still in the while loop `WL1` in frame 1 and, since we havent encountered `)` in `tokens[0]`, we will call `read_from_tokens`, which creates frame 2. the result of frame 2 will be appended to list `L1`.

in frame 2: we pop `2` from `tokens`. `tokens` is now `3 ) 3)`. since `2` is an atom, we return `2` to frame 1 and destroy frame 2. 

in frame 1: we've received `2` from frame 2 and append it to `L1`. `L1` is now `[+, 2]`. as a reminder, `tokens` is `3 ) 3 )`. we are still in the while loop `WL1` in frame 1 and, since `tokens[0]` is not `")"`, we will call `read_from_tokens`, thus creating frame 2. we will take frame 2's result and append it to `L1`.

in frame 2: we pop `3` from `tokens`. `tokens` is now `) 3 )`. since `3` is an atom, we return `3` to frame 1 and destroy frame 2.

in frame 1: we've received `3` from frame 2. we append `3` to `L1`. `L1` is now `[+, 2, 3]`. as a reminder, `tokens` is `) 3 )`. since `tokens[0]` is `)`, we break out of while loop `WL1` in frame 1. we pop out the `)` from `tokens`. tokens is now `3 )`. we return `L1`, which is `[+, 2, 3]`, to frame 0. frame 1 is destroyed.

in frame 0: L0 was `[*]`. we've received `L1` from frame 1 and append to `L0`.  `L0` is now `[*, [+, 2, 3]]`. as a reminder, tokens is `3 )`. `tokens[0]` is not `")"` and therefore we continue the while loop `WH0`. we call `read_from_tokens` on `tokens`, which creates frame 1. frame 1's result will be appended to `L0`.

in frame 1: we pop out `3` from `tokens`. `tokens` is now `)`. since it is an atom, we return `3` to frame 0 and destroy frame 1.

in frame 0: we've received `3` from frame 1. we append `3` to `L0`, which is now `[*, [+, 2, 3], 3]`. `tokens` is now `)`. `tokens[0]` is `)`, so we break out of the while loop `WH0`. we pop `)` from `tokens`. `tokens` is now empty and return `L1`, which is `[*, [+, 2, 3], 3]`, to the calling function (eg parser). 
"""

## evaluation - an execution trace
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

## `define`: an execution trace
lets examine what happens to `(define r 10)`.

the parser returns the ast `['define', 'r', 10]`. it is evaluated by the following code block:
```python
elif x[0] == 'define':
	(_, var, exp) = x
	env[var] = eval(exp, env)
```
the 0th element of the ast `x` - which is `['define', 'r', 10]` - is  `define` and the code block is executed. `x` is unpacked such that `var` is bound to the string `r` and `exp` is bound to the value `10`. since 10 is a constant literal, `eval(10)` returns the value `10`. `env` is the environment, represented as a python dictionary, and is updated such that `env[var] = 10`. 

