# Bolzano–Weierstrass Theorem

## Theorem
Every bounded sequence of real numbers has a convergent subsequence

## Proof

Let $(s_n)_{n \in \mathbb{N}}$ be a real sequence of real numbers with $|s_n| \leq L$  

Step 1: Search Procedure

- Set $a_0 = -L$ and $b_0 = L$. Then $|b_0 - a_0| = 2L$

- Divide the interval $[a_0, b_0]$ into two subintervals. Due to the pigeonhole principle, if we have an infinite number of items and we distribute them into a finite number of containers, at least one container must hold infinitely many items. So there must be at least one of these two subintervals that contain infinitely many members, called $s_n's$. Pick one such subinterval and call it $[a_1, b_1]$ with $|b_1 - a_1| = \frac{1}{2}| = L$, and that $a_1 \in \{a_0, a_0 + \frac{b_0 - a_0}{2}\}$. So $a_1 \geq a_0$. There are many infinitely many $s_n's$ in $[a_1, b_1]$. Select one, say $s_{i_1}$

-  Divide the interval $[a_1, b_1]$ into two halves. At least one half must contain infinitely many $s_n$'s. Pick one such half and call it $[a_2, b_2]$. Note that $|b_2 - a_2| = \frac{1}{2}|b_1 - a_1| = \frac{1}{2}L$, and that $a_2 \in \{a_1, a_1 + \frac{b_1 - a_1}{2}\}$. So $a_2 \geq a_1$. There are infinitely many $s_n$'s in $[a_2, b_2]$. Select one with $n > i_1$, say $s_{i_2}$.

- Continue until we get the following:

![image](https://github.com/user-attachments/assets/8f67b5eb-e17a-4356-92da-ef93ab4083ed)

Step 2: Guess the Limit

The sequence $a_1, a_2, a_3, \ldots$ is monotone increasing and bounded above by $b_0 = L$. So it converges. Call the limit $s$.

Step 3: Prove that $\lim_{n \to \infty} s_n = s$: 

Let $\epsilon > 0$. Since $(a_n)_{n \in \mathbb{N}}$ converges to $s$

$$
\exists N_1 \in \mathbb{N} \text{ such that } |a_n - s| < \frac{\epsilon}{2} \text{ whenever } n \geq N_1
$$

Since $s_{i_n}$ lies in the interval $[a_n, b_n]$, and the length of the interval $[a_n, b_n]$ is $\frac{L}{2^n}$, the distance from $s_{i_n}$ to $a_n$ is at most $\frac{L}{2^{n-1}}$, which converges to zero as $n \to \infty$

$$
\exists N_2 \in \mathbb{N} \text{ such that } |s_{i_n} - a_n| < \frac{\epsilon}{2} \text{ whenever } n \geq N_2
$$

Choose $N = \max \{N_1, N_2\}$. Then

$$
n \geq N \implies |s_{i_n} - s| \leq |s_{i_n} - a_n| + |a_n - s| < \epsilon
$$

## Application

https://www.sangakoo.com/en/unit/theorem-of-bolzano

## Reference
- https://personal.math.ubc.ca/~feldman/m320/bolzano.pdf
- https://en.wikipedia.org/wiki/Bolzano%E2%80%93Weierstrass_theorem
