# Build Ball Gripper with PDDL 3.1 Lirabry

There is a robot that can move between two rooms and pick up or drop balls with either of
his two arms. Initially, all balls and the robot are in the first room. We want the balls to be in
the second room.

## Step: Import libraries
```python
!pip install git+https://github.com/AI-Planning/pddl.git
from pddl.logic import Predicate, constants, variables
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements
```


## Step: Move Action
```python
x, y = variables("x y")

move = Action(
    "move",
    parameters=[x, y],
    precondition=Predicate("ROOM", x) & Predicate("ROOM", y) & Predicate("at-robby", x),
    effect=Predicate("at-robby", y) & ~Predicate("at-robby", x)
)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/dffa40b4-e037-4d69-bf48-098c3567b11e)

## Step: Our domain
```python
requirements = [Requirements.TYPING]
domain = Domain("ball_domain",
                requirements=requirements,
                types={"type_1": None},
                actions=[move])
print(domain_to_string(domain))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/9db4c287-08fc-46d3-aa8f-cab489ea00e6)

## References
- https://github.com/AI-Planning/pddl
- https://www.cs.toronto.edu/~sheila/2542/s14/A1/introtopddl2.pdf
