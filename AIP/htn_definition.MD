# Formal Definition of Hierarchical Task Network

## Decomposition Tree

![image](https://github.com/hughiephan/DPL/assets/16631121/639dc0bc-e1e5-4fde-ba81-7d9d207dcba2)

## Goal

![image](https://github.com/hughiephan/DPL/assets/16631121/23f66b59-a236-42b7-a8d2-6a6451e97546)

## Task Network

$$
tn=(T, \prec, \alpha)
$$

A task network $tn$ consists of:
- $T$: a finite and non-empty set of tasks
- $\prec$: a strict partial order on $T$(irreflexive, asymetric, and transitive). We can just call it as a set of ordering constraints/preconditions.
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
    isSafe,
    hasGas,
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
      isSafe,
      hasGas,
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

## Problem

3-tuple:  $(D, s_I, tn_I)$

- $D$: HTN Domain

- $s_I \in s^F$: initial state

- $tn_I$: initial task network


## Solution / Plan

## Executable Task Network

## Task Insertion

## References
- ...
