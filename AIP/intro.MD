# Introduction to AI Planning

## Step: 
```python
!pip install git+https://github.com/AI-Planning/pddl.git
from pddl.logic import Predicate, constants, variables
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements
```

## Step: Variables and constants
```python
x, y, z = variables("x y z", types=["type_1"])
a, b, c = constants("a b c", type_="type_1")
```

## Step: Predicates
Predicates are properties of objects that we are interested in; can be true or false.
```python
p1 = Predicate("p1", x, y, z)
p2 = Predicate("p2", x, y)
```
 
## Step: Actions
```python
a1 = Action(
    "action-1",
    parameters=[x, y, z],
    precondition=p1(x, y, z) & ~p2(y, z),
    effect=p2(y, z)
)
```

## Step: Domain
```python
requirements = [Requirements.STRIPS, Requirements.TYPING]
domain = Domain("my_domain",
                requirements=requirements,
                types={"type_1": None},
                constants=[a, b, c],
                predicates=[p1, p2],
                actions=[a1])
print(domain_to_string(domain))
```

Is x a `p1`? Is x of `type_1` ? Is z of `type_1`

Is x a `p2`? Is y of `type_1` ? 

![image](https://github.com/hughiephan/DPL/assets/16631121/9a3ac7fa-079f-4560-9156-d1c4eeba83c7)

Format of Domain:

![image](https://github.com/hughiephan/DPL/assets/16631121/67cdde16-1c8f-4c68-9817-8edb5570f6a9)


## References
- https://github.com/AI-Planning/pddl
- https://www.cs.toronto.edu/~sheila/2542/s14/A1/introtopddl2.pdf
