import pandas as pd
import os
from difflib import get_close_matches

path: str = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df = pd.read_excel(path)

barrios = {
    "centro": ("Centro", "Centro"),
    "barrio centro": ("Centro", "Centro"),
    "camba cua": ("Camba Cuá", "Oeste"),
    "camba cuá": ("Camba Cuá", "Oeste"),
    "libertad": ("Libertad", "Oeste"),
    "la cruz": ("La Cruz", "Norte"),
    "apipe": ("Apipé", "Este"),
    "apipé": ("Apipé", "Este"),
    "san juan": ("San Juan", "Centro"),
    "belgrano": ("Belgrano", "Centro"),
}

def normalizar_barrio(barrio):
    if pd.isna(barrio):
        return None, None

    b = str(barrio).lower().strip()

    if b in barrios:
        return barrios[b]

    similar = get_close_matches(b, barrios.keys(), n=1, cutoff=0.8)
    if similar:
        return barrios[similar[0]]

    return barrio, None

df[["barrio_normalizado", "zona"]] = df["ubicacion"].apply(
    lambda x: pd.Series(normalizar_barrio(x))
)

def validar_aviso(row):
    precio = pd.to_numeric(row["precio"], errors="coerce")

    if pd.isna(row["barrio_normalizado"]) or pd.isna(row["zona"]):
        return "RECHAZADO"

    if pd.isna(precio) or precio <= 0:
        return "RECHAZADO"

    return "VÁLIDO"

df["estado_aviso"] = df.apply(validar_aviso, axis=1)

df_final = df[[
    "Link Original",
    "barrio_normalizado",
    "zona",
    "tipo_propiedad",
    "tipo_operacion",
    "precio",
    "superficie_cubierta",
    "superficie_total",
    "habitaciones",
    "estado_aviso",
    "source"
]].copy()
output = os.path.expanduser("~/Downloads/dataset_geo_simple.xlsx")
df_final.to_excel(output, index=False)

print("Dataset listo:", output)
print(df_final["estado_aviso"].value_counts())

#El script limpia y ordena la información de los avisos.
#Unifica los nombres de barrios, agrega una zona general para facilitar y descarta publicaciones incompletas