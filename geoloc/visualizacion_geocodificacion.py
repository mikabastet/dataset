import pandas as pd
import matplotlib.pyplot as plt
import folium



input_path = r"C:\Users\mika\Downloads\dataset_geocodificado_completo.xlsx"
df = pd.read_excel(input_path)



total = len(df)
sin_ubi_original = df["ubicacion"].isna().sum()
ubi_alternativa = df["ubicacion_alternativa"].notna().sum()
sin_ubi_final = df["ubicacion_final"].isna().sum()
con_geo = df["lat"].notna().sum()



labels = [
    "Total registros",
    "Sin ubicación original",
    "Ubicación recuperada",
    "Sin ubicación final",
    "Geocodificados"
]

values = [
    total,
    sin_ubi_original,
    ubi_alternativa,
    sin_ubi_final,
    con_geo
]

plt.figure(figsize=(10,6))
plt.bar(labels, values)
plt.title("Estado de Ubicaciones en el Dataset")
plt.ylabel("Cantidad de registros")
plt.xticks(rotation=30)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()


df_mapa = df[df["lat"].notna() & df["lon"].notna()]

mapa = folium.Map(location=[-27.47, -58.83], zoom_start=12)

for _, row in df_mapa.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=3,
        fill=True
    ).add_to(mapa)

mapa.save(r"C:\Users\mika\Downloads\mapa_inmuebles.html")

print("Mapa guardado en Descargas como mapa_inmuebles.html")
#El script genera métricas y visualizaciones del proceso de geocodificación.    
