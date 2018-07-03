import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


raw_data = pd.read_csv('pokemon.csv', header=0)


# number of variable
df = raw_data[['Type 1', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation']]
categories=list(df)[1:]
N = len(categories)

groupby_type_df = df.groupby(['Type 1']).mean()
normalized_df=(
        (groupby_type_df - groupby_type_df.min()) / 
        (groupby_type_df.max() - groupby_type_df.min())
        )

def drawByGroup(type1, plot_row, plot_column, plot_index):
    # We need to repeat the first value to close the circular graph:
    values=list(normalized_df.loc[type1])
    values += values[:1]
     
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    p = plt.subplot(plot_row, plot_column, plot_index, polar=True, title=type1)
    p .set_title(type1)

    plt.xticks(angles[:-1], categories, color='grey', size=8)

    p.set_rlabel_position(0)
    plt.yticks([0.25,0.5,0.75], ["0.25","0.5","0.75"], color="grey", size=7)
    plt.ylim(0,1)

    p.plot(angles, values, linewidth=1, linestyle='solid')

    p.fill(angles, values, 'b', alpha=0.1)

plt.figure(figsize=(8,8), dpi=100)
drawByGroup("Bug", 2, 2, 1)
drawByGroup("Dragon", 2, 2, 2)
drawByGroup("Water", 2, 2, 3)
