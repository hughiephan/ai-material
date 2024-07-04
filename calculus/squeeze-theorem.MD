
Constructing the Inequality

Given $g(x) \leq f(x) \leq h(x)$ for $x$ near $a$, with:
- $\limsup_{x \to a} f(x)$: The smallest value that $f(x)$ can oscillate up to as $x$ approaches $a$, 
- and $\liminf_{x \to a} f(x)$: The largest value that $f(x)$ can oscillate down to as $x$ approaches $a$


$L = \lim_{x \to a} g(x) \leq \liminf_{x \to a} f(x) \leq \limsup_{x \to a} f(x) \leq \lim_{x \to a} h(x) = L$

Since the outer limits $\lim_{x \to a} g(x)$ and $\lim_{x \to a} h(x)$ both equal $L$, and the inequalities sandwich $\liminf_{x \to a} f(x)$ and $\limsup_{x \to a} f(x)$ between $L$, we conclude: $\liminf_{x \to a} f(x) = \limsup_{x \to a} f(x) = L$

Conclusion:  $\lim_{x \to a} f(x) = L$

## Reference
- https://en.wikipedia.org/wiki/Squeeze_theorem
