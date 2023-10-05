# Build PDDL Domain and Problem with PDDL 3.1 Lirabry

## Step: Import libraries
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

Our predicates:
- Is x = `p1`? 
- Is x = `p2`? 
- Is x of `type_1` ? 
- Is y of `type_1` ? 
- Is z of `type_1` ?
 
## Step: Actions
Description: Our agent can do action-1. Precondition: p1(x, y, z) is true and p2(y,z) is not true. Effect: p2(y, z) becomes true and everything else doesn't change

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

Output of `domain_to_string(domain)`:
```
(define (domain my_domain)
    (:requirements :strips :typing)
    (:types type_1)
    (:constants a b c - type_1)
    (:predicates (p1 ?x - type_1 ?y - type_1 ?z - type_1)  (p2 ?x - type_1 ?y - type_1))
    (:action action-1
        :parameters (?x - type_1 ?y - type_1 ?z - type_1)
        :precondition (and (p1 ?x ?y ?z) (not (p2 ?y ?z)))
        :effect (p2 ?y ?z)
    )
)
```

## Step: Problem
```python
problem = Problem(
    "problem-1",
    domain=domain,
    requirements=requirements,
    objects=[a, b, c],
    init=[p1(a, b, c), ~p2(b, c)],
    goal=p2(b, c)
)
print(problem_to_string(problem))
```

Output of `problem_to_string(problem)`:
```
(define (problem problem-1)
    (:domain my_domain)
    (:requirements :strips :typing)
    (:objects a b c - type_1)
    (:init (not (p2 b c)) (p1 a b c))
    (:goal (p2 b c))
)
```

## Step: Planning
Solve with https://editor.planning.domains

![image](https://github.com/hughiephan/DPL/assets/16631121/df1fa996-89b7-4063-a4f2-459fc9557fe9)

## References
- https://github.com/AI-Planning/pddl
