## Primal and Dual formulation

![image](https://github.com/hughiephan/DPL/assets/16631121/170b9616-1516-4d9d-9c17-6b5726144f32)

SVM can be a classifier with one of the two form:

- Primal formulation: $f(x) = w^{\top}x + b$ is formulated as solving an optimization problem over $w$
- Dual formulation: $f(x) = \displaystyle\sum_{i}^N\alpha_i{y_i}(x_i^\top{x}) + b$ by solving an optimization problem over $\alpha_i$

## Representer Theorem

Proof: https://en.wikipedia.org/wiki/Representer_theorem

The theorem states that the solution $w$ can always be written as a linear combination of the training data $w = \displaystyle\sum_{j=1}^N{\alpha_j{y_j}x_j}$. With $(x_1,y_1),...,(x_n,y_n) \in \chi \times \mathbb{R}$ is the training samples, with $\chi$ is a non-empty set

## Primal and Dual Problem

$N$ is the number of training points, and $d$ is the dimension of feature vector x.

Primal Problem: $\underset{w \in \mathbb{R}^d}{\min} ||w||^2 + C\displaystyle\sum_{i}^N{\max(0, 1 - y_i{f(x_i)})}$, for $w \in \mathbb{R}^d$

Dual Problem: $\underset{\alpha_i \geq 0}{\max}\displaystyle\sum_{i}\alpha_i - \frac{1}{2}\displaystyle\sum_{jk}\alpha_j\alpha_k{y_j}{y_k}(x_j^\top x_k)$, for $\alpha \in \mathbb{R}^N$

The dual form has an advantage because it only involves $x_j^\top x_k$


# Transformed Feature Space

![image](https://github.com/hughiephan/DPL/assets/16631121/5c356a0a-f058-416f-93af-5d516de93e33)

Then the Primal Classifier becomes: $f(x) = w^\top\phi(x) + b$

And the Dual Classifier becomes: $f(x) = \displaystyle\sum_{i}^N\alpha_i{y_i}(\phi(x_i)^\top\phi{x}) + b$

![image](https://github.com/hughiephan/DPL/assets/16631121/34981040-6d49-42d9-88fb-0ee0e478ab13)

Dual Classifier can be learnt and applied without explicitly computing $\phi(x)$ (also called Kernel trick)

## Example

![image](https://github.com/hughiephan/DPL/assets/16631121/4e41598a-3bcd-4abe-9dd8-1750fff3cf52)

## Reference
- https://www.adeveloperdiary.com/data-science/machine-learning/support-vector-machines-for-beginners-duality-problem
- https://machinelearningcoban.com/2017/04/09/smv
- https://becominghuman.ai/support-vector-machine-duality-problem-10442bb2f6cc
- https://www.analytixlabs.co.in/blog/introduction-support-vector-machine-algorithm
- https://www.youtube.com/watch?v=efR1C6CvhmE
- https://www.robots.ox.ac.uk/~az/lectures/ml/lect3.pdf
- https://stats.stackexchange.com/questions/544959/what-does-representer-theorem-in-machine-learning-tells-us
