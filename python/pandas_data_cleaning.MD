# 🐼 Pandas Data Cleaning & Joining (Custom DataFrames)

This tutorial demonstrates 4 core Pandas techniques using **manually created datasets**:

1. Converter (custom cleaning function)
2. Coerce (handling invalid numeric values)
3. Replace (string cleaning)
4. Join (combining datasets)

---

## 📌 1. Example of a Converter (Custom Function)

Instead of using `read_csv`, we simulate messy data and apply a converter manually.

### Example

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

### 💡 Explanation

* We mimic `converters` by using `.apply()`
* Invalid values (`"invalid"`) become `NaN`
* Useful when data is already loaded

---

## 📌 2. Example of `coerce`

### Example

```python
df = pd.DataFrame({
    'Score': ['85', '90', 'bad', '70']
})

df['Score_numeric'] = pd.to_numeric(df['Score'], errors='coerce')

df
```

### 💡 Explanation

* `"bad"` → automatically converted to `NaN`
* Much faster than writing a custom function
* Best for quick cleaning

---

## 📌 3. Example of `replace`

### Example

```python
df = pd.DataFrame({
    'Revenue': ['$1000', '$2500', '$1800']
})

# Remove '$' and convert
df['Revenue'] = df['Revenue'].str.replace('$', '')
df['Revenue'] = df['Revenue'].astype(float)

df
```

### 💡 Explanation

* Removes unwanted symbols
* Converts cleaned strings into numeric values
* Common in financial datasets

---

## 📌 4. Example of a Join

### Step 1: Create Two DataFrames

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
```

---

### Step 2: Join

```python
combined = sales.join(weather, on='date')

combined
```

### 💡 Explanation

* Matches `sales['date']` with `weather.index`
* Adds temperature to each sales record

---

### 🔁 Alternative: Merge

```python
combined = sales.merge(weather, on='date')
```

### 💡 Explanation

* More flexible than `join`
* Works even if no index is set

