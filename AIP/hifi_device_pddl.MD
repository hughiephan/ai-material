# HIFI Devices PDDL

## Step:
```python
!pip install git+https://github.com/AI-Planning/pddl.git
from pddl.logic import Predicate, constants, variables
from pddl.logic.base import And
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
```

## Step: 
```python
cable, cableporta, cableportb, device, deviceport = constants("cable cableporta cableportb device deviceport")
x, y, z, w = variables("x y z w")

predicates = [
    Predicate("free", x),
    Predicate("connected", x, y),
    Predicate("compatible", x, y),
]

init = [
    Predicate("CABLE", cable),
    Predicate("CABLEPORT", cableporta),
    Predicate("CABLEPORT", cableportb),
    Predicate("DEVICE", device),
    Predicate("DEVICEPORT", deviceport),
    Predicate("free", cableporta),
    Predicate("free", cableportb),
    Predicate("free", deviceport),
]

plugIn = Action(
    "plugIn",
    parameters=[x, y],
    precondition=Predicate("free", x) 
               & Predicate("free", y)
               & Predicate("compatible", x, y),
    effect=Predicate("connected", x, y) 
        & ~Predicate("free", x)
        & ~Predicate("free", y),
)

domain = Domain("hifi_devices_domain",
                requirements='',
                predicates=predicates,
                constants=[cable, cableporta, cableportb, device, deviceport],
                actions=[plugIn])
print(domain_to_string(domain))
```

## References
- ...
