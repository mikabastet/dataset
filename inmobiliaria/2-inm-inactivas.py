import pandas as pd
from datetime import timedelta
import os

df = pd.read_excel('~/Downloads/Ogappy_14_01_2026.xlsx')

df_instagram = df[df['source'] == 'instagram'].copy()

df_instagram['post_fecha'] = pd.to_datetime(df_instagram['post_fecha'], errors='coerce')

hoy = pd.to_datetime('today')
fecha_limite = hoy - timedelta(days=30)

inmobiliarias_totales = set(df_instagram['inmobiliaria'].unique())

inmobiliarias_activas = set(df_instagram[df_instagram['post_fecha'] >= fecha_limite]['inmobiliaria'].unique())

inmobiliarias_inactivas = inmobiliarias_totales - inmobiliarias_activas

ultima_fecha_posteo = df_instagram.groupby('inmobiliaria')['post_fecha'].max()


df_inactivas = pd.DataFrame({
    'Inmobiliaria': list(inmobiliarias_inactivas),
    'Ultima_fecha_posteo': [ultima_fecha_posteo.get(inmo, pd.NaT) for inmo in inmobiliarias_inactivas]
})


df_inactivas = df_inactivas.sort_values(by='Ultima_fecha_posteo', na_position='first')


print(f"Inmobiliarias inactivas (sin posteos en últimos 30 días): {len(inmobiliarias_inactivas)}\n")
print(df_inactivas.to_string(index=False))


output_path = os.path.expanduser('~/Downloads/inmobiliarias_inactivas_con_fecha.xlsx')
df_inactivas.to_excel(output_path, index=False)

print(f"\nArchivo guardado para revisión: {output_path}")

