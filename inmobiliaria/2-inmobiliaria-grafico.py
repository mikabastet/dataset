import pandas as pd
from datetime import timedelta
import os
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel(os.path.expanduser('~/Downloads/Ogappy_14_01_2026.xlsx'))

df_instagram = df[df['source'] == 'instagram']

hoy = pd.to_datetime('today')
fecha_limite = hoy - timedelta(days=30)

df_instagram['post_fecha'] = pd.to_datetime(df_instagram['post_fecha'], errors='coerce')

df_activos = df_instagram[df_instagram['post_fecha'] >= fecha_limite]

posts_por_inmo = df_activos['inmobiliaria'].value_counts()

num_inmobiliarias_activas = posts_por_inmo.count()

plt.figure(figsize=(10, 6))
sns.barplot(x=posts_por_inmo.values, y=posts_por_inmo.index, palette='pastel')

plt.title(f'Inmobiliarias activas en Instagram (últimos 30 días)\nTotal: {num_inmobiliarias_activas}', fontsize=16)
plt.xlabel('Cantidad de posteos')
plt.ylabel('Inmobiliaria')

plt.tight_layout()

output_img_path = os.path.expanduser('~/Downloads/inmobiliarias_activas_instagram.png')
plt.savefig(output_img_path, dpi=300)
plt.show()

print(f"Gráfico guardado en: {output_img_path}")
