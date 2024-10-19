# matplotlib_overview.py - My exploration of different plot types and customizations in Matplotlib

import numpy as np
import matplotlib.pyplot as plt
import os

# Create a directory to store the images
image_dir = 'visualization_assets'
os.makedirs(image_dir, exist_ok=True)

# Function to save figures
def save_figure(fig, filename):
    fig.savefig(os.path.join(image_dir, filename))
    plt.close(fig)
    print(f"Saved '{filename}' in the '{image_dir}' directory")

# Generate some sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 48, 15, 31, 57]
data = np.random.randn(1000)

# 1. Line Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y1, label='sin(x)')
ax.plot(x, y2, label='cos(x)')
ax.set_title('Line Plot: Trigonometric Functions')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True)
save_figure(fig, 'line_plot.png')

# 2. Scatter Plot
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(x, y1, c=y2, cmap='viridis', s=50)
plt.colorbar(scatter, label='cos(x)')
ax.set_title('Scatter Plot: sin(x) vs x, colored by cos(x)')
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
save_figure(fig, 'scatter_plot.png')

# 3. Bar Plot
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categories, values, color='skyblue', edgecolor='navy')
ax.set_title('Bar Plot: Sample Categories')
ax.set_xlabel('Category')
ax.set_ylabel('Value')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height}', ha='center', va='bottom')
save_figure(fig, 'bar_plot.png')

# 4. Histogram
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(data, bins=30, edgecolor='black')
ax.set_title('Histogram: Distribution of Random Data')
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
save_figure(fig, 'histogram.png')

# 5. Box Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot([y1, y2], labels=['sin(x)', 'cos(x)'])
ax.set_title('Box Plot: Distribution of sin(x) and cos(x)')
ax.set_ylabel('Value')
save_figure(fig, 'box_plot.png')

# 6. Subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Subplots: Multiple Visualizations', fontsize=16)

axs[0, 0].plot(x, y1)
axs[0, 0].set_title('Line Plot: sin(x)')

axs[0, 1].scatter(x, y2)
axs[0, 1].set_title('Scatter Plot: cos(x)')

axs[1, 0].bar(categories, values)
axs[1, 0].set_title('Bar Plot: Categories')

axs[1, 1].hist(data, bins=20)
axs[1, 1].set_title('Histogram: Random Data')

plt.tight_layout()
save_figure(fig, 'subplots.png')

print("\nMatplotlib Overview Complete!")
print(f"I've created various types of plots and saved them in the '{image_dir}' directory.")
print("This exercise has helped me understand different visualization techniques")
print("and how to customize plots using Matplotlib.")