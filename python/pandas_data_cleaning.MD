# Pandas Data Preprocessing

This tutorial introduces four essential data preprocessing techniques in Pandas using a mocked DataFrame.

We begin with **Converters**, which enable the use of custom functions to handle specialised data transformation logic.

Next, the **Coerce** method is used to deal with invalid numeric values by converting them into a consistent representation (such as `NaN`), instead of allowing them to interrupt the data processing pipeline.

The **Replace** function is then applied for string cleaning through targeted value substitution.

Finally, we demonstrate how to combine separate datasets using the **Join** operation.

## Base dataframe

We start with a small, messy dataframe that will be reused throughout all sections. The goal is to progressively clean and enrich this dataset.

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
```

## 1. Example of a `Converter` to run a custom function

This approach uses a custom function to clean the `Price` column. It attempts to convert each value into a float, and replaces invalid entries with `NaN`, allowing the column to be safely used for numeric operations.

```python
# Doesn't work
df["Price"].dtype  # Returns dtype('O') (string)
df["Price"].mean()  # Error: cannot compute mean on strings

# Work
def my_converter(value):
    try:
        return float(value)
    except ValueError:
        return math.nan  # Avoid using 0 as it can distort analysis

df['Price'] = df['Price'].apply(my_converter)
df["Price"].dtype
df["Price"].mean()
```

## 2. Example of `coerce`

Here, the `Score` column is converted into numeric format using `errors='coerce'`. Any invalid values are automatically replaced with `NaN`, making this a concise alternative to custom cleaning functions.

```python
# Doesn't work
df['Score'] = pd.to_numeric(df['Score']) # ValueError: Unable to parse string "bad"

# Work
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
df['Score'].mean()
```

## 3. Example of `replace`

The `Revenue` column is cleaned by removing the `$` symbol before converting the values into floats. This is a common step when dealing with formatted financial data.

```python
# Doesn't work
df['Revenue'].mean()  # TypeError due to string values

# Work
df['Revenue'] = df['Revenue'].str.replace('$', '').astype(float)
df['Revenue'].mean()
```

## 4. Example of a `Join`

The `.join()` method combines the main dataframe with another dataframe by aligning a column (`date`) with the index of the second dataframe. This approach is efficient when the secondary dataset is already indexed by the key variable.

```python
# Create a secondary dataframe (e.g., weather)
weather = pd.DataFrame({
    'weather_date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
    'temperature': [30, 32, 29]
}).set_index('weather_date')

df.join(weather, on='date')
```
