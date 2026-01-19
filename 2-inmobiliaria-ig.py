import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import os

df = pd.read_excel('~/Downloads/Ogappy_14_01_2026.xlsx')

df_instagram = df[df['source'] == 'instagram'].copy()

total_inmobiliarias = df_instagram['inmobiliaria'].nunique()
print(f"Total inmobiliarias en Instagram: {total_inmobiliarias}")

hoy = pd.to_datetime('today')
fecha_limite = hoy - timedelta(days=30)

df_instagram['post_fecha'] = pd.to_datetime(df_instagram['post_fecha'], errors='coerce')

df_activos = df_instagram[df_instagram['post_fecha'] >= fecha_limite]

inmobiliarias_activas = df_activos['inmobiliaria'].unique()
print(f"Inmobiliarias activas en Instagram últimos 30 días ({len(inmobiliarias_activas)}):")
for inmo in inmobiliarias_activas:
    print(f"- {inmo}")

df_corrientes = df_instagram[df_instagram['ubicacion'].str.contains('Corrientes', case=False, na=False)]

df_corrientes_activas = df_corrientes[df_corrientes['post_fecha'] >= fecha_limite]

inmobiliarias_corrientes_activas = df_corrientes_activas['inmobiliaria'].nunique()
print(f"Inmobiliarias activas en Corrientes Capital (últimos 30 días): {inmobiliarias_corrientes_activas}")


datos = {
    "Total Inmobiliarias": total_inmobiliarias,
    "Inmobiliarias Activas": len(inmobiliarias_activas),
    "Activas en Corrientes": inmobiliarias_corrientes_activas
}

plt.bar(datos.keys(), datos.values(), color=['#5A9', '#59A', '#95A'])
plt.title("Estado de Inmobiliarias en Instagram")
plt.ylabel("Cantidad")
plt.show()

df_activas = pd.DataFrame(inmobiliarias_activas, columns=['Inmobiliaria'])

output_path = os.path.expanduser('~/Downloads/inmobiliarias_activas_instagram.xlsx')
df_activas.to_excel(output_path, index=False)

#65 en total en ig 
#37 activas en losultimos 30 dias
#10 activas en corrientes capital