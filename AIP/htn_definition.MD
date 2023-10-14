# Formal Definition of Hierarchical Task Network

Considering the logistics domain example from Xiao et al [1], we have made a few modifications for an easier explanation of the HTN Definition. Suppose every task has only one method, the initial task `ship(pkg1, whA, shopB)` is to ship a package from city A to city B and it has a method: to ship the package from the warehouse to the airport by truck, from city A to city B by plane, and from the airport to the shop by truck. 

![image](https://github.com/hughiephan/DPL/assets/16631121/39c3a93c-f814-42f2-9db0-8276a8f67d79)

## Task Network

![image](https://github.com/hughiephan/DPL/assets/16631121/b91f9149-e77b-4fc9-bb7c-c1b210daaa4f)

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

![image](https://github.com/hughiephan/DPL/assets/16631121/280d8a8e-aec0-4b81-a653-425a2de539e8)

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

## Initial Task Network
![image](https://github.com/hughiephan/DPL/assets/16631121/37337703-dd25-4b60-a756-7117996b1879)

$$
tn_I := ({t_I}, \emptyset, {(t_I , n_I )})
$$

The initial task network which consists of the initial task $t_I$ mapping to the initial task name $n_I$. Precondition is an empty set.

Example: We create the initial task network with no precondition, task ids, and alpha function to map the task with task names.

```
task_network_initial: 
  tasks: 
    t0
  alpha:
    t0: ship
```

## Method

![image](https://github.com/hughiephan/DPL/assets/16631121/13f2cc99-53a8-4707-884e-93efcf6a0341)

$$
m = (n, tn_m)
$$ 

Method maps a compound task name to a task network. 
- $n$: compound task name 
- $tn_m$: task network

Method will decomposes a task network $tn_1 = (T_1, \prec, \alpha_1)$ into a new task network $tn_2$  by replacing task t, written $tn_1 \xrightarrow[t,m]{} tn_2$, 

Example: 
We have a method for mapping a compound task name `ship(x,y,z)` to `task_network_1`
```
method:
  compound_task_name: ship(x,y,z)
  task_network_1: 
    tasks: 
      t0, 
    precondition: 
      hasFuel,
    alpha:
      t0: ship
```

Then we can decompose the task network `task_network_1` into `task_network_2`:

```
task_network_2: 
  tasks: 
    t1,
    t2,
    t3,
  precondition: 
    hasFuel,
  alpha:
    t1: cityShip,
    t2: airShip,
    t3: cityShip,
```


## Domain

![image](https://github.com/hughiephan/DPL/assets/16631121/002058af-ca17-4a0b-88e2-872dbe42ce9d)

Thomas Geier and Pascal Bercher [2] mixed the planning problem and domain together. So let's stick with the newer definition from Bercher et al [3] where the problem and domain definitions are separated nicely.

$$
D = (F, N_P, N_C, \delta, M)
$$ 

- $F$: finite set of facts 
- $N_P$: finite set of primitive task names with $N_P \cap N_C = \emptyset$
- $N_C$: finite set of compound task names
- $\delta : N_P \rightarrow 2^F \times 2^F \times 2^F$, action mappings. It will assign actions to primitive task names.
- $M \subseteq C \times TN_{C\cup{O}}$: a finite set of decomposition methods

Explanation: Delta $\delta$ function has the same purpose of Alpha $\alpha$ function, mapping unique IDs to task names because there can be duplicate task names. But the different is that $\delta$ only works with primitive task names, while $\alpha$ works will both primitive and compound task names. Maybe this has the purpose of helping us get the ordered combination of primitive tasks as plan. Final solution cannot contain compound task names, so Delta $\delta$ help us track the primitive tasks.

Example:
- Set of facts: $F$ = { $x, \neg{x}, y, \neg{y}, z, \neg{z}$ }
- Set of primitive task names: $N_P$ = { load, fly, drive, unload }
- Set of compound task names: $N_C$ = { ship, cityShip, airShip }
- With Delta $\delta$ function, we have a set of actions to primitive task names: {(a1, load), (a2, fly), (a3, unload), (a4, load), (a5, drive), (a6, unload), (a7, load), (a8, drive), (a9, unload)}
- With $M$ function, we have a set of decomposition methods: {(ship(x,y,z), $tn_1$), ....}

Above example (written in different form):
```
domain:
  fact: x, not(x), y, not(y), z, not(z),
  primitive_task_name: load, fly, drive, unload,
  compound_task_name: ship, cityShip, airShip,
  delta: 
    a1: load, 
    a2: fly, 
    a3: unload,
    a4: load, 
    a5: drive, 
    a6: unload, 
    a7: load, 
    a8: drive, 
    a9: unload,
  method: [
    compound_task_name: ship(x,y,z)
    task_network_1: 
      tasks: 
        t0, 
      precondition: 
        hasFuel,
      alpha:
        t0: ship,
   
    compound_task_name: cityShip(x,y,z)
    task_network_2: 
      tasks: 
        t1, 
      precondition: 
        hasFuel,
      alpha:
        t1.1: load,
        t1.2: drive,
        t1.3: unload,
  ]
```

## Problem
$$
P = (D, s_I, tn_I)
$$ 

- $D$: HTN Domain
- $s_I \in s^F$: initial state
- $tn_I$: initial task network

Example:
```
problem:
  initial_state: x, y, z
  task_network_initial: 
    tasks: 
      t0
    alpha:
      t0: ship
  domain:
    fact: x, not(x), y, not(y), z, not(z),
    primitive_task_name: load, fly, drive, unload,
    compound_task_name: ship, cityShip, airShip,
    delta: 
      a1: load, 
      a2: fly, 
      a3: unload,
      a4: load, 
      a5: drive, 
      a6: unload, 
      a7: load, 
      a8: drive, 
      a9: unload,
    method: [
      compound_task_name: ship(x,y,z)
      task_network_1: 
        tasks: 
          t0, 
        precondition: 
          hasFuel,
        alpha:
          t0: ship,
     
      compound_task_name: cityShip(x,y,z)
      task_network_2: 
        tasks: 
          t1, 
        precondition: 
          hasFuel,
        alpha:
          t1.1: load,
          t1.2: drive,
          t1.3: unload,
    ]
```

## Solution

Possible route

![image](https://github.com/hughiephan/DPL/assets/16631121/fb0e7e61-ea45-4693-a96d-34fbaf96fbfd)

Solution

![image](https://github.com/hughiephan/DPL/assets/16631121/ed189763-02d3-44b4-8317-deae27019a0c)

Plan $\sigma_1$ =〈load, drive, unload, load, fly, unload, load, drive, unload〉

## Executable Task Network

To be written

## Task Insertion
In case the plane is not in the airport of city A, the air transportation task airShip(pkg1, airpA, airpB) cannot be accomplished, and neither can the initial task. When arranging the plane to airport A, fly(plane1, airpA), is done before loading to the plane, and an executable plan is found.

![image](https://github.com/hughiephan/DPL/assets/16631121/044ece9d-afa7-4bd4-ab5d-9fc809270e18)

$$
tn_2 = (T_1 \cup \{t\}, \prec_1, \alpha_1 \cup \{(t,o)\})  
$$

With:
- $tn_1 =  (T_1, \prec_1, \alpha_1)$: a task network  
- $o$: a primitive task name 
- $t \notin T_1$

Explanation:
- First of all, the new task to be inserted should not already exist in $tn_1$. The new task network $tn_2$ is an expansion of the previous tasks in $tn_1$ with our new task. But the preconditions should stay the same because our inserted task's purpose is to assist the planner in reaching the goal, not changing the logic of the problem. Alpha $\alpha$ function help us map the tasks.


## References
- [1] Xiao, Z., Wan, H., Zhuo, H., Herzig, A., Perrussel, L., & Chen, P. (2019). Refining HTN Methods via Task Insertion with Preferences. AAAI Conference on Artificial Intelligence.
- [2] Thomas Geier and Pascal Bercher. 2011. On the decidability of HTN planning with task insertion. In Proceedings of the Twenty-Second international joint conference on Artificial Intelligence - Volume Volume Three (IJCAI'11). AAAI Press, 1955–1961.
- [3] Bercher, P., Alford, R., & Höller, D. (2019). A Survey on Hierarchical Planning – One Abstract Idea, Many Concrete Realizations. In Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, ĲCAI-19 (pp. 6267–6275). International Joint Conferences on Artificial Intelligence Organization.


