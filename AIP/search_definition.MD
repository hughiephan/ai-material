# Progression Search Formal Definition

In AI search algorithms, the state (or search) space is usually represented as a graph, where nodes are states and the edges are the connections (or actions) between the corresponding states. This approach combines task decomposition with state-based goals.

# Unconstrained Task
A task id $t$ is unconstrained in a task network $(T, \prec, \alpha)$ if and only if there is no task $\acute{t} \in T$ such that $(\acute{t}, t) \in \prec)$

Explanation: 
- Meaning that there is no precondition between that task and another task.

# Solution
$$
n = (s, (T, \prec, \alpha), \pi)
$$

The node will be a solution if and only if:
- Task network is empty $T = \emptyset$
- State is goal state $s \supseteq g$

With:
- $\pi$: generated plan

# Algorithm 1


$fringe \gets { \{(s_0, tn_I, \epsilon) \} }$

While $fringe \neq \emptyset$ Do

&nbsp;&nbsp; $n \xleftarrow{} fringe.pop()$

&nbsp;&nbsp; If $n.isgoal$ then return $n$ 


Fringe consists of:
- $s_0$: initial state
- $tn_I$: initial task network
- $\epsilon$: an empty sequence

A search node is a tuple that includes the 
- current state
- task network
- elements of the problem definition that change during search

Explanation:
- Add first, add a search node into the fringe.
- Test if the popped node is the solution

## Solution Criteria
$$
tn = (T, \prec, \alpha)
$$

The task network $tn$ is a solution if and only if:
- $tn_I \xrightarrow{*} tn$: can be reached by decomposing the initial task network
- $\forall(t) \in T: \alpha(t) \in A$: all task names are primitive
- Sequence of task ??


## Extra
# Questions
- {prec, add, del}: $A \rightarrow 2^L$ ?
- State transition function $\gamma: A \times 2^L \rightarrow 2^L$ ?
- Application of method ?
- Applicable action ?
