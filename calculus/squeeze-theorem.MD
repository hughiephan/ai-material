# Squueze Theorem

The Squeeze Theorem can help prove that an algorithm converges to a particular solution. When studying the convergence of gradient descent, the Squeeze Theorem can be used to show that the updates to the weights get arbitrarily close to the optimal weights, assuming the step sizes are appropriately chosen and the loss function is well-behaved

## Inferior and Superior 

TBD

## Proof of Squeeze Theorem using Inferior and Superior Limit

Given $g(x) \leq f(x) \leq h(x)$ for $x$ near $a$, with:
- $\limsup_{x \to a} f(x)$: The smallest value that $f(x)$ can oscillate up to as $x$ approaches $a$, 
- $\liminf_{x \to a} f(x)$: The largest value that $f(x)$ can oscillate down to as $x$ approaches $a$

$L = \lim_{x \to a} g(x) \leq \liminf_{x \to a} f(x) \leq \limsup_{x \to a} f(x) \leq \lim_{x \to a} h(x) = L$

Since the outer limits $\lim_{x \to a} g(x)$ and $\lim_{x \to a} h(x)$ both equal $L$, and the inequalities sandwich $\liminf_{x \to a} f(x)$ and $\limsup_{x \to a} f(x)$ between $L$, we conclude: $\liminf_{x \to a} f(x) = \limsup_{x \to a} f(x) = L$. Conclusion:  $\lim_{x \to a} f(x) = L$

## Reference
- https://en.wikipedia.org/wiki/Squeeze_theorem
- https://www.math.clemson.edu/~petersj/Courses/M453/Lectures/L11-LiminfLimsupSeq.pdf
