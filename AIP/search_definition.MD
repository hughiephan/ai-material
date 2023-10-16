# Progression Search Formal Definition

# Algorithm

## Step 1: 
![image](https://github.com/hughiephan/DPL/assets/16631121/04850b77-ad42-44f6-b5c4-c1f38ff84b01)

```
tnI: 
  precondition: <>
  alpha:
    t1: deliver,
    t2: deliver
```

## Step 2: 
![image](https://github.com/hughiephan/DPL/assets/16631121/0e2580b9-7c37-4cc7-8df4-bd519481fbf4)

```
tn1: 
  precondition: <t1.1, t1.2, t1.3, t1.4>
  alpha:
    t1.1: get-to,
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop,
    t2: deliver
```

## Step 3:
![image](https://github.com/hughiephan/DPL/assets/16631121/044045ee-af5d-4d18-9c34-e3f334872749)

```
tn2: 
  precondition: <t2.1, t2.2, t2.3, t2.4>
  alpha:
    t1: deliver
    t2.1: get-to,
    t2.2: pick-up,
    t2.3: get-to,
    t2.4: drop
```

## Step 4: 
![image](https://github.com/hughiephan/DPL/assets/16631121/e64bd14b-2458-4692-a4ad-90d30b979857)

```
tn1.1: 
  precondition: <t1.1.1, t1.2, t1.3, t1.4>
  alpha:
    t1.1.1: no-op,
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop
    t2: deliver
```

## Step 5:

![image](https://github.com/hughiephan/DPL/assets/16631121/24454efd-c8aa-486d-b8aa-276d56ecf94d)

```
tn1.2:
  precondition: 
    <t1.1, t1.2, t1.3, t1.4>,
    <t2.1, t2.2, t2.3, t2.4>,
  alpha:
    t1.1: get-to,
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop,
    t2.1: get-to,
    t2.2: pick-up,
    t2.3: get-to,
    t2.4: drop
```

# Some description

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
- Fringe will be sorted according to some heuristic. For example: based on the priority (distance between nodes), we can sort the fringe.  
- Test if the popped node is the solution

## Solution Criteria
$$
tn = (T, \prec, \alpha)
$$

The task network $tn$ is a solution if and only if:
- $tn_I \xrightarrow{*} tn$: can be reached by decomposing the initial task network
- $\forall(t) \in T: \alpha(t) \in A$: all task names are primitive
- Sequence of task ??

## References
- 

## Extra
# Questions
- {prec, add, del}: $A \rightarrow 2^L$ ?
- State transition function $\gamma: A \times 2^L \rightarrow 2^L$ ?
- Application of method?
- Applicable action?
- Useful for calculating heuristics?
- What is special about "progression"?

