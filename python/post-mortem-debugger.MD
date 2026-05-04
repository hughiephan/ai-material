
# Using a post morterm debugger

Let's use the example of finding the "closet-point path" to help us illustrate the post morterm debugger.

Unlike the normal debugger where we have to set break points, the post morterm debugger allows us to run the debugging process directly after the code has crashed. The usual debugger even though is a modern, visual interface or a quick, sometimes there are use cases for a command-driven approach for post-mortem analysis.

To illustrate the use of post morterm debugger, I'll also add some global random_value and another_random value of a 100 and 200

```python
import math

random_value = 100  # Random Global variable

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def find_closest(start_point, remaining_points):
    closest_point = remaining_points[0]
    for point in remaining_points[1:]:
        if distance(start_point, point) < distance(start_point, closest_point):
            closest_point = point
    return closest_point

def best_path(points):
    another_random_value = 200  # Random Local variable
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

Run the code once, it works
```python 
best_path(delivery)
```

Run the code a second time, it crashes.
```python 
best_path(delivery)
```

Why does that happen? We could first run the %debug, and it will show us the exact location that the error happens.
```
%debug
```

One useful method is p which short for print, and I want to see the values of the variables in the code, so let's print out the random global value we add earlier.
```
p random_value # We can see it still works fine and giving us the result of 100
```

So let's pretend we are not sure where the problems are, we can use the u which stands for up to go to the original function that call to the function that has the error
```
u # we are now at the best_path(delivery)
```

Remeber the second random value we added earlier, let's see if we can still access it
```
p another_random_value # So it doesn't work now, it's because we are outside of the function best_path. And the value is a local one, and can only be access when we are inside the function
```

So let's now go back into the best_path function, we can use the d which stand for down to go into it
```
p another_random_value # Good, it shows us the error now since we are inside the function and we can access all the local variables of that function
```

But we still haven't found the error, let's try to print out some other things. We can see that the points[0] is trying to access the first value in the points list, so let's see what the list of the points contain
```
p points # Hhmm this returned empty list [], this probably is the culprit
```

To show case the exact problem, this would becoming from the .remove function. Since we gives the list and the list is ran succuessfully for the best_path function call, but after that finishes, it clears the whole list. That's why in the second run you wouldn't be able to run it since the delivery is essentially empty before the algorithm can process it.
```
remaining_points.remove(current_point)
```

So for that you could use a .copy() to ... (please explain why copy helps).

```
a = [1,2,3]  # Initialize the list of 1, 2,3
b = a        # Let's assign the a to b
id(a)        # Let's check the id of a 
id(b)        # Let's check the id of b, oh they are similar
a.remove(1)  # So let's run the remove the 1 value out of the list
a            # a has the 1 removed
b            # oh, b also has the 1 removed, we don't want that to happens as it would be quite similar to the best path function issue earlier
```

So what we can do is



