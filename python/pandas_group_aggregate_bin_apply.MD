# Pandas Essentials: Grouping, Aggregating, Binning, and Applying

This tutorial covers four fundamental Pandas operations using a single dataset. We will explore how to group data, calculate multiple statistics, bin continuous variables, and apply custom logic across rows and columns.

## The Dataset
We'll use a simplified version of a Titanic-style dataset. It contains three variables: **Age**, **Sex**, and **Survived** (where $1$ is "Yes" and $0$ is "No").

```python
import pandas as pd

df = pd.DataFrame({
    "Age": [5, 17, 25, 35, 45, 60, 70, 80],
    "Sex": ["male", "female", "female", "male", "female", "male", "male", "female"],
    "Survived": [0, 1, 1, 0, 1, 0, 0, 1]
})
```

️## Groupby + Mean: The Binary Insight
When you apply `.mean()` to a binary (0/1) column, the result is the **proportion of 1s**. This is a powerful shortcut for calculating survival rates or conversion rates.
```python
# Calculate survival rate by Sex
survival_rates = df.groupby("Sex")["Survived"].mean()
print(survival_rates)
```

> **🔍 Why it works:**
> If a group has survivors `[1, 1, 0, 0]`, the mean is $\frac{1+1+0+0}{4} = 0.5$. Thus, a mean of **0.5** equals a **50% survival rate**.


## Using `.aggregate()` for Multiple Statistics
Sometimes one metric isn't enough. The `.agg()` (or `.aggregate()`) method allows you to compute different statistics for different columns simultaneously.

### Standard Aggregation
```python
df.groupby("Sex").agg({
    "Age": ["min", "max", "mean"],
    "Survived": ["mean", "sum"]
})
```

### Named Aggregation (Recommended)
This approach keeps your column names clean and easy to read.
```python
summary = df.groupby("Sex").agg(
    avg_age=("Age", "mean"),
    oldest=("Age", "max"),
    survival_rate=("Survived", "mean"),
    total_survivors=("Survived", "sum")
)
```

## Using `cut()` + `groupby()`: Binning Data
Continuous data like **Age** can be noisy. `pd.cut()` allows you to group these values into meaningful categories (bins).

### Create Age Groups
```python
bins = [0, 18, 40, 65, 100]
labels = ["Child", "Young Adult", "Adult", "Senior"]

df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels)
```

### Multi-Level Grouping
You can now group by these new bins to see survival rates across demographics.
```python
# Survival rate by Sex AND Age Group
demographic_survival = df.groupby(["Sex", "AgeGroup"])["Survived"].mean()
```

## Using `.apply()`: Row vs. Column Logic
️
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
# 1. Create Bins
df["AgeGroup"] = pd.cut(df["Age"], bins=[0, 18, 40, 65, 100], 
                       labels=["Child", "Young Adult", "Adult", "Senior"])

# 2. Complex Grouping and Aggregation
final_report = df.groupby(["Sex", "AgeGroup"]).agg(
    avg_age=("Age", "mean"),
    survival_rate=("Survived", "mean"),
    count=("Survived", "count")
).dropna() # Remove empty bins if necessary

print(final_report)
```

### Key Takeaways
*   **Mean on 0/1:** Instantly gives you a percentage/proportion.
*   **`.agg()`:** Best for "Summary Tables" with specific column names.
*   **`pd.cut()`:** Best for turning numbers into categories.
