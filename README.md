# lispy
an updated and heavily commented version of [norvig's lispy](http://norvig.com/lispy.html). it should be read in conjunction with [this](http://pythonpracticeprojects.com/lisp.html) and [this](http://www.michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/).

## usage
to use, do `python lispy.py`.
```python
>>> (* (+ 2 3) 3)  # returns 15
```

## how does it work?
## tracing through parsing
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