# Progression Search Formal Definition

# Algorithm

## Task Network Initial: 
![image](https://github.com/hughiephan/DPL/assets/16631121/ce5c1460-e72e-4d8c-860d-db57be4c479c)

```
tnI: 
  precondition: <>
  alpha:
    t1: deliver,
    t2: deliver
```

## Task Network 1: 

Decomposing Task Network 1 into 4 sub-tasks (get-to, pick-up, get-to, drop)

![image](https://github.com/hughiephan/DPL/assets/16631121/6a26cf81-1c6a-4751-8905-f42021c186c8)

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

## Task Network 2:
![image](https://github.com/hughiephan/DPL/assets/16631121/08d95363-504d-4848-aee0-7fa43e5a4a8c)

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

## Task Network 1.1: 

![image](https://github.com/hughiephan/DPL/assets/16631121/08c9e291-7671-4e4b-b464-8fcdff5dab10)

```
tn1.1: 
  precondition: <t1.1.1, t1.2, t1.3, t1.4>
  alpha:
    t1.1.1: no-op,
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop,
    t2: deliver
```

## Task Network 1.2:

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

## Task Network 2.1:

![image](https://github.com/hughiephan/DPL/assets/16631121/bd6762e9-88c6-4b86-a14c-7f7449e52e20)

```
tn2.1:
  precondition: 
    <t2.1.1, t2.2, t2.3, t2.4>,
  alpha:
    t1: deliver,
    t2.1.1: no-op,
    t2.2: pick-up,
    t2.3: get-to,
    t2.4: drop
```

## Task Network 2.2:

![image](https://github.com/hughiephan/DPL/assets/16631121/5f9d5d72-db73-4774-bc5b-7ebc00c36f65)

```
tn2.2:
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

## Task Network 2.2.1:

![image](https://github.com/hughiephan/DPL/assets/16631121/725a38b5-1e23-428d-bfd9-c598ee435385)

```
tn2.2.1:
  precondition: 
    <t1.1, t1.2, t1.3, t1.4>,
    <t2.1.1, t2.2, t2.3, t2.4>,
  alpha:
    t1.1: get-to,
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop,
    t2.1.1: no-op,
    t2.2: pick-up,
    t2.3: get-to,
    t2.4: drop
```

## Task Network 2.2.1.2:

![image](https://github.com/hughiephan/DPL/assets/16631121/f614ee93-9d30-4838-ac9c-f1f7559f0c12)

```
tn2.2.1.2:
  precondition: 
    <t1.1, t1.2, t1.3, t1.4>,
    <t2.2, t2.3, t2.4>,
  alpha:
    t1.1: get-to,
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop,
    t2.2: pick-up,
    t2.3: get-to,
    t2.4: drop
```

```
Goal: <no-op>
```

## Task Network 2.2.1.2.1:

![image](https://github.com/hughiephan/DPL/assets/16631121/8d168e76-e292-4e98-a8bd-04922a1056ab)

```
tn2.2.1.2.1:
  precondition: 
    <t1.1.1, t1.2, t1.3, t1.4>,
    <t2.2, t2.3, t2.4>,
  alpha:
    t1.1.1: no-op,
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop,
    t2.2: pick-up,
    t2.3: get-to,
    t2.4: drop
```

```
Goal: <no-op>
```

## Task Network 2.2.1.2.1.2:

![image](https://github.com/hughiephan/DPL/assets/16631121/936d8b88-843b-497a-91c6-0dfbb35bfb3f)

```
tn2.2.1.2.1.2:
  precondition: 
    <t1.2, t1.3, t1.4>,
    <t2.2, t2.3, t2.4>,
  alpha:
    t1.2: pick-up,
    t1.3: get-to,
    t1.4: drop,
    t2.2: pick-up,
    t2.3: get-to,
    t2.4: drop
```

```
Goal: <no-op, no-op>
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

