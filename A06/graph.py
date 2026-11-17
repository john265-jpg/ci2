import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("graph.csv", header=None)

# 2. First column = x, second column = y
x = df.iloc[:, 0].to_numpy(dtype=float)
y = df.iloc[:, 1].to_numpy(dtype=float)

# 3. Fit a straight line y = m*x + b
m, b = np.polyfit(x, y, 1)

# 4. Build the regression line for plotting
x_line = np.linspace(x.min(), x.max(), 200)
y_line = m * x_line + b

# 5. Plot
plt.figure(figsize=(8, 5))
plt.plot(x_line, y_line, color="red", label=f"y = {m:.4f}x + {b:.4f}")
plt.scatter(x, y, s=15, label="data")
plt.xlabel("t [s]")
plt.ylabel("A")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("graph.png", dpi=150)
plt.show()