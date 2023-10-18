# Progression Search Formal Definition

# Some description

In AI search algorithms, the state (or search) space is usually represented as a graph, where nodes are states and the edges are the connections (or actions) between the corresponding states. This approach combines task decomposition with state-based goals.

# Unconstrained Task


![image](https://github.com/hughiephan/DPL/assets/16631121/bdea9ce9-4384-4960-917f-b5c853cefed6)

A task id $t$ is unconstrained in a task network $(T, \prec, \alpha)$ if and only if there is no task $\acute{t} \in T$ such that $(\acute{t}, t) \in \prec)$

Explanation: 
- Unconstrained tasks are tasks that have no predecessors in the network.

# Solution
$$
n = (s, (T, \prec, \alpha), \pi)
$$

The node will be a solution if and only if:
- Task network is empty $T = \emptyset$
- State is goal state $s \supseteq g$

With:
- $\pi$: generated plan

# Standard Progression Search Algorithm

01. $fringe \gets { \{(s_0, tn_I, \epsilon) \} }$

02. While $fringe \neq \emptyset$ Do

03. &nbsp;&nbsp; $n \xleftarrow{} fringe.pop()$

04. &nbsp;&nbsp; If $n.isgoal$ then return $n$ 

05. &nbsp;&nbsp; $U  \xleftarrow[]{} n.unconstrainedNodes$

06. &nbsp;&nbsp; For $t \in U$ do

07. &nbsp;&nbsp;&nbsp;&nbsp; If $isPrimitive(t)$ then

08. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; If $isApplicable(t)$ then

09. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $\acute{n} \xleftarrow[]{} n.apply(t)$

10. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $fringe.add(\acute{n})$

11. &nbsp;&nbsp;&nbsp;&nbsp; else

12. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; For $m \in t.methods$ do

13. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $\acute{n} \xleftarrow[]{} n.decompose(t,m)$

14. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $fringe.add(\acute{n})$

15. Return $unsolvable$

## Fringe

![image](https://github.com/hughiephan/DPL/assets/16631121/3036954b-962f-40e3-91cb-6267e6526e3e)

The fringe consists of:
- $s_0$: initial state
- $tn_I$: initial task network
- $\epsilon$: an empty sequence

In Fringe search, the fringe is like the frontier.

Example:
```
fringe:
  state: s0
  task_network:
    tnI: 
      precondition: <>
      alpha:
        t1: deliver(P1,B),
        t2: deliver(P2,D)
  element: ??
```

## Search Node 

![image](https://github.com/hughiephan/DPL/assets/16631121/fb946cf3-395d-4514-b149-ca778c07569c)

- current state
- task network
- elements of the problem definition that change during search

Explanation:
- Add first, add a search node into the fringe.
- Fringe will be sorted according to some heuristic. For example: based on the priority (distance between nodes), we can sort the fringe.  
- Test if the popped node is the solution

## Decomposition
Explanation:
- There is similarity between decomposition, in previous paper it is used to decompose task network. It this paper it is used to decompose a new search node.

## Progression

$$
\acute{n} = (\acute{s}, (\acute{T}, \acute{\prec}, \acute{\alpha}), \acute{\pi}
$$ 

- $n = (s, T, \prec, \alpha, \pi)$ : a search node
- $t \in T$: unconstrained task
- $\acute{n}$: search node from progressing $t$
- $\acute{T} = T$ \ { $t$ }
- $\acute{\prec} = \prec$ \ { $(t,\acute{t}) | \acute{t} \in T$ }
- $\acute{\alpha} = \alpha$ \ { $t \mapsto \alpha(t)$ }  


Explanation:
- List of new tasks should remove the unconstrained task we just processed.
- The new precondition remove the precondition relationship between the unconstrained task 
- The $alpha$ mapping of the unconstrained task will be removed also.

## Solution Criteria
$$
tn = (T, \prec, \alpha)
$$

The task network $tn$ is a solution if and only if:
- $tn_I \xrightarrow{*} tn$: can be reached by decomposing the initial task network
- $\forall(t) \in T: \alpha(t) \in A$: all task names are primitive
- Sequence of task ??

## References
- Höller, Daniel & Bercher, Pascal & Behnke, Gregor & Biundo, Susanne. (2020). HTN Planning as Heuristic Progression Search. Journal of Artificial Intelligence Research. 67. 835-880. 10.1613/jair.1.11282. 

# Extra
## Questions
- {prec, add, del}: $A \rightarrow 2^L$ ?
- State transition function $\gamma: A \times 2^L \rightarrow 2^L$ ?
- Application of method?
- Applicable action?
- Useful for calculating heuristics?
- What is special about "progression"?
