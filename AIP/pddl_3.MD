# Solve problem with PDDL Editor and PDDL 3.1 Library

## Step 1: Import libraries
```python
!pip install git+https://github.com/AI-Planning/pddl.git
from pddl.logic import Predicate, constants, variables
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements
```

## Step 2: Variables
```python
x, y, z = variables("x y z")
```

## Step 3: Objects and constants
```python
a, b, c = constants("a b c")
```

## Step 4: Predicates
Predicates are properties of objects that we are interested in; can be true or false.
```python
predicates = [
    Predicate("p1", x, y, z),
    Predicate("p2", x, y),
]
```

Our predicates:
- Is x = `p1`? 
- Is x = `p2`? 
- Is x of `type_1` ? 
- Is y of `type_1` ? 
- Is z of `type_1` ?
 
## Step 5: Actions
Description: Our agent can do action-1. Precondition: p1(x, y, z) is true and p2(y,z) is not true. Effect: p2(y, z) becomes true and everything else doesn't change

```python
a1 = Action(
    "action-1",
    parameters=[x, y, z],
    precondition=p1(x, y, z) & ~p2(y, z),
    effect=p2(y, z)
)
```

## Step 6: Domain
```python
domain = Domain("domain_1",
                requirements='',
                constants=[a, b, c],
                predicates=predicates,
                actions=[a1])
print(domain_to_string(domain))
```

Output of `domain_to_string(domain)`, but before we input this into solver, remove `(:types)` the line
```
(define (domain domain_1)
    (:types)    <------ Remove this before inputting into a planner.
    (:constants a b c)
    (:predicates (p1 ?x ?y ?z)  (p2 ?x ?y))
    (:action action-1
        :parameters (?x ?y ?z)
        :precondition (and (p1 ?x ?y ?z) (not (p2 ?y ?z)))
        :effect (p2 ?y ?z)
    )
)
```

## Step 7: Problem
```python
problem = Problem(
    "problem_1",
    domain=domain,
    requirements='',
    objects=[a, b, c],
    init=[Predicate("p1", a, b, c), ~Predicate("p2", b, c)],
    goal=Predicate("p2", b, c)
)
print(problem_to_string(problem))
```

Output of `problem_to_string(problem)`:
```
(define (problem problem_1)
    (:domain domain_1)
    (:objects a b c)
    (:init (not (p2 b c)) (p1 a b c))
    (:goal (p2 b c))
)
```

## Step 8: Planning
Solve with https://editor.planning.domains

![image](https://github.com/hughiephan/DPL/assets/16631121/df1fa996-89b7-4063-a4f2-459fc9557fe9)

## References
- https://github.com/AI-Planning/pddl
