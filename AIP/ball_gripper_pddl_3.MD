# Ball Gripper with PDDL 3.1 Lirabry

There is a robot that can move between two rooms and pick up or drop balls with either of
his two arms. Initially, all balls and the robot are in the first room. We want the balls to be in
the second room.

![image](https://github.com/hughiephan/DPL/assets/16631121/db79dd5d-ff74-4c28-a222-174f23fd0a50)

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

## Step 3: Objects

![image](https://github.com/hughiephan/DPL/assets/16631121/16b95955-88ed-46c8-b79d-ec4903076a50)

```python
rooma, roomb, ball1, ball2, ball3, ball4, left, right = constants("rooma roomb ball1 ball2 ball3 ball4 left right")
objects = [
    rooma, roomb,
    ball1, ball2, ball3, ball4,
    left, right,
]
```

## Step 4: Predicates

![image](https://github.com/hughiephan/DPL/assets/16631121/af7f54d8-64ef-4d83-a197-4ad1b1db63c5)

```python
predicates = [
    Predicate("ROOM", x),
    Predicate("BALL", x),
    Predicate("GRIPPER", x),
    Predicate("at-robby", x),
    Predicate("at-ball", x, y),
    Predicate("free", x),
    Predicate("carry", x, y),
]
```

## Step 5: Initial State
![image](https://github.com/hughiephan/DPL/assets/16631121/6fd7aa56-2651-496b-b0bb-0bf24a97865d)

```python
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
```

## Step 6: Goal specification
```python
goal = [
    Predicate("at-ball", ball1, roomb),
    Predicate("at-ball", ball2, roomb),
    Predicate("at-ball", ball3, roomb),
    Predicate("at-ball", ball4, roomb),
]
```

## Step 7: Move Action

![image](https://github.com/hughiephan/DPL/assets/16631121/dffa40b4-e037-4d69-bf48-098c3567b11e)

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

## Step 8: Pickup Action
![image](https://github.com/hughiephan/DPL/assets/16631121/ed7adf6b-a649-472b-b444-87ec3246731f)

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
```

## Step 9: Drop Action

![image](https://github.com/hughiephan/DPL/assets/16631121/21989be2-981a-4579-8307-1c2e5662ae59)

```python
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

## Step 10: Ball gripper domain
```python
domain = Domain("ball_gripper_domain",
                requirements='',
                predicates=predicates,
                constants=objects,
                actions=[move,pickup,drop])
print(domain_to_string(domain))
```

Output of domain_to_string(domain), but before inputting into solver, we need to remove the line with `(:types)` because PDDL 3.1 Library does not support empty types.
```
(define (domain ball_gripper_domain)
    (:types)    <------- Remove this before input into planner
    (:constants ball1 ball2 ball3 ball4 left right rooma roomb)
    (:predicates (BALL ?x)  (GRIPPER ?x)  (ROOM ?x)  (at-ball ?x ?y)  (at-robby ?x)  (carry ?x ?y)  (free ?x))
    (:action drop
        :parameters (?x ?y ?z)
        :precondition (and (BALL ?x) (ROOM ?y) (GRIPPER ?z) (carry ?z ?x) (at-robby ?y))
        :effect (and (at-ball ?x ?y) (free ?z) (not (carry ?z ?x)))
    )
     (:action move
        :parameters (?x ?y)
        :precondition (and (ROOM ?x) (ROOM ?y) (at-robby ?x))
        :effect (and (at-robby ?y) (not (at-robby ?x)))
    )
     (:action pickup
        :parameters (?x ?y ?z)
        :precondition (and (BALL ?x) (ROOM ?y) (GRIPPER ?x) (at-ball ?x ?y) (at-robby ?y) (free ?z))
        :effect (and (carry ?z ?x) (not (at-ball ?x ?y)) (not (free ?z)))
    )
)
```

## Step 11: Ball gripper problem
```python
problem = Problem(
    "ball_gripper_problem",
    domain=domain,
    requirements='',
    objects=objects,
    init=init,
    goal=goal,
)
print(problem_to_string(problem))
```

We need to make some adjustment to the `:goal` of output problem, because the PDDL 3.1 Library does not support multiple goals yet. So, we have to replace the first line with second line.
```
(:goal [Predicate(at-ball, ball1, roomb), Predicate(at-ball, ball2, roomb), Predicate(at-ball, ball3, roomb), Predicate(at-ball, ball4, roomb)])       <--------- Replace this line...

(:goal (and (at-ball ball1 roomb) (at-ball ball2 roomb) (at-ball ball3 roomb) (at-ball ball4 roomb)))        <----- ...with this line.
```

Here is the final definition of our problem:
```
(define (problem ball_gripper_problem)
    (:domain ball_gripper_domain)
    (:objects ball1 ball2 ball3 ball4 left right rooma roomb)
    (:init (BALL ball1) (BALL ball2) (BALL ball3) (BALL ball4) (GRIPPER left) (GRIPPER right) (ROOM rooma) (ROOM roomb) (at-ball ball1 rooma) (at-ball ball2 rooma) (at-ball ball3 rooma) (at-ball ball4 rooma) (at-robby rooma) (free left) (free right))
    (:goal (and (at-ball ball1 roomb) (at-ball ball2 roomb) (at-ball ball3 roomb) (at-ball ball4 roomb)))
)
```

## Step 12: Solve
Try to solve with https://editor.planning.domains . But the planner proved that it's impossible to reach the goal. "Simplified" means it didn't even need to search.

![image](https://github.com/hughiephan/DPL/assets/16631121/64dd5a2f-8e06-41ce-91ef-578c8c18bbe6)

## References
- PDDL Python Library from AI-Planning 
- Malte Helmert from Computer Science Unversity of Toronto (An Introduction to PDDL)
- https://stackoverflow.com/questions/74158344/exploration-program-goal-returning-as-false-not-sure-what-to-do-next
