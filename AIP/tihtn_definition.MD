# Formal Definition of Hierarchical Task Network with Task Insertion (TIHTN)

Considering the logistics domain example from Xiao et al [1], we have made a few modifications for an easier explanation of the HTN Definition. Suppose every task has only one method, the initial task `ship(pkg1, whA, shopB)` is to ship a package from city A to city B and it has a method: to ship the package from the warehouse to the airport by truck, from city A to city B by plane, and from the airport to the shop by truck. 

![image](https://github.com/hughiephan/DPL/assets/16631121/9fdf6121-4768-482e-9b8c-a3f19a9fd869)

## Task Network

![image](https://github.com/hughiephan/DPL/assets/16631121/d95f2428-59f5-40c3-904a-8f8ea13edc1f)

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
tn1: 
  precondition: <t1, t2, t3>
  alpha:
    t1: cityShip(pkg1, whA, airpA),
    t2: airShip(pkg1, airpA, airpB),
    t3: cityShip(pkg1, airpB, shopB)
```

## Isomorphic

![image](https://github.com/hughiephan/DPL/assets/16631121/de836baf-b114-4fe8-a24f-5945e77f3d77)

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

Example: Two isomorphic task networks with the same task names `load`, `drive`, and `unload`
```
tn2: 
  precondition: <t1.1, t1.2, t1.3>
  alpha:
    t1.1: load,
    t1.2: drive,
    t1.3: unload

tn3: 
  precondition: <t3.1, t3.2, t3.3>
  alpha:
    t3.1: load,
    t3.2: drive,
    t3.3: unload
```

## Initial Task Network

![image](https://github.com/hughiephan/DPL/assets/16631121/60c9a766-504c-48f7-9ff9-35b75505e4a3)

$$
tn_I := ({t_I}, \emptyset, {(t_I , n_I )})
$$

The initial task network which consists of the initial task $t_I$ mapping to the initial task name $n_I$. Precondition is an empty set.

Example: We create the initial task network with no precondition, task ids, and alpha function to map the task with task names.

```
tnI: 
  precondition: <>
  alpha:
    t0: ship(pkg1, whA, shopB)
```

## Method

![image](https://github.com/hughiephan/DPL/assets/16631121/c5cad797-9d31-4eca-8f70-838ccfaf6fed)

$$
m = (n, tn_m)
$$ 

Method maps a compound task name to a task network. 
- $n$: compound task name 
- $tn_m$: task network

Method will decomposes a task network $tn_1 = (T_1, \prec, \alpha_1)$ into a new task network $tn_2$  by replacing task t, written $tn_1 \xrightarrow[t,m]{} tn_2$, 

Example: `m-cityShip` method is used for mapping the compound task name `cityShip(pkg1, whA, airpA)` to Task Network `tn1`
```
m-cityShip:
  compound_task_name: cityShip(pkg1, whA, airpA)
  tn1: 
    precondition: <t1, t2, t3>
    alpha:
      t1: cityShip(pkg1, whA, airpA),
      t2: airShip(pkg1, airpA, airpB),
      t3: cityShip(pkg1, airpB, shopB)
```

We can decompose Task Network `tn1` from previous step into Task Network `tn4` using `m-cityShip` method

![image](https://github.com/hughiephan/DPL/assets/16631121/2e0885f6-4f32-4164-8ba5-18ddf5794bb7)

```
tn4: 
  precondition: <t1.1, t1.2, t1.3, t2, t3>
  alpha:
    t1.1: load,
    t1.2: drive,
    t1.3: unload,
    t2: airShip(pkg1, airpA, airpB),
    t3: cityShip(pkg1, airpB, shopB)
```


## Domain

![image](https://github.com/hughiephan/DPL/assets/16631121/105a92f7-0a96-4e42-9796-73e5ec55dd2d)

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
  fact:???
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
  method:
    m-ship
      compound_task_name: ship(pkg1, whA, shopB), 
      tn0, 
    m-cityShip
      compound_task_name: cityShip(pkg1, whA, airpA),
      tnX,  
    m-airShip
      compound_task_name: airShip(pkg1, airpA, airpB),
      tnY,
    m-cityShip
      compound_task_name: cityShip(pkg1, airpB, shopB),
      tnZ
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
  initial_state: ???
  tnI: 
    precondition: <>
    alpha:
      t0: ship(pkg1, whA, shopB)
  domain:
    fact: ???
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
    method:
      m-ship
        compound_task_name: ship(pkg1, whA, shopB), 
        tn0, 
      m-cityShip
        compound_task_name: cityShip(pkg1, whA, airpA),
        tnX,  
      m-airShip
        compound_task_name: airShip(pkg1, airpA, airpB),
        tnY,
      m-cityShip
        compound_task_name: cityShip(pkg1, airpB, shopB),
        tnZ
```

## Executable Task Network

$tn=(T, \prec, \alpha)$ is executable in state $s \in 2^L$

If and only if:
- It is primitive
- Exist a linearization of tasks t1,...,tn compatible with $\prec$ and sequence states $s_0,...s_n$ such that $s_0 = s$

Explantion:
- This definition is important because we don't want to create an task network that can not be run. The solution will be based on this.
- Executable Task Network should only consists of primitive tasks.
- I think linearization means that we want to have a definite route from task t1 to task tn. We don't want it to loop.

Example: To be written

## Solution

Possible route

![image](https://github.com/hughiephan/DPL/assets/16631121/fb0e7e61-ea45-4693-a96d-34fbaf96fbfd)

Solution

![image](https://github.com/hughiephan/DPL/assets/16631121/cee81b01-8ea2-4115-84d0-ffae0251d9a2)

Plan $\sigma_1$ =〈load, drive, unload, load, fly, unload, load, drive, unload〉


## Task Insertion
In case the plane is not in the airport of city A, the air transportation task airShip(pkg1, airpA, airpB) cannot be accomplished, and neither can the initial task. When arranging the plane to airport A, fly(plane1, airpA), is done before loading to the plane, and an executable plan is found.

![image](https://github.com/hughiephan/DPL/assets/16631121/b9807dbb-ab23-4320-84ef-7d3d7430ad42)

$$
tn_2 = (T_1 \cup \{t\}, \prec_1, \alpha_1 \cup \{(t,o)\})  
$$

With:
- $tn_1 =  (T_1, \prec_1, \alpha_1)$: a task network  
- $o$: a primitive task name 
- $t \notin T_1$

Explanation:
- First of all, the new task to be inserted should not already exist in $tn_1$ and it can only be primitive task. The new task network $tn_2$ will be an expansion of the previous tasks in $tn_1$ with our new primitive task. But the preconditions should stay the same because our inserted task's purpose is to assist the planner in reaching the goal, not changing the logic of the problem. Alpha $\alpha$ function help us generate a task id for the new inserted task.

Example: Inserting a new primitive task name `fly`
```
task_network_2: 
  precondition:
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
    t4: fly,           <--------- Map the new task ID with the new primitive task name
```

## References
- [1] Xiao, Z., Wan, H., Zhuo, H., Herzig, A., Perrussel, L., & Chen, P. (2019). Refining HTN Methods via Task Insertion with Preferences. AAAI Conference on Artificial Intelligence.
- [2] Thomas Geier and Pascal Bercher. 2011. On the decidability of HTN planning with task insertion. In Proceedings of the Twenty-Second international joint conference on Artificial Intelligence - Volume Volume Three (IJCAI'11). AAAI Press, 1955–1961.
- [3] Bercher, P., Alford, R., & Höller, D. (2019). A Survey on Hierarchical Planning – One Abstract Idea, Many Concrete Realizations. In Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, ĲCAI-19 (pp. 6267–6275). International Joint Conferences on Artificial Intelligence Organization.

# Extra

## Formal Grammar 
To be written (Section 3 of paper On the Decidability of HTN Planning with Task Insertion, IJCAI'11)

## Questions
Here are the concepts I could not fully grasp about HTN yet:
- What is State and Fact?
- CFG Proof?
- Propositional Symbols?
- Why $s \in 2^L$?
- Sequence of state and sequence of tasks?

## Note
- $\epsilon$ is an empty sequence

## Classical Problem
$$
P_c = (L, A, s_0, g, \delta)
$$

- L is set of propositional environment facts
- $s_0 \subseteq L$ is initial state
- $g \subseteq L$ gives the goal definition
- A is set of action names
- $\delta = (prec, add, del)$ contains functions. Functions map action name to subset of environment facts : $A -> 2^L$
- State is set of facts
- Action a is applicable in state s, with relation $\tau = A \times 2^L \), \( \tau(a,s) \iff prec(a) \subseteq s$
- When applicable, state transition function: $\gamma : A \times 2^L \rightarrow 2^L$, $\gamma(a,s) = (s \ del(a)) \bigcup add(a)$, 
- Sequence of actions $(a_0,a_1...a_l)$ with $a_i \in A$ is applicable in a state $s_0$ if and only if $a_i$ is applicable in $s_i$, with $s_i$ is defined as $\gamma(a_{i-1},s_{i-1})$ for $i > 0$. State $s_{l+1}$ results from application.
- Solution is a sequence $(a_0,a_1...a_l)$ that is applicable in $s_0$ that results in state $s_{l+1}$, with $s_{l+1} \supseteq g$
