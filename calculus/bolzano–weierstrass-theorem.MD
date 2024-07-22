# Bolzano–Weierstrass Theorem

## Theorem
Every bounded sequence of real numbers has a convergent subsequence

## Proof

Let $(s_n)_{n \in \mathbb{N}}$ be a real sequence of real numbers with $|s_n| \leq L$  

Step 1 (Search Procedure):

- Set $a_0 = -L$ and $b_0 = L$. Then $|b_0 - a_0| = 2L$

- Divide the interval $[a_0, b_0]$ into two subintervals. Due to the pigeonhole principle, if we have an infinite number of items and we distribute them into a finite number of containers, at least one container must hold infinitely many items. So there must be at least one of these two subintervals that contain infinitely many members, called $s_n's$. Pick one such subinterval and call it $[a_1, b_1]$ with $|b_1 - a_1| = \frac{1}{2}| = L$, and that $a_1 \in \{a_0, a_0 + \frac{b_0 - a_0}{2}\}$. So $a_1 \geq a_0$. There are many infinitely many $s_n's$ in $[a_1, b_1]$. Select one, say $s_{i_1}$

-  Divide the interval $[a_1, b_1]$ into two halves. At least one half must contain infinitely many $s_n$'s. Pick one such half and call it $[a_2, b_2]$. Note that $|b_2 - a_2| = \frac{1}{2}|b_1 - a_1| = \frac{1}{2}L$, and that $a_2 \in \{a_1, a_1 + \frac{b_1 - a_1}{2}\}$. So $a_2 \geq a_1$. There are infinitely many $s_n$'s in $[a_2, b_2]$. Select one with $n > i_1$, say $s_{i_2}$.

- Continue until we get the following:

![image](https://github.com/user-attachments/assets/8f67b5eb-e17a-4356-92da-ef93ab4083ed)

## Reference
- https://personal.math.ubc.ca/~feldman/m320/bolzano.pdf
- https://en.wikipedia.org/wiki/Bolzano%E2%80%93Weierstrass_theorem
