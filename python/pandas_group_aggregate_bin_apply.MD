# Pandas Essentials: Grouping, Aggregating, Binning, and Applying

We will explore how to group data, aggregation methods like mean, cutting values into bins, and the apply method.

## Dataset

Firstly, we'll use a simplified version of a Titanic-style dataset as an example (most of the time, you would work with a .csv file). It contains three variables: **Age**, **Sex**, and **Survived** (where 1 is "Survived" and 0 is "Dead").

```python
import pandas as pd

df = pd.DataFrame({
    "Age": [10, 22, 34, 58, 75],
    "Sex": ["male", "female", "female", "male", "female"],
    "Survived": [0, 1, 1, 1, 1]
})
```

## Groupby, Apply, and Mean

Let's calculate the survival rate of males and females on the Titanic.

```python
# Run the group by with the two columns: sex and survived
df.groupby("Sex")["Survived"] # Returning a SeriesGroupBy 

# Print the result out with the apply method
df.groupby("Sex")["Survived"].apply(print) 

# There are other built-in methods, like calculating the mean of survival rates.
df.groupby("Sex")["Survived"].mean()
```

## Using `.aggregate()`

Sometimes one metric isn't enough. The `.agg()` (or `.aggregate()`) method allows you to compute different statistics for different columns simultaneously.

```python
df.groupby("Sex").agg({
    "Age": ["min", "max"],  # Let's find out about the minimum and maximum age for males and females in the data
    "Survived": ["mean", "sum"]  # And survival rate through the mean and counting for male and female in the data
})
```

## Using `cut()` + `groupby()` to bin data

Continuous data like **Age** can be noisy. With a small dataset, fewer bins work better.

### Create Simpler Age Groups

For example, we don't show by age but by groups of age, let's say Young and Old. Young is from 0 to 40, and Old Age is between 40 and 100

```python
bins = [0, 40, 100]   # This will create 2 bins of 0 to 40, and 40 to 100
labels = ["Young", "Old"]   # With the 2 bins above, we label them as young and old

df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels)
df
```

## Using `.apply()`: Row vs. Column Logic

The `.apply()` method is the "Swiss Army Knife" of Pandas, but the `axis` parameter is crucial.

### Axis = 1 (Row-wise)

Use this when your logic depends on **multiple columns** within the same row.

```python
def risk_level(row):
    return "High" if row["Age"] > 60 else "Low"

df["Risk"] = df.apply(risk_level, axis=1)
```

### Axis = 0 (Column-wise)

Use this to apply a function across the **entire column**.

```python
# Calculate the mean for specific numeric columns
column_means = df[["Age", "Survived"]].apply(lambda col: col.mean(), axis=0)
```

### Apply with Groupby

You can also apply complex custom logic to entire groups.

```python
def survival_percentage(group):
    # Custom calculation: sum of survivors divided by group size
    return group["Survived"].sum() / len(group)

group_logic = df.groupby("Sex").apply(survival_percentage)
```

---

## Summary: Putting It All Together

This final snippet combines all the concepts into one clean workflow:

```python
# 1. Create Simpler Bins
df["AgeGroup"] = pd.cut(df["Age"], bins=[0, 40, 100], 
                       labels=["Young", "Old"])

# 2. Complex Grouping and Aggregation
final_report = df.groupby(["Sex", "AgeGroup"]).agg(
    avg_age=("Age", "mean"),
    survival_rate=("Survived", "mean"),
    count=("Survived", "count")
).dropna()

print(final_report)
```
