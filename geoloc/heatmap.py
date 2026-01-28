import pandas as pd
import folium
from folium.plugins import HeatMap

input_path = r"C:\Users\mika\Downloads\dataset_geocodificado_completo.xlsx"
df = pd.read_excel(input_path)

df_mapa = df[df["lat"].notna() & df["lon"].notna()]
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

mapa = folium.Map(location=[-27.47, -58.83], zoom_start=12)

data_heat = df_mapa[['lat', 'lon']].values.tolist()

HeatMap(data_heat, 
        radius=15, 
        blur=10, 
        min_opacity=0.5,
        gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
       ).add_to(mapa)

output_path = r"C:\Users\mika\Downloads\heatmap_inmuebles.html"
mapa.save(output_path)

print(f"{output_path}")