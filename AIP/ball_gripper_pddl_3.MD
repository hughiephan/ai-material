# Build Ball Gripper with PDDL 3.1 Lirabry

There is a robot that can move between two rooms and pick up or drop balls with either of
his two arms. Initially, all balls and the robot are in the first room. We want the balls to be in
the second room.

## Step 1: Import libraries
```python
!pip install git+https://github.com/AI-Planning/pddl.git
from pddl.logic import Predicate, constants, variables
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements
```

## Step 2: Move Action
```python
move = Action(
    "move",
    parameters=[x, y],
    precondition=Predicate("ROOM", x) 
               & Predicate("ROOM", y) 
               & Predicate("at-robby", x),
    effect=Predicate("at-robby", y) 
        & ~Predicate("at-robby", x)
)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/dffa40b4-e037-4d69-bf48-098c3567b11e)

## Step: Grip Action
```python
grip = Action(
    "grip",
    parameters=[x, y, z],
    precondition=Predicate("BALL", x) 
               & Predicate("ROOM", y) 
               & Predicate("GRIPPER", x)
               & Predicate("at-ball", x, y)
               & Predicate("at-robby", y)
               & Predicate("free", z),
    effect=Predicate("carry", z, x) 
        & ~Predicate("at-robby", x, y)
        & ~Predicate("free", z),
)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/ed7adf6b-a649-472b-b444-87ec3246731f)


## Step: Our domain
```python
requirements = [Requirements.TYPING]
domain = Domain("ball_domain",
                requirements=requirements,
                types={"type_1": None},
                actions=[move,grip])
print(domain_to_string(domain))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/723ca674-28c7-4609-bedc-97001bcaeb2d)

## References
- https://github.com/AI-Planning/pddl
- https://www.cs.toronto.edu/~sheila/2542/s14/A1/introtopddl2.pdf
