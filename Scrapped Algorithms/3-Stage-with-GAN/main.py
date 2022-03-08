import pandas as pd
import numpy as np

def histogram_intersection(a, b):
    v = np.minimum(a, b).sum().round(decimals=1)
    return v
df = pd.DataFrame([([0, 1], 3, 0.2), ([0, 2], 4, 0.553), ([0, 3], 5, 0.22), ([0, 4], 6, 0.9)],
                  columns=['a', 'b', 'c'])

# df.to_csv('out.csv')
# print(df.head())
# corr = df.corr().abs()
# print(corr)
# upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
# to_drop = [column for column in upper.columns if any(upper[column] > 0.75)]
# print(to_drop)

data = 'out.csv'

x = np.loadtxt(data, skiprows=1, delimiter=',',
              unpack=True)

np.corrcoef(x)