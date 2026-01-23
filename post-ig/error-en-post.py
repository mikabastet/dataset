import pandas as pd
import os

df = pd.read_excel(os.path.expanduser('~/Downloads/Ogappy_14_01_2026.xlsx'))

df_instagram = df[df['source'] == 'instagram'].copy()

df_instagram['post_fecha'] = pd.to_datetime(df_instagram['post_fecha'], errors='coerce')

fechas_validas = df_instagram['post_fecha'].notna().sum()
fechas_invalidas = df_instagram['post_fecha'].isna().sum()
total = len(df_instagram)

print(f"Total registros Instagram: {total}")
print(f"Registros con fecha válida: {fechas_validas}")
print(f"Registros con fecha inválida (NaT): {fechas_invalidas}")

df_fechas_invalidas = df_instagram[df_instagram['post_fecha'].isna()]

output_path = os.path.expanduser('~/Downloads/fechas_invalidas_instagram.xlsx')
df_fechas_invalidas.to_excel(output_path, index=False)

print(f"\nEjemplos de registros con fecha inválida guardados en: {output_path}")
