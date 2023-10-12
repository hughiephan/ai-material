# HTN

![image](https://github.com/hughiephan/DPL/assets/16631121/0638e801-18b9-48be-bc57-21c83fce09db)

## Task Network Definition

$$
tn=(T, \prec, \alpha)
$$

Function alpha to map task id to task name

A task network $tn$ consists of a set of constraints $\prec$

```
task_network: 
  tasks: 
    cityShip(x,y,z), 
    load,
    drive,
    unload,
  precondition: 
    isSafe(x),
    hasGas(y),
  
```

## Method

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
