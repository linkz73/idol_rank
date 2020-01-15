import pandas as pd
df33 = pd.DataFrame({"c1": [1, 2], "c2": [11, 22]}, index=["i1", "i2"])
print(df33)

df33.index.name = "idx"
print(df33)

df33 = df33.set_index("c1")
print(df33)


