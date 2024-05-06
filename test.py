import pandas as pd
import numpy as np
import matplotlib as mpl

# Sample DataFrame
data = {"Product": ["A", "B", "C"], "Unit Price": [10.5, 20.75, 15.99]}

df = pd.DataFrame(data)

# Format 'Unit Price' column as currency
df["Unit Price"] = df["Unit Price"].map("${:,.2f}".format)

print(df)
