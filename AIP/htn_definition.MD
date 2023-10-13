# Formal Definition of Hierarchical Task Network

## Decomposition Tree

![image](https://github.com/hughiephan/DPL/assets/16631121/639dc0bc-e1e5-4fde-ba81-7d9d207dcba2)

## Task Network

$$
tn=(T, \prec, \alpha)
$$

A task network $tn$ consists of:
- $T$: a finite and non-empty set of tasks
- $\prec$: a strict partial order on $T$(irreflexive, asymetric, and transitive). We can just call it as a set of ordering constraints.
- $\alpha$: a function to map task id to task name 

Explanation:
- It makes sense that the constraints / preconditions are transitive. A precondition should only happen after it's previous precondition is satisfied. Irreflexivity mean that no element is related to itself, I think we have this to avoid loop. And asymmetric is the direct result of both irreflexive and transitive.
- We need task ID because when we do recursive, the task name will be duplicated so we need the unique IDs for tasks. The $\prec$ defines the relationship between two tasks so it makes sense that $prec$ is a subset of $T \times T$

Example: 
```
task_network: 
  tasks: 
    t1, 
    t1.1,
    t1.2,
    t1.3,
  precondition:
    hasFuel,
  alpha:
    t0: ship,
    t1: cityShip,
    t2: airShip,
    t3: cityShip,
    t1.1: load,
    t1.2: drive,
    t1.3: unload,
    t2.1: load,
    t2.2: fly,
    t2.3: unload,
    t3.1: load,
    t3.2: drive,
    t3.3: unload,
```

## Isomorphic

Two task networks are isomorphic if they describe the same arrangement of task names despite using different identifiers. For $tn=(T, \prec, \alpha)$ and $\acute{tn}=(\acute{T}, \acute{\prec}, \acute{\alpha})$, we have:

$$
tn \cong \acute{tn}
$$

If any only if there exists a bijection $\sigma:T \rightarrow \acute{T}$.

With $t,\acute{t} \in T$, it holds that $(t,\acute{t}) \in \prec$, if and only if $(\sigma(t),\sigma(\acute{t})) \in \acute{\prec}$ and $\alpha(t) = \acute{\alpha}(\sigma(t))$

Explanation
- Like Graph or Tree, there are a few applications when we are able compare two task networks. For example, if two task networks are isomorphic, it's going to be useful for predicting, prunning, detecting loop,...
- We pick $t$ and $\acute{t} \in T$ and with a relation $\prec$ between the two $t$ and $\acute{t}$. If we want the isomorphic to holds, there are two importang things:
  - Exists a relation $\acute{\prec}$ for the bijected $t$ and $\acute{t}$ in the new region
  - Mapping $\alpha$ help us get the task names, and the two task names in two region need to be equal.

Example: Two isomorphic task networks with the same task name `cityShip`
```
task_network_1: 
  tasks: 
    t0, 
    t1,
  precondition: 
    hasFuel,
  alpha:
    t0: ship,
    t1: cityShip,

task_network_2: 
  tasks: 
    t0,
    t3,
  precondition: 
    hasFuel,
  alpha:
    t0: ship,
    t3: cityShip,
```

## Method

Method $m = (n, tn_m)$ maps a compound task name n to a task network tn

decomposes a task network $tn_1 = (T_1, \prec, \alpha_1)$ into a new task network $tn_2$  by replacing task t, written $tn_1 \xrightarrow[t,m]{} tn_2$, 

Example: 
```
cityShip(x,y,z):  
  compound_task_name: ship(x,y,z)
  task_network: 
    tasks: 
      t1, 
      t1.1,
      t1.2,
      t1.3,
    precondition: 
      hasFuel,
    alpha:
      t0: ship,
      t1: cityShip,
      t2: airShip,
      t3: cityShip,
      t1.1: load,
      t1.2: drive,
      t1.3: unload,
      t2.1: load,
      t2.2: fly,
      t2.3: unload,
      t3.1: load,
      t3.2: drive,
      t3.3: unload,
```

## Domain
Thomas Geier and Pascal Bercher [1] mixed the planning problem and domain together. So let's stick with the newer definition from Bercher et al [2] where the problem and domain definitions are separated nicely.

5-tuple Domain $D = F, N_P, N_C, \delta, M$ 

- $F$: finite set of facts / proposition symbol

- $N_P$: finite set of primitive task names with $N_P \bigcap N_C = \emptyset$

- $N_C$: finite set of compound task names

- $\delta : N_P \rightarrow 2^F \times 2^F \times 2^F$, action mappings (assign actions to primitive task names)

- $M \subseteq C \times TN_{C\bigcup{O}}$: a finite set of decomposition methods


## Problem
3-tuple:  $(D, s_I, tn_I)$

- $D$: HTN Domain

- $s_I \in s^F$: initial state

- $tn_I$: initial task network

With $tn_I := ({t_I }, \emptyset, {(t_I , c_I )})$

## Solution / Plan

![image](https://github.com/hughiephan/DPL/assets/16631121/23f66b59-a236-42b7-a8d2-6a6451e97546)

## Executable Task Network

## Task Insertion

## References
- [1] Thomas Geier and Pascal Bercher. 2011. On the decidability of HTN planning with task insertion. In Proceedings of the Twenty-Second international joint conference on Artificial Intelligence - Volume Volume Three (IJCAI'11). AAAI Press, 1955–1961.
- [2] Bercher, P., Alford, R., & Höller, D. (2019). A Survey on Hierarchical Planning – One Abstract Idea, Many Concrete Realizations. In Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, ĲCAI-19 (pp. 6267–6275). International Joint Conferences on Artificial Intelligence Organization.


