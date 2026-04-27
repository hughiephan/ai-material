# Pandas Data Preprocessing

This tutorial demonstrates 4 core Pandas data preprocessing techniques using a mocked dataframe:

1. Converter (custom cleaning function)
2. Coerce (handling invalid numeric values)
3. Replace (string cleaning)
4. Join (combining dataframes using an index)

---

## Base dataframe

We start with a small, messy dataframe that we will reuse across all sections. We will progressively clean and enrich this dataframe.

```python
import pandas as pd
import math

df = pd.DataFrame({
    'Product': ['A', 'B', 'C'],
    'Price': ['10.5', 'invalid', '15.2'],
    'Revenue': ['$1000', '$2500', '$1800'],
    'Score': ['85', 'bad', '70'],
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03'])
})

df["Price"].dtype # Return dtype('O') which is string
df["Price"].mean() # This will give us error since it cannot work on string
```

---

## 1. Example of a Converter (Custom Function)

This approach applies a custom function to clean the `Price` column. It attempts to convert values into floats and replaces invalid entries with `NaN`, ensuring the column becomes usable for numeric analysis without breaking the workflow.

```python
def my_converter(value):
    try:
        return float(value)
    except ValueError:
        return math.nan

df['Price_clean'] = df['Price'].apply(my_converter)

df
```

---

## 2. Example of `coerce`

Here, we convert the `Score` column into numeric values using `errors='coerce'`. Any invalid value is automatically replaced with `NaN`, making this an alternative to writing custom cleaning logic.

```python
df['Score_numeric'] = pd.to_numeric(df['Score'], errors='coerce')

df
```

---

## 3. Example of `replace`

We clean the `Revenue` column by removing the `$` symbol and then converting the values into floats. This step is common when working with formatted financial data.

```python
df['Revenue_clean'] = df['Revenue'].str.replace('$', '').astype(float)

df
```

---

## 4. Example of a Join

The `.join()` method is used to combine the main dataframe with another dataframe by matching a column (`date`) with the index of another DataFrame. This is efficient when the secondary dataframe is indexed by the key variable.

```python
# Create a secondary dataframe (e.g., weather)
weather = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
    'temperature': [30, 32, 29]
}).set_index('date')

# Join
df_joined = df.join(weather, on='date')

df_joined
```
