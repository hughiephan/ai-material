## Python Practicals: Working with Lists

---

### 🔹 What is a List?

A **list in Python** is basically a container that holds multiple items in order.

---

### 🔹 Examples of Lists

#### List containing numbers

```python
our_list = [10, 20, 30, 40, 50]
print(type(our_list))
our_list
```

#### List containing strings

```python
our_list = ['cat', 'dog', 'tiger']  # strings use quotation marks
```

#### List containing other lists (nested list)

```python
our_list = [[1, 2], [3, 4, 5]]
```

#### Empty list

```python
our_list = []
```

#### List with mixed data types

```python
our_list = [10, 20, 30, [1, 2], 'cat']
```

---

### 🔹 Indexing in Lists

Lists start from index **0**:

```python
# id:         0   1   2     3      4
our_list = [10, 20, 30, [1, 2], 'cat']
```

Accessing elements:

```python
our_list[0]
```

---

### 🔹 Negative Indexing

Lists also support negative indexing:

```python
# idn:       -5   -4  -3  -2     -1
# id:         0    1   2   3      4
our_list = [10, 20, 30, [1, 2], 'cat']
```

Accessing elements:

```python
our_list[-1]
```

---

### 🔹 Slicing Lists

To get multiple values at once, use the colon `:` operator:

```python
# (start index : up to but not including stop)

our_list[2:4]
our_list[2:5]
our_list[2:-1]
our_list[2:]  # defaults to the last element
```

---

### 🔹 Built-in Functions

Lists have many useful built-in functions:

```python
dir(our_list)
help(our_list.append)
```

> In Python, everything is an object (e.g., integers, strings, lists).

---

### 🔹 Modifying Lists

#### Append an element

```python
our_list.append('dog')
our_list
```

#### Remove an element using pop

```python
dir(our_list)
help(our_list.pop)

our_list.pop(3)  # popped out value
our_list         # updated list
```

---

### 🔹 Practice Tip

In the exercises, try using other built-in functions such as:

* `sort()` → to reorder elements
* `reverse()` → to reverse the list

Exploring these functions will help you better understand how lists work.
