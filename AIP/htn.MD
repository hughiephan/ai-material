# HTN

## Task Network Definition

$$
tn=(T, \prec, \alpha)
$$

Function alpha to map task id to task name

Atask network $tn$ consists of a set of constraints $\prec$


## Method

![image](https://github.com/hughiephan/DPL/assets/16631121/91d734a2-18a2-4db5-9a9e-bff02fc2f361)

Method $m = (n, tn_m)$ maps a compound task name n to a task network tn

decomposes a task network $tn_1 = (T_1, \prec, \alpha_1)$ into a new task network $tn_2$  by replacing task t, written $tn_1 \xrightarrow[t,m]{} tn_2$, 

Example: 
```
cityShip(x,y,z):  
  compound_task_name: ship(x,y,z)
  task_network: 
    cityShip(x,y,z), 
    load,
    drive,
    unload,
```

## Context Free Language


## References
- ...
