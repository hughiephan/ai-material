# Pandas Essentials: Grouping, Aggregating, Binning, and Applying

We will go through how to group data, use aggregation functions such as mean, divide continuous values into bins, and apply custom functions.

## Dataset

To begin, we’ll use a simplified Titanic-like dataset as an example (in practice, you would usually load data from a `.csv` file). The dataset includes three columns: **Age**, **Sex**, and **Survived** (where 1 indicates survival and 0 indicates death).

```python
import pandas as pd

df = pd.DataFrame({
    "Age": [10, 22, 34, 58, 75],
    "Sex": ["male", "female", "female", "male", "female"],
    "Survived": [0, 1, 1, 1, 1]
})
```

## `Groupby`, `Apply`, and `Mean`

Now, let’s compute the survival rate for males and females.

```python
# Group data by the "Sex" column and select "Survived"
df.groupby("Sex")["Survived"] # Returns a SeriesGroupBy object

# Display each group using apply
df.groupby("Sex")["Survived"].apply(print) 

# You can also use built-in functions such as mean to calculate survival rates
df.groupby("Sex")["Survived"].mean()
```

## Using `.aggregate()`

In many cases, a single metric is not sufficient. The `.agg()` (or `.aggregate()`) method allows you to calculate multiple statistics across different columns at once.

```python
df.groupby("Sex").agg({
    "Age": ["min", "max"],  # Compute the minimum and maximum ages for each group
    "Survived": ["mean", "sum"]  # Compute survival rate (mean) and total survivors (sum)
})
```

## Using `cut()` + `groupby()` to bin data

Continuous variables like **Age** can be overly detailed. For small datasets, it’s often better to group values into broader categories. Here, we create simple age groups.

Instead of analyzing exact ages, we divide them into categories: Young (0–40) and Old (40–100).

```python
bins = [0, 40, 100]   # Defines two intervals: 0–40 and 40–100
labels = ["Young", "Old"]   # Assign labels to each interval

df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels)
```

## Advanced `.apply`

Previously, `.apply` was used just to display results, but it can also handle more complex, custom computations on each group.

```python
def survival_percentage(group):
    # Calculate survival rate: number of survivors divided by total group size
    return group["Survived"].sum() / len(group)

df.groupby("Sex").apply(survival_percentage) 
```

From the result, you’ll notice this gives the same output as the mean. This approach becomes useful when a built-in function does not directly support your required calculation.
