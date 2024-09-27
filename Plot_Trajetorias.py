import matplotlib.pyplot as plt
import pandas as pd

x = pd.read_csv('C:\\Users\\isabe\\OneDrive\\Área de Trabalho\\Codigos_Projeto_HU\\Gráficos de Desempenho dos Códigos\\x_10.csv')
y = pd.read_csv('C:\\Users\\isabe\\OneDrive\\Área de Trabalho\\Codigos_Projeto_HU\\Gráficos de Desempenho dos Códigos\\y_10.csv')

fig, ax = plt.subplots()

for i in range(len(x)-1):
    ax.annotate('', xy=(y['y'][i+1], x['x'][i+1]), xytext=(y['y'][i], x['x'][i]), arrowprops=dict(arrowstyle="->", color='mediumblue'))

for i in range(len(x)-2):
    ax.plot(y['y'][i+1], x['x'][i+1], 'o', color='crimson')

ax.set_xlim(0, 24.5) 
ax.set_ylim(0, 8)

ax.invert_yaxis()

plt.gca().xaxis.set_ticks_position('top')
plt.gca().xaxis.set_label_position('top')

plt.xticks(fontsize=10, weight='bold')
plt.yticks(fontsize=10, weight='bold')
plt.xlabel('x', fontsize=12, weight='bold')
plt.ylabel('y', fontsize=12, weight='bold')

ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.spines['top'].set_visible(True)

plt.show()