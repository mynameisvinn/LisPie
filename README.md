# lispy
an updated and heavily commented version of [norvig's lispy](http://norvig.com/lispy.html). it should be read in conjunction with [this](http://pythonpracticeprojects.com/lisp.html) and [this](http://www.michaelnielsen.org/ddi/lisp-as-the-maxwells-equations-of-software/).

## usage
to use, do `python lispy.py`.
```python
>>> (* (+ 2 3) 3)  # returns 15
```

## how does it work?
### parsing
parsing converts an expression into something that can be sequentially evaluated. for example, the nested expression `(* (+ 2 3) 3)` is converted into `['*', ['+', 2, 3], 3]` for evaluation.