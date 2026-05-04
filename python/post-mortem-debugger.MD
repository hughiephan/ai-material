# Using a post-mortem debugger

Let’s use the example of finding the “closest-point path” to illustrate how a post-mortem debugger works.

Unlike a normal debugger, where we set breakpoints before running the code, a post-mortem debugger lets us inspect the program *after it has already crashed*. While modern IDEs provide visual debugging tools, there are still cases where a command-driven post-mortem approach is useful for understanding what actually went wrong.

To demonstrate this, we’ll also introduce a couple of global and local variables (`random_value = 100` and `another_random_value = 200`) just to observe scope behavior during debugging.

```python
import math

random_value = 100  # global variable

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def find_closest(start_point, remaining_points):
    closest_point = remaining_points[0]
    for point in remaining_points[1:]:
        if distance(start_point, point) < distance(start_point, closest_point):
            closest_point = point
    return closest_point

def best_path(points):
    another_random_value = 200  # local variable
    current_point = points[0]
    remaining_points = points
    path = []
    
    while remaining_points != []:
        current_point = find_closest(current_point, remaining_points)
        path.append(current_point)
        remaining_points.remove(current_point)
        
    return path

delivery = [(1,1), (3,3), (2,2)]
```

Run the code once — it works:

```python
best_path(delivery)
```

Run it a second time — it crashes:

```python
best_path(delivery)
```

---

## Why does this happen?

Now we use a post-mortem debugger:

```
%debug
```

One useful command is `p` (print), which lets us inspect variables.

```
p random_value   # works fine → 100
```

If we are unsure where the issue is, we can move up the stack trace:

```
u   # go up to best_path(delivery)
```

Now let’s test variable scope.

```
p another_random_value
```

This fails — because we are *outside* the function where it was defined. `another_random_value` is a local variable, so it only exists while we are inside `best_path`.

So we move back down into the function context:

```
d
```

Now we try again:

```
p another_random_value   # now it works → 200
```

But we still haven’t found the bug.

Let’s inspect the data:

```
p points
```

We discover something important:

```
[]
```

The list is empty. That’s the root of the problem.

Also, make sure to stop the debugger using `exit`
```
exit
```

---

## What actually caused the crash?

The issue comes from this line:

```python
remaining_points.remove(current_point)
```

We are modifying the *original list in-place*. Since `remaining_points = points`, both variables point to the same list in memory. That means every `.remove()` call is also modifying the original `delivery` list.

So after the first run, the list gets emptied. On the second run, `delivery` is already empty, so `points[0]` crashes immediately. 

We can prove that it is empty by just running

```
delivery # And yes, it's showing the empty list
```

---

## How do we fix the problem, using `.copy()`?

Before we can do that, let’s demonstrate the difference between aliasing and copying.

### Aliasing (shared reference)

```python
a = [1, 2, 3]
b = a

id(a)
id(b)   # same object

a.remove(1)

a  # [2, 3]
b  # [2, 3] → unexpected side effect
```

Both variables point to the same list in memory, so changes affect both.

This is exactly what happened in `best_path`.

---

### Using `.copy()` (independent object)

```python
a = [1, 2, 3]
b = a.copy()

id(a)
id(b)   # different objects

a.remove(1)

a  # [2, 3]
b  # [1, 2, 3] → unchanged
```

Now `b` is a separate list in memory, so modifying `a` does not affect it.

---

So in the end, the post-mortem debugger allowed us to inspect the program after it failed, but the key takeaway comes from understanding the difference between shared references and copied objects in Python. From here, the responsibility shifts to you: make sure you understand how the algorithm behaves end-to-end, and apply .copy() appropriately to prevent unintended side effects and fix the issue.
