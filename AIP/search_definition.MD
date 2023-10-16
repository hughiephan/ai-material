# Progression Search Formal Definition

In AI search algorithms, the state (or search) space is usually represented as a graph, where nodes are states and the edges are the connections (or actions) between the corresponding states. 

# Unconstrained Task
A task id $t$ is unconstrained in a task network $(T, \prec, \alpha)$ if and only if there is no task $\acute{t} \in T$ such that $(\acute{t}, t) \in \prec)$

Explanation: 
- Meaning that there is no precondition between that task and another task.

# Solution
$$
n = (s, (T, \prec, \alpha), \pi)
$4

The node will be a solution if and only if:
- Task network is empty $T = \emptyset$
- State is goal state (s \supseteq g)

# Algorithm 1


$fringe \gets { \{(s_0, tn_I, \epsilon) \} }$

While $fringe \neq \emptyset$ Do

&nbsp;&nbsp; $n \xleftarrow{} fringe.pop()$

&nbsp;&nbsp; If $n.isgoal$ then return $n$ 


With:
- $s_0$: initial state
- $tn_I$: initial task network
- $\epsilon$: an empty sequence

Explanation:
- Test if the popped node is the solution

## Extra
# Questions

