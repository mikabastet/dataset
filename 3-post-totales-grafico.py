import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

file_path = os.path.expanduser('~/Downloads/Ogappy_14_01_2026.xlsx')
df = pd.read_excel(file_path)

df['post_fecha'] = pd.to_datetime(df['post_fecha'], errors='coerce')

total_por_plataforma = df['source'].value_counts()
print("Total posteos por plataforma:")
print(total_por_plataforma)

posteos_por_dia_plataforma = df.groupby(['post_fecha', 'source']).size().reset_index(name='conteo')

posteos_totales_por_dia = df.groupby('post_fecha').size().reset_index(name='total_dia')
dias_validos = posteos_totales_por_dia[posteos_totales_por_dia['total_dia'] <= 100]['post_fecha']

posteos_filtrados = posteos_por_dia_plataforma[posteos_por_dia_plataforma['post_fecha'].isin(dias_validos)]

print("\nConteo posteos por día y plataforma (sin outliers):")
print(posteos_filtrados.head())

sns.set_style('whitegrid')
plt.figure(figsize=(16, 8), dpi=300)
sns.lineplot(data=posteos_filtrados, x='post_fecha', y='conteo', hue='source', marker='o', linewidth=2.5, markersize=6)

plt.title('Posteos por Día por Plataforma (sin outliers)', fontsize=18, weight='bold', pad=20)
plt.xlabel('Fecha', fontsize=14, weight='bold')
plt.ylabel('Cantidad de posteos', fontsize=14, weight='bold')
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)
plt.legend(title='Plataforma', fontsize=12, title_fontsize=13, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()

output_path = os.path.expanduser('~/Downloads/posteos_por_dia_plataforma.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n✅ Gráfico guardado en: {output_path}")

plt.show()
