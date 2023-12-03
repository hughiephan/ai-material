## Primal and Dual Problem

Primal problem: SVM is a linear classifier $f(x) = w^{\top}x + b$ is formulated as solving an optimization problem over $w$: $\underset{w \in \mathbb{R}^d}{\min} ||w||^2 + C\displaystyle\sum_{i}^N{\max(0, 1 - y_i{f(x_i)})}$ 

Dual problem: $f(x) = \displaystyle\sum_{i}^N\alpha_i{y_i}(x_i^\top{x}) + b$ by solving an optimization problem over $\alpha_i$

## Example

![image](https://github.com/hughiephan/DPL/assets/16631121/4e41598a-3bcd-4abe-9dd8-1750fff3cf52)

## Reference
- https://www.adeveloperdiary.com/data-science/machine-learning/support-vector-machines-for-beginners-duality-problem
- https://machinelearningcoban.com/2017/04/09/smv
- https://becominghuman.ai/support-vector-machine-duality-problem-10442bb2f6cc
- https://www.analytixlabs.co.in/blog/introduction-support-vector-machine-algorithm
- https://www.youtube.com/watch?v=efR1C6CvhmE
- https://www.robots.ox.ac.uk/~az/lectures/ml/lect3.pdf
