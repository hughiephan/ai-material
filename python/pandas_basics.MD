# Pandas basics

## 1. Understanding Series vs. DataFrames

A `Series` is a one-dimensional array (essentially a single column of data), whereas a `DataFrame` is a two-dimensional table made up of one or more Series. In this example, we create a standalone Series for ages and then incorporate it as a column into a larger DataFrame.

```python
import pandas as pd

number_series = pd.Series([20, 30, 40])

family = pd.DataFrame({
    "Name": ["Bob", "Charlie", "Bob"],
    "Age": number_series,
})
```

---

## 2. Series-Specific Methods vs. DataFrame Methods

Certain Pandas methods, such as `.unique()`, are designed to evaluate a single dimension of data. Because a Series represents a single column, `.unique()` works perfectly to find distinct values. However, applying it directly to a two-dimensional DataFrame will trigger an error since the method doesn't know which column to evaluate.

```python
type(family["Name"])              # Series
family["Name"].unique()           # Good

type(family)                      # Dataframe            
family.unique()                   # Show error
```

---

## 3. Creating Boolean Masks for Conditions

When you apply a logical operator (like `>`) to a Pandas column, it evaluates that condition for every single row. The result is a "boolean mask"—a new Series made entirely of `True` and `False` values that indicate whether each specific row met your criteria.

```python
family["Age"] > 25   # or could use family.Age > 25 with similar output

# Output:
# 0    False
# 1     True
# 2     True
```

---

## 4. Filtering DataFrames Using Boolean Masks

Once you have a boolean mask (the `True`/`False` condition from the previous step), you can pass it directly into the DataFrame's brackets `[]`. Pandas will filter the dataset, returning a new DataFrame containing only the rows where the condition is `True`.

```python
family[family["Age"] > 25]
```

---

## 5. Distinguishing Between `type()` and `.dtype`

It is important to understand the difference between the container and its contents. The standard Python `type()` function returns the high-level object class (telling you it is a Pandas Series). The Pandas `.dtype` attribute tells you the specific data type of the actual values stored inside that Series (like 64-bit integers).

* **`type()`** → object type (the container/whole object)
* **`dtype`** → data type (the values inside)

```python
type(family["Age"]) # pandas Series
family["Age"].dtype # int64
```

---

## 6. Accessing Data: Label-Based (`.loc`) vs. Position-Based (`.iloc`)

Pandas offers two primary indexers for selecting specific rows and columns. `.loc` is used when you want to look up data by its explicit index *label* (e.g., a specific string like "Bob"). `.iloc` is used when you want to look up data by its underlying integer *position* (e.g., the very first row at index 0).

```python
family_with_name_index = family.set_index("Name")
family_with_name_index

family_with_name_index.loc["Bob"]  # Label-based
family_with_name_index.iloc[0]     # Position-based
```

---

## 7. Slicing Data with the Colon (`:`) Operator

The colon (`:`) is a slicing operator that lets you select a range of data rather than just a single value. When used with `.iloc`, it can fetch a range of positions (like the first two rows). When used with `.loc`, a lone colon means "select all rows," allowing you to then specify exactly which columns you want to extract alongside them.

```python
family.iloc[:2]          # first 2 rows
family.loc[:, ["Age"]]   # all rows, Age column  
```
