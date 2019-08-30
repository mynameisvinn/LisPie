# `conditional` expression: an execution trace
a conditional has the following syntax: `(if test conseq alt)`. in our interpreter, we evaluate test; if true, evaluate and return conseq; otherwise alt. for example, `(if (> 10 20) 1 0) => 0`.

the code `(if (> 10 20) 1 0) => 0` is parsed into an ast `['if', ['>', 10, 20], 1, 0]`. since `x[0] == 'if'`, we execute the following code block:
```python
elif x[0] == 'if':
	(_, test, conseq, alt) = x
	exp = (conseq if eval(test, env) else alt)
	return eval(exp, env)
```
we extract `test`, `conseq`, and `alt` from `x`. `test` is `['>', 10, 20]` and is evaluated as `op.gt(10, 20)`. in this case, `exp` is assigned to `alt`. finally `eval(alt)` which returns `alt` (in this case, this is equivalent to `eval(0))`, which returns `0`.) 