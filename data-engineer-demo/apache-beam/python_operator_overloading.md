# Python Operator Overloading: `|` and `>>`

How Python operator overloading (`__or__`, `__rshift__`) powers pipeline DSLs like Apache Beam:

```python
p | Step1 | Step2 >> sink
```

## Magic methods

- `a | b` calls `a.__or__(b)` — `a` is `self`, `b` is the argument.
- `a >> b` calls `a.__rshift__(b)`.
- Return a **new object** from `__or__` so you can chain: `a | b | c`.
- Reverse / in-place variants: `__ror__` (used when the left operand lacks `__or__`), `__ior__` (`|=`).

## Why it chains

`__or__` returns a new instance of the class, so the next `|` triggers `__or__` again on that result.

## Minimal example

```python
class DataPipeline:
    def __init__(self, data=None):
        if data is None:
            self.data = []
        elif isinstance(data, list):
            self.data = data
        else:
            self.data = [data]

    def __or__(self, operation):        # a | fn
        return DataPipeline([operation(x) for x in self.data])

    def __rshift__(self, destination):  # a >> list
        destination.extend(self.data)
        return destination


sink = []
DataPipeline([1, 2, 3]) | (lambda x: x * 2) | (lambda x: x + 10) >> sink
# sink == [12, 14, 16]
```

## Step-by-step trace

For `pipeline | double`:

1. Python sees `pipeline | double`.
2. Translates to `pipeline.__or__(double)` — `self` = `pipeline`, `operation` = `double`.
3. Runs `[double(x) for x in self.data]`.
4. Returns a new `DataPipeline` holding the result, ready for the next `|`.

## Precedence gotcha

`|` binds tighter than `>>` in Python, so:

```python
p | f >> sink   # parses as  (p | f) >> sink
```

Same reason Beam's `p | step >> label` works.
