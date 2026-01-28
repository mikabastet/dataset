import pandas as pd
import re
from geopy.geocoders import Nominatim
from time import sleep

input_path = r"C:\Users\mika\Downloads\Ogappy_14_01_2026.xlsx"
output_path = r"C:\Users\mika\Downloads\dataset_geocodificado_completo.xlsx"

df = pd.read_excel(input_path)

def extraer_ubicacion(texto):
    if pd.isna(texto):
        return None
    texto = texto.lower()
    patrones = [
        r"barrio\s+[a-záéíóúñ\s]{3,40}",
        r"b°\s*[a-záéíóúñ\s]{3,40}",
        r"zona\s+[a-záéíóúñ\s]{3,40}",
        r"[a-záéíóúñ]+\s+\d{2,5}",   
        r"av\.?\s*[a-záéíóúñ\s]+\d{0,5}"
    ]
    for p in patrones:
        m = re.search(p, texto)
        if m:
            return m.group(0)
    return None

mask_sin_ubi = df["ubicacion"].isna() | (df["ubicacion"] == "")
df.loc[mask_sin_ubi, "ubicacion_alternativa"] = df.loc[mask_sin_ubi, "post_descripcion"].apply(extraer_ubicacion)

df["ubicacion_final"] = df["ubicacion"]
mask = df["ubicacion_final"].isna() | (df["ubicacion_final"] == "")
df.loc[mask, "ubicacion_final"] = df.loc[mask, "ubicacion_alternativa"]

df["direccion_limpia"] = (
    df["ubicacion_final"]
    .astype(str)
    .str.lower()
    .str.replace(r"[^\w\s]", "", regex=True)
    .str.strip()
)

geolocator = Nominatim(user_agent="geo_mika")

def geocodificar(direccion):
    try:
        if direccion == "" or direccion.lower() == "none":
            return None, None
        location = geolocator.geocode(direccion + ", Corrientes, Argentina", timeout=10)
        sleep(1)  
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return None, None

if "lat" not in df.columns:
    df["lat"] = None
if "lon" not in df.columns:
    df["lon"] = None

for i, row in df.iterrows():
    if pd.isna(row["lat"]) or pd.isna(row["lon"]):
        lat, lon = geocodificar(row["direccion_limpia"])
        df.at[i, "lat"] = lat
        df.at[i, "lon"] = lon
        print(f"Fila {i}: {row['direccion_limpia']} -> lat: {lat}, lon: {lon}")

df.to_excel(output_path, index=False)
print("Archivo geocodificado guardado en:", output_path)

print("Registros totales:", len(df))
print("Registros sin ubicación original:", mask_sin_ubi.sum())
print("Registros con ubicación alternativa encontrada:", df["ubicacion_alternativa"].notna().sum())
print("Registros sin ubicación final:", df["ubicacion_final"].isna().sum())
print("Registros con latitud y longitud:", df["lat"].notna().sum())
