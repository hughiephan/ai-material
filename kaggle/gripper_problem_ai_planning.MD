# Gripper Problem with AI Planning

There is a robot that can move between two rooms and pick up or drop balls with either of his two arms. Initially, all balls and the robot are in room A. We want the 4 balls to be in room B. We will apply AI Planning to solve this problem. You can find the full explanation on Medium: Hughie Phan - Gripper Problem with AI Planning.

![image](https://github.com/hughiephan/DPL/assets/16631121/f95d71b8-0b59-4681-bd59-039b60fa521f)

```python
!pip install git+https://github.com/AI-Planning/pddl.git
from pddl.logic import Predicate, constants, variables
from pddl.logic.base import And
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
```

```python
rooma, roomb, ball1, ball2, ball3, ball4, left, right = constants("rooma roomb ball1 ball2 ball3 ball4 left right")
x, y, z = variables("x y z")
predicates = [
    Predicate("ROOM", x),
    Predicate("BALL", x),
    Predicate("GRIPPER", x),
    Predicate("at-robby", x),
    Predicate("at-ball", x, y),
    Predicate("free", x),
    Predicate("carry", x, y),
]
init = [
    Predicate("ROOM", rooma),
    Predicate("ROOM", roomb),
    Predicate("BALL", ball1),
    Predicate("BALL", ball2),
    Predicate("BALL", ball3),
    Predicate("BALL", ball4),
    Predicate("GRIPPER", left),
    Predicate("GRIPPER", right),
    Predicate("free", left),
    Predicate("free", right),
    Predicate("at-robby", rooma),
    Predicate("at-ball", ball1, rooma),
    Predicate("at-ball", ball2, rooma),
    Predicate("at-ball", ball3, rooma),
    Predicate("at-ball", ball4, rooma),
]
goal = And(
    Predicate("at-ball", ball1, roomb),
    Predicate("at-ball", ball2, roomb),
    Predicate("at-ball", ball3, roomb),
    Predicate("at-ball", ball4, roomb),
)
```

```python
rooma, roomb, ball1, ball2, ball3, ball4, left, right = constants("rooma roomb ball1 ball2 ball3 ball4 left right")
x, y, z = variables("x y z")
predicates = [
    Predicate("ROOM", x),
    Predicate("BALL", x),
    Predicate("GRIPPER", x),
    Predicate("at-robby", x),
    Predicate("at-ball", x, y),
    Predicate("free", x),
    Predicate("carry", x, y),
]
init = [
    Predicate("ROOM", rooma),
    Predicate("ROOM", roomb),
    Predicate("BALL", ball1),
    Predicate("BALL", ball2),
    Predicate("BALL", ball3),
    Predicate("BALL", ball4),
    Predicate("GRIPPER", left),
    Predicate("GRIPPER", right),
    Predicate("free", left),
    Predicate("free", right),
    Predicate("at-robby", rooma),
    Predicate("at-ball", ball1, rooma),
    Predicate("at-ball", ball2, rooma),
    Predicate("at-ball", ball3, rooma),
    Predicate("at-ball", ball4, rooma),
]
goal = And(
    Predicate("at-ball", ball1, roomb),
    Predicate("at-ball", ball2, roomb),
    Predicate("at-ball", ball3, roomb),
    Predicate("at-ball", ball4, roomb),
)
```

```python
pickup = Action(
    "pickup",
    parameters=[x, y, z],
    precondition=Predicate("BALL", x) 
               & Predicate("ROOM", y) 
               & Predicate("GRIPPER", x)
               & Predicate("at-ball", x, y)
               & Predicate("at-robby", y)
               & Predicate("free", z),
    effect=Predicate("carry", z, x) 
        & ~Predicate("at-ball", x, y)
        & ~Predicate("free", z),
)

move = Action(
    "move",
    parameters=[x, y],
    precondition=Predicate("ROOM", x) 
               & Predicate("ROOM", y) 
               & Predicate("at-robby", x),
    effect=Predicate("at-robby", y) 
        & ~Predicate("at-robby", x)
)

drop = Action(
    "drop",
    parameters=[x, y, z],
    precondition=Predicate("BALL", x)
               & Predicate("ROOM", y) 
               & Predicate("GRIPPER", z)
               & Predicate("carry", z, x)
               & Predicate("at-robby", y),
    effect=Predicate("at-ball", x, y) 
        & Predicate("free", z)
        & ~Predicate("carry", z, x),
)
```

```python
domain = Domain("ball_gripper_domain",
                requirements='',
                predicates=predicates,
                constants=[rooma, roomb, ball1, ball2, ball3, ball4, left, right],
                actions=[move,pickup,drop])
print(domain_to_string(domain))
```

```python
problem = Problem(
    "ball_gripper_problem",
    domain=domain,
    requirements='',
    objects=[rooma, roomb, ball1, ball2, ball3, ball4, left, right],
    init=init,
    goal=goal,
)
print(problem_to_string(problem))
```
