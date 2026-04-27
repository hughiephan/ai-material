# Pandas Data Cleaning & Joining

This tutorial demonstrates 5 core Pandas techniques using a mocked dataframe:

1. Converter (custom cleaning function)
2. Coerce (handling invalid numeric values)
3. Replace (string cleaning)
4. Join (combining datasets using an index)
5. Merge (combining datasets using columns)

---

## Base Dataset

We start with a small, messy dataset that we will reuse across all sections. We will progressively clean and enrich this dataset.

```python
import pandas as pd
import math

df = pd.DataFrame({
    'Product': ['A', 'B', 'C', 'D'],
    'Price': ['10.5', '20.0', 'invalid', '15.2'],
    'Revenue': ['$1000', '$2500', '$1800', '$2200'],
    'Score': ['85', '90', 'bad', '70'],
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04'])
})

df
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

Here, we convert the `Score` column into numeric values using `errors='coerce'`. Any invalid value is automatically replaced with `NaN`, making this a concise and efficient alternative to writing custom cleaning logic.

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

The `.join()` method is used to combine the main dataset with another dataset by matching a column (`date`) with the index of another DataFrame. This is efficient when the secondary dataset is indexed by the key variable.

```python
# Create a secondary dataset (e.g., weather)
weather = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04']),
    'temperature': [30, 32, 29, 31]
}).set_index('date')

# Join
df_joined = df.join(weather, on='date')

df_joined
```

---

## 5. Example of a Merge

The `.merge()` method combines datasets by matching columns directly rather than relying on index alignment. It is more flexible and works well when both datasets store their keys as regular columns.

```python
# Reset weather index for merge
weather_reset = weather.reset_index()

# Merge
df_merged = df.merge(weather_reset, on='date')

df_merged
```
