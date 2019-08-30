# `quote`: an execution trace
if `x` is `(quote exp)`, then `x[0]` satisfies the conditional and we execute the following code block:
```python
elif x[0] == 'quote':
	(_, exp) = x  # x is of the form (quote exp)
	return exp
```