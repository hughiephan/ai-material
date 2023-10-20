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
  task: t1, t2, t3
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
  task: t1.1, t1.2, t1.3
  precondition: <t1.1, t1.2, t1.3>
  alpha:
    t1.1: load,
    t1.2: drive,
    t1.3: unload

tn3: 
  task: t3.1, t3.2, t3.3
  precondition: <t3.1, t3.2, t3.3>
  alpha:
    t3.1: load,
    t3.2: drive,
    t3.3: unload
```

## Initial Task Network

![image](https://github.com/hughiephan/DPL/assets/16631121/def7b4b9-80df-4a8b-a224-0cc2e3bc78d7)

$$
tn_I := ({t_I}, \emptyset, {(t_I , n_I )})
$$

The initial task network which consists of the initial task $t_I$ mapping to the initial task name $n_I$. Precondition is an empty set.

Example: We create the initial task network with no precondition, task ids, and alpha function to map the task with task names. Initial Task Network is different from the initial task, meaning that Initial Task Network can combines multiple initial tasks, not just one task.

```
tnI: 
  task: t0
  precondition: <>
  alpha:
    t0: ship(pkg1, whA, shopB)
```

## Method

![image](https://github.com/hughiephan/DPL/assets/16631121/807f80e0-1977-45d1-a29f-038700fd8586)

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
    task: t1, t2, t3
    precondition: <t1, t2, t3>
    alpha:
      t1: cityShip(pkg1, whA, airpA),
      t2: airShip(pkg1, airpA, airpB),
      t3: cityShip(pkg1, airpB, shopB)
```

We can decompose Task Network `tn1` from previous step into Task Network `tn4` using `m-cityShip` method

