In Python, common functional constructs are available as built-in functions (e.g. `map()`, `filter()`, `all()`, `any()`, `sum()`...). Additional higher-order functions are part of the `functools` module, like `reduce()` and `partial()`. The Python implementation of **fold left** is `functools.reduce()`. Python does not implement **fold right**. This article highlights a few of the functional theories behind **fold left** and **fold right**, and from this information, derives one way to implement **fold right** in Python.

<!-- more -->

This article is a [Python](https://www.python.org/) article, but some of the initial code examples are in [Haskell](https://www.haskell.org/). Haskell natively implements both **fold left** and **fold right**. Haskell code, like Python code, reads like pseudo-code and provides executable examples illustrating this article.

# Fold

[Fold](https://en.wikipedia.org/wiki/Fold_(higher-order_function)) regroups a family of [higher-order functions](https://en.wikipedia.org/wiki/Higher-order_function) in [functional programming](https://en.wikipedia.org/wiki/Functional_programming). At a high level, *folding* allows to deconstruct or reduce data. A typical signature for a generic **fold** function is the following:

{% katex(block=true) %}\text{fold}\ f\ z\ xs{% end %}

$$
\text{fold}\ f\ z\ xs
$$


$$
a=1
b=2
$$

[^1]

Where:

* `f` is a higher-order function taking two arguments, an accumulator and an element of the list `xs`. It is applied recursively to each element of `xs`.
* `z` is the initial value of the accumulator and an argument of the function `f`.
* `xs` is a collection.

At a high level, we can picture *fold* as a function that:

1. Iterates over the collection `xs`
2. Applies `f` to the accumulator `z` and a first element of `xs` while returning a new value for `z`
3. Continues to apply function `f` to the new value of `z` for each element of `xs`
4. Returns the final value of `z` after operating on each element of `xs`

As an example, if we wanted to implement a function `total()` that adds all the elements of a list of integers, we would have:

* `total(f, z, xs)` where:
  * `f` is the **addition** operator `(+)`
  * `z` is an initial value for the accumulator, `0`
  * `xs` is a list of integers, e.g. `[1, 2, 3]`

We can then invoke `total()`, as follows (pseudocode):

```
total((+), 0, [1, 2, 3])
```

The nested operations and the result would be:

```
((0 + 1) + 2) + 3 = 6
```

Fold functions come in different kinds, the two main linear ones are `foldl` and `foldr`.

## foldl

`foldl`, for **fold left**, is left associative. Think of `foldl` as *fold from the left* (image courtesy of Wikipedia):

<div style="text-align: center">
<img alt="Left fold transformation" src="https://upload.wikimedia.org/wikipedia/commons/5/5a/Left-fold-transformation.png" />
</div>

{% katex(block=true) %}\text{foldl}\ f\ z\ xs{% end %}

The **fold left** function performs the operations on the elements of the list `xs`, starting from the left. If we substitute `f` with **addition** `(+)`, `z` with value `0`, and `xs` with `[1,2,3]`, the step-by-step operations execute as follows:

{% katex(block=true) %}
\begin{split}
&\text{foldl}\ (+)\ 0\ [1, 2, 3] \\
&\implies \text{foldl}\ (+)\ 1\ [2, 3] \\
&\implies \text{foldl}\ (+)\ 3\ [ 3 ] \\
&\implies \text{foldl}\ (+)\ 6\ [] \\
&\implies 6
\end{split}
{% end %}


$$
\begin{split}
&\text{foldl}\ (+)\ 0\ [1, 2, 3] \\
&\implies \text{foldl}\ (+)\ 1\ [2, 3] \\
&\implies \text{foldl}\ (+)\ 3\ [ 3 ] \\
&\implies \text{foldl}\ (+)\ 6\ [] \\
&\implies 6
\end{split}
$$

The intermediary steps can be reduced into the following one-liner:

{% katex(block=true) %}\text{foldl}\ (+)\ 0\ [1, 2, 3] = ((0 + 1) + 2) + 3{% end %}

We can use the [online REPL](https://tryhaskell.org/) to execute this Haskell code:

```hs
> (((0 + 1) + 2) + 3)
6
```

The operations start from the left by adding the initial accumulator `0` to the first element of the list `1`. The second operation adds the new accumulator `1` to the next element in the list `2`, and so forth until we reach the final result `6`.

We can verify the result of invoking `foldl`:

```hs
> foldl (+) 0 [1,2,3]
6
```

The expression executes `foldl` with the addition `(+)` as a function, an accumulator set to `0` and the list `[1, 2, 3]`. The result is `6`.

## foldr

`foldr`, for **fold right**, is right associative. Think of `foldr` as *fold from the right* (image courtesy of Wikipedia):

<div style="text-align: center">
<img alt="Right fold transformation" src="https://upload.wikimedia.org/wikipedia/commons/3/3e/Right-fold-transformation.png" />
</div>

{% katex(block=true) %}\text{foldr}\ f\ z\ xs{% end %}

The **fold right** function performs the operations on the elements of the list`xs`, starting from the right. Similarly to what we did for `foldl`, substitute `f` with `(+)`, `z` with `0`, and `xs` with `[1,2,3]`. Observe how the addition concretely applies first to the element on the end of the list:

{% katex(block=true) %}
\begin{split}
&\text{foldr}\ (+)\ 0\ [1, 2, 3] \\
&\implies 1 + (\text{foldr}\ (+)\ 0\ [2, 3]) \\
&\implies 1 + (2 + (\text{foldr}\ (+)\ 0\ [ 3 ])) \\
&\implies 1 + (2 + (3 + (\text{foldr}\ (+)\ 0\ []))) \\
&\implies 1 + (2 + (3 + 0)) \\
&\implies 1 + (2 + 3) \\
&\implies 1 + 5 \\
&\implies 6
\end{split}
{% end %}

The steps above can be represented as follows:

{% katex(block=true) %}\text{foldr}\ (+)\ 0\ [1, 2, 3] = 1\ + (2\ + (3\ + 0)){% end %}

We can execute the same expression in the Haskell REPL:

```hs
> 1 + (2 + (3 + 0))
6
```

The following expression is the same operation using the Haskell `foldr` function:

```hs
> foldr (+) 0 [1,2,3]
6
```

The two expressions above are illustrating respectively the manual implementation mimicking the `foldr` order of execution and the invocation of the Haskell `foldr` function.

Because **addition** is [associative](https://en.wikipedia.org/wiki/Associative_property), rearranging the parentheses does not alter the result of the expression: `1 + (2 + (3 + 0))` and `(((0 + 1) + 2) + 3)` are equivalent expressions and evaluate to the same result, `6`. For this reason both `foldl` and `foldr` with the same arguments return the same result if `f` is **addition**. Non-associative functions, like **subtraction** or **division**, would return different results when using `foldl` and `foldr` with the same arguments. For example with **subtraction**, we would observe the following:

```haskell
> foldl (-) 10 [1,2,3]
4
> foldr (-) 10 [1,2,3]
-8
```

Note that both `foldl` and `foldr` take the same arguments, the **subtraction** function `(-)`, the accumulator `10`, and the list `[1,2,3]`. We can translate the `foldl` execution as the following parenthesized subtractions:

```hs
> (((10 - 1) - 2) - 3)
4
```

The `foldr` executes the **subtraction** function to each element of the list from the right-hand side:

```hs
>  1 - (2 - (3 - 10))
-8
```

# Laws of fold

In the book [Introduction to Functional Programming using Haskell](https://www.amazon.com/dp/0134843460/), the authors [Richard Bird](https://www.cs.ox.ac.uk/richard.bird/) and [Philip Wadler](https://homepages.inf.ed.ac.uk/wadler/) wrote a section on the **Laws of fold**. The first three laws are called **duality theorems** and concern the relationship between `foldl` and `foldr`. For simplification and in the context of this article, let's focus on the first and third duality theorems.

## First duality theorem

The first duality theorem states that, for all finite lists `xs`, if `f` is [associative](https://en.wikipedia.org/wiki/Associative_property) and has identity element `e`, then:

{% katex(block=true) %}\text{foldr}\ f\ e\ xs\ =\ \textrm{foldl}\ f\ e\ xs{% end %}

We have already observed the following example using the **addition** as operation and the accumulator `z` set to `0`. Note that `0` is the [identity element](https://en.wikipedia.org/wiki/Identity_element) for **addition** on the set of [Real numbers](https://en.wikipedia.org/wiki/Real_number). We can validate this theory by invoking `foldl` and `foldr` with **addition** and the same collection `[1,2,3]`:

```haskell
> foldl (+) 0 [1,2,3]
6
> foldr (+) 0 [1,2,3]
6
> foldl (+) 0 [1,2,3] == foldr (+) 0 [1,2,3]
True
```

What would be the impact if `z` is not associative? The **third duality theorem** may have an answer.

## Third duality theorem

The **third duality theorem** for **fold** states that, for all finite lists `xs`:

{% katex(block=true) %}\text{foldr}\ f\ e\ xs\ =\ \text{foldl}\ (\text{flip}\ f)\ e\ (\text{reverse}\ xs){% end %}

where:

{% katex(block=true) %}\text{flip}\ f\ x\ y = f\ y\ x{% end %}

Let's use again **subtraction** that is not associative to validate the relationship between `foldl()` and `foldr()`:

```haskell
> foldl (-) 0 [1,2,3]
-6
> foldr (-) 0 [1,2,3]
2
> foldl (flip(-)) 0 (reverse [1,2,3])
2
> foldr (-) 0 [1,2,3] == foldl (flip(-)) 0 (reverse [1,2,3])
True
```

Despite that **subtraction** is not associative, when we apply [flip()](https://zvon.org/other/haskell/Outputprelude/flip_f.html) to the function `(-)` and reverse the order of the argument list `xs`, when we invoke `foldl()`, we obtain the same result as invoking `foldr()` on the same arguments.

Note that `flip()` evaluates the function by flipping the order of the arguments. For example, in Haskell, `(-) 2 1` is equivalent to `2 - 1`, whereas `flip(-) 2 1` is the same as `1 - 2`. We can validate these operations in the online Haskell REPL:

```hs
> (-) 2 1 == 2 - 1
True
> flip(-) 2 1 == 1 - 2
True
```

These two theorems should help crafting a `foldr` function in Python.

# Fold in Python

Despite some past [resistance](https://www.artima.com/weblogs/viewpost.jsp?thread=98196) from [Guido van Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum), Python 3 still has a *Fold* function. We can find it in the `functools` module, and it is named [reduce()](https://docs.python.org/3/library/functools.html#functools.reduce). The function `functools.reduce()` is implemented as a **fold left**.

## foldl in Python

The signature of `functools.reduce()` is `reduce(function, sequence[, initial]) -> value`. The parameter `initial` is optional and corresponds to the accumulator `z` of the Haskell `foldl()` and detailed in the previous section.

As an exercise and to mimic Haskell, a `foldl` function can be written in Python as follows, with a *lambda*:

```python
>>> import functools
>>> import operator
>>> foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)
>>> foldl(operator.sub, 0, [1,2,3])
-6
>>> foldl(operator.add, 'L', ['1','2','3'])
'L123'
```

Note that subtraction and addition are supplied to `foldl()` with respectively [operator.sub](https://docs.python.org/3/library/operator.html#operator.sub) and [operator.add](https://docs.python.org/3/library/operator.html#operator.add). Another option would be to use lambda functions. For example instead of using `operator.add` we could use `lambda x, y: x + y`.

A more formal approach is to implement `foldl` as a function:

```python
import functools
import operator

def foldl(func, acc, xs):
  return functools.reduce(func, xs, acc)

# tests
print(foldl(operator.sub, 0, [1,2,3])) # -6
print(foldl(operator.add, 'L', ['1','2','3'])) # 'L123'
```

So far we have only wrapped `functools.reduce` to look like a `foldl`. Let's see how it could work with `foldr`.

## foldr in Python

Relying on the **third duality theorem** described in the [Laws of fold](/foldl-foldr-python/#third-duality-theorem), `foldr` can be crafted as a *lambda*:

```python
>>> import functools
>>> import operator
>>> foldr = lambda func, acc, xs: functools.reduce(lambda x, y: func(y, x), xs[::-1], acc)
>>> foldr(operator.sub, 0, [1,2,3])
2
>>> foldr(operator.add, 'R', ['1', '2', '3'])
'123R'
```

By applying the two rules of the **third duality theorem**, we respectively:

1. **Flipped** the arguments of `f`: `lambda x, y: func(y, x)`
1. **Reversed** the order of `zs`: `xs[::-1]`

**Notes**: `xs[::-1]` is the Python idiomatic way to return the reverse of a list. Check this [answer from Alex Martelli on stackoverlow](https://stackoverflow.com/a/3705676). The other option, more readable, is to use the built-in [reversed](https://docs.python.org/3.5/library/functions.html#reversed) function. In Python 2, `reduce()` was a built-in function.

Lambdas implemented as above are not generally conducive to good code readability. The following code, although longer, might be more maintainable:

```python

import functools
import operator

def flip(func):
    def newfunc(x, y):
        return func(y, x)
    return newfunc

def foldr(func, acc, xs):
    return functools.reduce(flip(func), reversed(xs), acc)

# test
print(foldr(operator.sub, 0, [1,2,3])) # 2
print(foldr(operator.add, 'R', ['1','2','3'])) # '123R'
```

To flip the arguments of `func`, we use the `flip()` function with a nested function `newfunc()` that returns a function flipping the arguments such that `x` becomes `y` and `y` is `x`.

**Note**: the `flip` function above is inspired from [Raymond Hettinger in a StackOverflow answer](https://stackoverflow.com/a/9850282)

We now have new toy functions in Python, `foldl` and `foldr`.  What can we do with those?

# The Power of Reduce (foldl)

The folding concept opens the doors to build many other functions. It can be done without having to write explicit recursive code or managing loops. For example, `max`, `min`, `sum`, `prod`, `any`, `all`, `map`, `filter` among others, can all be expressed using `fold`.

Here are some examples, using lambdas for conciseness:

```python
>>> import functools
>>> import operator
>>> lmax = lambda xs: functools.reduce(lambda x, y: x if x > y else y, xs)
>>> lmax([1,2,3,4,5])
5
>>> lmin = lambda xs: functools.reduce(lambda x, y: x if x < y else y, xs)
>>> lmin([1,2,3,4,5])
1
>>> lsum = lambda xs, /, start=0: functools.reduce(operator.add, xs, start)
>>> lsum([1,2,3,4,5])
15
>>> lprod = lambda xs, /, start=1: functools.reduce(operator.mul, xs, start)
>>> lprod([1,2,3,4,5])
120
>>> lany = lambda xs: functools.reduce(lambda x, y: x or bool(y), xs, False)
>>> lany([[], [], []])
False
>>> lany(['', 'guido', ''])
True
>>> lall = lambda xs: functools.reduce(lambda x, y: x and bool(y), xs, True)
>>> lall([4,5,6,7])
True
>>> lall([0,1,2])
False
>>> lmap = lambda func, xs: functools.reduce(lambda x, y: x + [func(y)], xs, [])
>>> lmap(lambda x: x + 2, [1,2,3,4,5])
[3, 4, 5, 6, 7]
>>> lfilter = lambda func, xs: functools.reduce(lambda x, y: x + [y] if func(y) else x, xs, [])
>>> lfilter(lambda x: x % 2 == 0, range(1,10))
[2, 4, 6, 8]
```

All the examples have existing and more powerful implementations in Python. They are all [built-in functions](https://docs.python.org/3/library/functions.html), except for [math.prod()](https://docs.python.org/3/library/math.html#math.prod) in  the `math` module since Python 3.8. All of the functions above are relying on `reduce` (`foldl`) and none are taking advantage of `foldr`.

# More Examples with foldr and foldl

```lisp
> (foldr cons '(4) '(1 2 3))
'(1 2 3 4)

> (cons '1 (cons '2 (cons '3 '(4))))
'(1 2 3 4)

> (foldl cons '(4) '(1 2 3))
'(3 2 1 4)

> (cons '3 (cons '2 (cons '1 '(4))))
'(3 2 1 4)
```

# Example with Foldr

Here is a  scenario that demonstrates a possible usage of `foldl` and `foldr` in Python. Peter Drake presents this construct in his [Lambdas and folds Youtube video](https://youtu.be/1IjBT9TSTyQ). Imagine that, given a list, we need to identify the last and/or the first element that satisfies a certain predicate. This could be written as follows:

```python
import functools

def foldl(func, acc, xs):
  return functools.reduce(func, xs, acc)

def flip(func):
    def newfunc(x, y):
        return func(y, x)
    return newfunc

def foldr(func, acc, xs):
    return functools.reduce(flip(func), reversed(xs), acc)

def first(func, acc, xs):
    return foldr(lambda x, y: x if func(x) else y, acc, xs)

def last(func, acc, xs):
    return foldl(lambda x, y: y if func(y) else x, acc, xs)

print(last(lambda x: x<8, None, [1,2,3,4,5,6,7,8,9]))   # => 7
print(first(lambda x: x>3, None, [1,2,3,4,5,6,7,8,9]))  # => 4
print(first(lambda x: x>20, None, [1,2,3,4,5,6,7,8,9])) # => None
```

`first` and `last` don't require any loop or explicit recursion. `first` uses `foldr` taking advantage of the *right folding* whereas `last` relies on `foldl`.

## How does first work?

```python

predicate (example: element less than 8)

z = None
xs = [1,2,3,4,5,6,7,8,9]
foldl:
* f =  lambda x: x<8
* z = None
* xs = [1,2,3,4,5,6,7,8,9]

first element (x: None, y: 1)
lambda x, y: x if x < 8 or z
now z = x = 1
second element z = 1
x = 2
now z = x = 2
...
x = 8
now z = z = 7
x = 9
now z = z = 7
```


## How does last work?

```python

predicate (example: element greater than 8)

z = None
xs = [1,2,3,4,5,6,7,8,9]
foldf:
* f =  lambda x: x>8
* z = None
* xs = [1,2,3,4,5,6,7,8,9]

first element (x: None, y: 1)
lambda x, y: x if x < 8 or z
now z = x = 1
second element z = 1
x = 2
now z = x = 2
...
x = 8
now z = z = 7
x = 9
now z = z = 7
```



# Conclusion

In this era of the rediscovery of functional programming, there is much more to explore and to apply to languages that are not inherently functional. Arguably, from a pragmatic perspective, there may be little we need that is not already provided in the current versions of Python and that would require some sophisticated folding mechanisms. Furthermore, other higher-order functions flagships along with `fold`, like `map` and `filter`, can be expressed in Python with elegant *list comprehensions* and *generator expressions*, but this should be the subject of a different article.

# Updates

* **03/12/2021**:
  * Removed Python 2 references

* **08/28/2016**
  * Initial publication of this article.


[^1]: THIS SUCKS.
