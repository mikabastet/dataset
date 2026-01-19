import pandas as pd
import os

# Cargar datos
file_path = os.path.expanduser('~/Downloads/Ogappy_14_01_2026.xlsx')
df = pd.read_excel(file_path)

df['post_fecha'] = pd.to_datetime(df['post_fecha'], errors='coerce')

total_por_plataforma = df['source'].value_counts().rename_axis('Plataforma').reset_index(name='Total_Posteos')
posteos_por_dia_plataforma = df.groupby(['post_fecha', 'source']).size().reset_index(name='Conteo')
posteos_totales_por_dia = df.groupby('post_fecha').size().reset_index(name='Total_Posteos_Dia')
dias_validos = posteos_totales_por_dia[posteos_totales_por_dia['Total_Posteos_Dia'] <= 100]['post_fecha']
posteos_filtrados = posteos_por_dia_plataforma[posteos_por_dia_plataforma['post_fecha'].isin(dias_validos)]
output_path = os.path.expanduser('~/Downloads/posteos_resumen.xlsx')
with pd.ExcelWriter(output_path) as writer:
    total_por_plataforma.to_excel(writer, sheet_name='Total por Plataforma', index=False)
    posteos_por_dia_plataforma.to_excel(writer, sheet_name='Por Día y Plataforma', index=False)
    posteos_totales_por_dia.to_excel(writer, sheet_name='Total Diario', index=False)
    posteos_filtrados.to_excel(writer, sheet_name='Filtrado sin Outliers', index=False)

print(f"Datos guardados en: {output_path}")


#Ccuántos posteos hay en total para cada plataforma (MercadoLibre, Remax, etc.).

#cuántos posteos se hicieron por día para cada plataforma.

# cuántos posteos hay en total por día, sumando todas las plataformas.

# excluye los días con más de 100 posteos (considerados outliers).