# Pandas Data Cleaning & Joining (Custom DataFrames)

This tutorial demonstrates 5 core Pandas techniques using manually created datasets:

1. Converter (custom cleaning function)
2. Coerce (handling invalid numeric values)
3. Replace (string cleaning)
4. Join (combining datasets using index)
5. Merge (combining datasets using columns)

---

## 1. Example of a Converter (Custom Function)

This approach mimics the behavior of `converters` in `read_csv` by manually applying a function to clean values after the DataFrame is created. It is particularly useful when working with already-loaded or synthetic data. The custom function attempts to convert values into floats, and if it encounters invalid entries (such as text), it safely replaces them with `NaN`, preventing downstream errors in analysis.

```python
import pandas as pd
import math

# Create a messy dataset
data = pd.DataFrame({
    'Product': ['A', 'B', 'C', 'D'],
    'Price': ['10.5', '20.0', 'invalid', '15.2']
})

# Custom converter
def my_converter(value):
    try:
        return float(value)
    except ValueError:
        return math.nan

# Apply converter
data['Price_clean'] = data['Price'].apply(my_converter)

data
```

---

## 2. Example of `coerce`

Using `errors='coerce'` in `pandas.to_numeric()` provides a concise and efficient way to handle invalid numeric values. Instead of raising errors when encountering non-numeric entries, Pandas automatically converts them into `NaN`. This method is generally preferred for quick cleaning tasks because it avoids the need for custom functions while remaining highly readable.

```python
df = pd.DataFrame({
    'Score': ['85', '90', 'bad', '70']
})

df['Score_numeric'] = pd.to_numeric(df['Score'], errors='coerce')

df
```

---

## 3. Example of `replace`

String cleaning is often necessary when numeric values are stored with additional formatting characters, such as currency symbols. The `.str.replace()` method removes these unwanted characters, making the data suitable for type conversion. Once cleaned, the column can be safely converted into a numeric type, enabling further analysis.

```python
df = pd.DataFrame({
    'Revenue': ['$1000', '$2500', '$1800']
})

# Remove '$' and convert
df['Revenue'] = df['Revenue'].str.replace('$', '')
df['Revenue'] = df['Revenue'].astype(float)

df
```

---

## 4. Example of a Join

The `.join()` method combines DataFrames by aligning a column from one DataFrame with the index of another. This is particularly efficient for time-series or indexed data where one dataset is naturally keyed by an index (such as dates). By setting the index appropriately, `.join()` provides a clean and fast way to enrich one dataset with additional features from another.

```python
sales = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
    'sales': [100, 150, 200]
})

weather = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
    'temperature': [30, 32, 29]
})

# Set index for join
weather = weather.set_index('date')

# Perform join
combined_join = sales.join(weather, on='date')

combined_join
```

---

## 5. Example of a Merge

The `.merge()` method is a more general and flexible way to combine DataFrames by matching values across columns rather than relying on index alignment. It supports a variety of join types (inner, left, right, outer) and is ideal when working with relational-style data where keys exist as regular columns in both datasets.

```python
sales = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
    'sales': [100, 150, 200]
})

weather = pd.DataFrame({
    'date': pd.to_datetime(['2026-01-01', '2026-01-02', '2026-01-03']),
    'temperature': [30, 32, 29]
})

# Perform merge
combined_merge = sales.merge(weather, on='date')

combined_merge
```
