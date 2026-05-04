
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




