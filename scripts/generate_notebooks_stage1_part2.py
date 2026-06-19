import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_eda_notebooks():
    nb = new_notebook()
    
    cells = [
        new_markdown_cell("# EDA: Dataset Overview\n\n## 1. Goal\nAnalyze the data schema and target distributions.\n\n## 2. Imports"),
        new_code_cell("""import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root
project_root = Path(os.getcwd()).parent.parent
sys.path.append(str(project_root))

from notebooks.config import *
sns.set_style(PLOT_STYLE)"""),
        
        new_markdown_cell("## 3. Load Engineered Data"),
        new_code_cell("""df = pd.read_parquet(CLEANED_DATA_PATH)
print(f"Dataset shape: {df.shape}")
df.head()"""),
        
        new_markdown_cell("## 4. Target Variables Analysis"),
        new_code_cell("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(df[RESPONSE_TIME_TARGET], bins=50, ax=axes[0])
axes[0].set_title("Resolution Duration (minutes)")

sns.histplot(df[CONGESTION_TARGET], bins=20, ax=axes[1])
axes[1].set_title("Congestion Proxy Score")

sns.countplot(x=df[DEPLOYMENT_TARGET], order=['LOW', 'MEDIUM', 'HIGH'], ax=axes[2])
axes[2].set_title("Deployment Load Classification")

plt.tight_layout()
plt.show()"""),

        new_markdown_cell("## 5. Temporal Patterns"),
        new_code_cell("""plt.figure(figsize=(10, 5))
sns.countplot(x='hour_of_day', data=df, hue='is_weekend')
plt.title("Incident Frequency by Hour of Day")
plt.show()""")
    ]
    
    nb['cells'] = cells
    with open('notebooks/eda/01_dataset_overview.ipynb', 'w') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    create_eda_notebooks()
    print("EDA notebooks generated.")