![image](https://github.com/hughiephan/DPL/assets/16631121/b20303a6-a539-4c47-8719-83590511e2d7)

```
tn4: 
  task: t1.1, t1.2, t1.3, t2, t3
  precondition: <t1.1, t1.2, t1.3, t2, t3>
  alpha:
    t1.1: load,
    t1.2: drive,
    t1.3: unload,
    t2: airShip(pkg1, airpA, airpB),
    t3: cityShip(pkg1, airpB, shopB)
```

## Domain

![image](https://github.com/hughiephan/DPL/assets/16631121/628f9707-4d27-442b-bd79-786f179438d9)

Thomas Geier and Pascal Bercher [2] mixed the planning problem and domain together. So let's stick with the newer definition from Bercher et al [3] where the problem and domain definitions are separated nicely.

$$
D = (F, N_C, N_P, \delta, M)
$$ 

- $F$: finite set of facts 
- $N_C$: finite set of compound task names
- $N_P$: finite set of primitive task names 
- $\delta$, action mappings. It will assign actions to primitive task names.
- $M$: a finite set of decomposition methods

Explanation: Delta $\delta$ function has the same purpose of Alpha $\alpha$ function, mapping unique IDs to task names because there can be duplicate task names. But the different is that $\delta$ only works with primitive task names, while $\alpha$ works will both primitive and compound task names. Maybe this has the purpose of helping us get the ordered combination of primitive tasks as plan. Final solution cannot contain compound task names, so Delta $\delta$ help us track the primitive tasks.

Example:
- Set of facts: $F$ = {f-load, f-fly, f-drive, f-unload) 
- Set of compound task names: $N_C$ = { ship, cityShip, airShip }
- Set of primitive task names: $N_P$ = { load, fly, drive, unload }
- With Delta $\delta$ function, we have a set of actions to primitive task names: {(a1, load), (a2, fly), (a3, unload), (a4, load), (a5, drive), (a6, unload), (a7, load), (a8, drive), (a9, unload)}
- With $M$ function, we have a set of decomposition methods: {(ship(pkg1, whA, shopB), tn0), (cityShip(pkg1, whA, airpA), tnX), (airShip(pkg1, airpA, airpB), tnY), (cityShip(pkg1, airpB, shopB),tnZ)}

Above example but written in different form:
```
domain:
  fact: f-load, f-fly, f-drive, f-unload
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
- $s_I$: initial state
- $tn_I$: initial task network

Example:
```
problem:
  initial_state: s0
  tnI: 
    task: t0
    precondition: <>
    alpha:
      t0: ship(pkg1, whA, shopB)
  domain:
    fact: f-load, f-fly, f-drive, f-unload
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

# Executable Task Network

A task network is called executable if there exists an executable linearization of its tasks.

## Solution
$tn_S$ is a solution of problem $P$, if and only if $tn_s$ can be obtained from initial task network $tn_I$ by a sequence of method applications, does not contain compound task anymore, and is executable. 

- $tn_I \rightarrow tn$ 
- $\forall{t} \in T$
- Sequence < $t_1t_2...t_n$ > of the tasks is in line with $\prec$
- (Optional) < $(\alpha(t_1)\alpha(t_2)...\alpha(t_n)$ > in $s_I$ results in a goal state.

Given:
- $tn=(T, \prec, \alpha)$
- $D$ : HTN Domain
- $P$ : HTN Problem

Explanation:
- The task network can be reached by decomposing the initial task network
- All the task names in the Task Network are primitive.
- The sequence of tasks need to follow the rule of preconditions.
- Combines task decomposition with state-based goals. This could also be used without state-based goal.

Possible route

![image](https://github.com/hughiephan/DPL/assets/16631121/fb0e7e61-ea45-4693-a96d-34fbaf96fbfd)

Solution

![image](https://github.com/hughiephan/DPL/assets/16631121/cee81b01-8ea2-4115-84d0-ffae0251d9a2)

Plan $\pi$ =〈load, drive, unload, load, fly, unload, load, drive, unload〉


## Task Insertion
In case the plane is not in the airport of city A, the air transportation task airShip(pkg1, airpA, airpB) cannot be accomplished, and neither can the initial task. When arranging the plane to airport A, fly(plane1, airpA), is done before loading to the plane, and an executable plan is found.  

![image](https://github.com/hughiephan/DPL/assets/16631121/3f06cfa0-8d3b-4436-bda4-cec8685776cb)

$$
tn_2 = (T_1 \cup \{t\}, \prec_1, \alpha_1 \cup \{(t,p)\})  
$$

With:
- $tn_1 =  (T_1, \prec_1, \alpha_1)$: a task network  
- $p$: a primitive task name 
- $t \notin T_1$

Explanation:
- First of all, the new task to be inserted should not already exist in $tn_1$ and it can only be primitive task. The new task network $tn_2$ will be an expansion of the previous tasks in $tn_1$ with our new primitive task. But the preconditions should stay the same because our inserted task's purpose is to assist the planner in reaching the goal, not changing the logic of the problem. Alpha $\alpha$ function help us generate a task id for the new inserted task.


## Undeciability of HTN Planning 
$$
G= (\Gamma, \sum, R, S)  
$$

With $i \in {1,2} $, we have $G_1, G_2$, two CFG in Chomsky normal form, then:

- $\sum$: set of terminal symbols 
- $\Gamma$: non-terminal symbols of $G_i$ 
- $S_i \in \Gamma_i$: start symbol of $G_i$ with $i \in {1,2} $
- $R_i$: grammar rules of $G_i$, 

Production Rule $R1$ and $R2$ has either form (Chomsky normal form):
- $X \rightarrow Y Z$ (with X is non-terminal symbols -> Y, Z  are also non-terminal symbols)
- $X \rightarrow\ a$  (with X is non-terminal symbol -> a terminal symbol)

And $L(G_i)$: is the language of $G_i$ which is the set of strings it generates

Assume 
- $\Gamma_1 \cap \Gamma_2  = \emptyset$
- $\epsilon \notin L(G_1) \cup L(G_2)$

Also define:
- $\Gamma := \Gamma_1 \cup \Gamma_2$
- $R := R_1 \cup R_2$

CFG fits with HTN Planning is because we can can derive the string by repeatedly replacing a non-terminal by the right hand side of the production, until all non-terminal have been replaced by terminal symbols. We can think of non-terminal symbols as Compound Tasks, and terminal symbols as Primitive Tasks. Two Formal Grammar G1 and G2 was processed in parallel. We can prove this by transform our HTN Formalization into two CFG. Then because of "whether the languages of two CFGs have a non-empty intersection" is undecidable [7] then our HTN Formalization will also be undeciable.

![image](https://github.com/hughiephan/DPL/assets/16631121/0702cf4d-5079-4abc-b6af-54654adf463b)

Example:
- $G1 = (\lbrace H,Q \rbrace, \lbrace a, b \rbrace, R1, H)$
- $G2 = (\lbrace D,F \rbrace, \lbrace a, b \rbrace, R2, D)$
- Production Rules R1:  
  - H can be decomposed into aQb
  - Q can be decomposed into aQ, bQ, a or b
- Production Rules R2:
  - D can be decomposed into aFD or ab
  - F can be decomposed into a or b

$$
PLAN-EXISTENCE_{HTN} : \text{is undeciable}
$$ 

Construct the Domain and Problem:
- $D = (F, N_C, N_P, \delta, M)$
- $P^* = (D, s_I, tn_I, g)$

With Goal description $g$ can be compiled away into $P$, by adding a new primitive task $p$ with $g$ as precondtion, $\delta(p) = (g, \emptyset, \emptyset)$

Then:

- $F := \lbrace (turn_{G1}, turn_{G2}) \rbrace \cup \sum$
- $N_C := \Gamma \cup \lbrace c_I \rbrace$
- $N_P := \lbrace G_i^a | a \in \sum , i \in \lbrace 1,2 \rbrace \rbrace \cup \lbrace F \rbrace$
- $s_I := \lbrace turn_{G1} \rbrace$
- $M := \lbrace (c_I, tn \rbrace \cup$ $X, tn_{X \rightarrow YZ} | X \rightarrow Y Z \in R \rbrace \cup$ $X, tn_{X \rightarrow a} | X \rightarrow a \in R_i, i \in \lbrace 1,2 \rbrace \rbrace$, where:
  - $tn := (\lbrace s_1,s_2,f \rbrace, \lbrace (s_1,f), (s_2,f) \rbrace, \lbrace (s_1, S_1), (s_2, S_2), (f,F) \rbrace)$
  - $tn_{X \rightarrow YZ} := (\lbrace t, \acute{t} \rbrace, \lbrace (t, \acute{t} \rbrace), \lbrace t, Y \rbrace, \lbrace \acute{t}, Z \rbrace)$
  - $tn_{X \rightarrow a} := (\lbrace t \rbrace, \emptyset, \lbrace (t, G_i^a) \rbrace)$

With: 
- $G_1^a = (\lbrace turn_{G1} \rbrace, \lbrace turn_{G2}, a \rbrace \lbrace turn_{G1} \rbrace)$
- $G_2^a = (\lbrace turn_{G2}, a \rbrace, \lbrace turn_{G1} \rbrace \lbrace turn_{G2}, a \rbrace)$

Example:
- $tn_I = (\lbrace t1, t2 \rbrace, \emptyset, \lbrace (t1, H), (t2, D) \rbrace)$ . Task Network has two task id $t1$ and $t2$, no precondition and mapping between $t1$ and $t2$ with the initial tasks $H$ and $D$
- $s_I = \lbrace turn_{G1} \rbrace$ 
- $F = \lbrace F_{turn_{G1}}, F_{turn_{G2}} \rbrace \cup \lbrace F_{a}, F_{b} \rbrace$
- $N_C = \lbrace H, Q, D,F \rbrace \cup \lbrace H, D \rbrace$
- $N_P = \lbrace (\lbrace turn_{G1} \rbrace, \lbrace turn_{G2}, a \rbrace \lbrace turn_{G1} \rbrace),$ 
  - $(\lbrace turn_{G1} \rbrace, \lbrace turn_{G2}, b \rbrace \lbrace turn_{G1} \rbrace),$
  - $(\lbrace turn_{G2}, a \rbrace, \lbrace turn_{G1} \rbrace \lbrace turn_{G2}, a \rbrace)$
  - $(\lbrace turn_{G2}, b \rbrace, \lbrace turn_{G1} \rbrace \lbrace turn_{G2}, b \rbrace) \rbrace$
  - $\cup \lbrace F_{turn_{G1}}, F_{turn_{G2}} \rbrace$ 
  - $\cup \lbrace F_{a}, F_{b} \rbrace$
- $M$ ???

The task network $tn_6$ is the solution because both the word abab appear twice, and only consists of Primitive Tasks.

## Classical Problem
$$
P_c = (F, N_A, s_I, g, \delta)
$$

- Sometimes Classical Problem is defined with a 4-tuple without the Delta $\delta$
- F is set of propositional environment facts
- $s_I \subseteq F$ is initial state
- $g \subseteq F$ gives the goal definition
- $N_A$ is a finite set of action names
- $\delta = (prec, add, del)$ contains functions. Functions map action name to subset of environment facts.
- State is set of facts
- Action a is applicable in state s, with relation  \( \tau(a,s) \iff prec(a) \subseteq s$
- When applicable, state transition function: $\gamma(a,s) = (s \ del(a)) \bigcup add(a)$, 
- Sequence of actions $(a_0,a_1...a_l)$ with $a_i \in N_A$ is applicable in a state $s_I$ if and only if $a_i$ is applicable in $s_i$, with $s_i$ is defined as $\gamma(a_{i-1},s_{i-1})$ for $i > 0$. State $s_{l+1}$ results from application.
- Solution is a sequence $(a_0,a_1...a_l)$ that is applicable in $s_I$ that results in state $s_{l+1}$, with $s_{l+1} \supseteq g$

## Questions
### Question: Task hierarchy model physic and advice?

### Question: Classical vs TIHTN planning
- Task insertion plus goal description fully subsumes classical planning (while allowing task hierarchies as well)

### Question: Classical vs HTN planning
In Classical Planning, the state is a sequence of actions. But the state in HTN is a hierarchy.

![image](https://github.com/hughiephan/DPL/assets/16631121/f5968d79-9c1e-4461-bd02-d62bc3eab1be)

In Classical Planning, the Actions have deterministic effects, meaning that one action only results in one outcome. This HTN formalism works in deterministic domain. There are other works for HTN on Nondeterministic domain [4]

In real-world / complex planning problems, the environment can be partially observable. This means that the planner does not have complete information about the current state and may need to make decisions based on partial or uncertain information. Classical Planning only works with fully observable environment. This HTN Planning also works on fully observable environment. There are other HTN that can work on partially observable environment (for example, Partially Observable Markov Decision Processes POMDP can works on partially observable environment)

In Classical Planning, there is no consideration of time. Time duration is Instantaneous meaning it does not consider the time it takes to perform each action and the effects of actions occurring simultaneously. This HTN also does not consider time. There is the paper TimeLine [5] on HTN that can deal with time.

In Classical Planning, it's is Static.  We see that Classical Planning does not consider time so there can be no exogenous event. An exogenous event can be defined as a happening that occurs at a specific point along a conceptual timeline and changes the world state by altering the value of one or more predicates. For example: Electricity will be available at 10 AM. Thus, actions that need electricity will only be able to execute after 10 AM [6]. This paper HTN is also static. Due to this paper on TimeLine [5], it is theoretically possible for HTN Planning's word dynamics to be Exogenous Events.

Both Classical and HTN planning have sequential plans with a linearly ordered sequence of actions (a1, a2, … an) 

Both Classical and HTN is finite system (finite states, actions, events). If we want to model the domain and problem as inifite system, maybe use Turing infinite state machine.

The goal in classical planning is defined by a set of state features that shall be achieved. Therefore classical heuristics are designed to estimate the distance from a given state to a goal state. In HTN planning the “goal” is an abstract task to perform; no state-based goal is given. HTN will decompose high level abstraction tasks.

### Question: HTN vs TIHTN planning
To be written

### Question: Task Network Solution vs Solution

## References
- [1] Xiao, Z., Wan, H., Zhuo, H., Herzig, A., Perrussel, L., & Chen, P. (2019). Refining HTN Methods via Task Insertion with Preferences. AAAI Conference on Artificial Intelligence.
- [2] Thomas Geier and Pascal Bercher. 2011. On the decidability of HTN planning with task insertion. In Proceedings of the Twenty-Second international joint conference on Artificial Intelligence - Volume Volume Three (IJCAI'11). AAAI Press, 1955–1961.
- [3] Bercher, P., Alford, R., & Höller, D. (2019). A Survey on Hierarchical Planning – One Abstract Idea, Many Concrete Realizations. In Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, ĲCAI-19 (pp. 6267–6275). International Joint Conferences on Artificial Intelligence Organization.
- [4] Chad Hogg, Ugur Kuter, and Héctor Muñoz-Avila. 2009. Learning hierarchical task networks for nondeterministic planning domains. In Proceedings of the 21st International Joint Conference on Artificial Intelligence (IJCAI'09). Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 1708–1714.
- [5] Yaman, Fusun & Nau, Dana. (2003). TimeLine: An HTN Planner That can Reason About Time. AIPS Workshop on Planning for Temporal Domains, 2002. 
- [6] Do, Minh & Kambhampati, Subbarao & Zimmerman, Terry. (2004). Planning - Scheduling Connections through Exogenous Events. 
- [7] Hopcroft et al., 2000 John E. Hopcroft, Rajeev Motwani, and Jeffrey D. Ullman. Introduction to Automata Theory, Languages, and Computation, volume 3. Addison-Wesley Reading, MA, second edition, 2000.
- https://web.stanford.edu/class/cs227/Lectures/lec16.pdf
