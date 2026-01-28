import pandas as pd
import os
from difflib import get_close_matches
import re


path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df = pd.read_excel(path)

print("Registros originales:", len(df))


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




def normalizar_barrio_texto(texto):
    if pd.isna(texto):
        return None, None

    t = str(texto).lower()

    for barrio in barrios:
        if re.search(rf"\b{re.escape(barrio)}\b", t):
            return barrios[barrio]

    palabras = t.split()
    for p in palabras:
        similar = get_close_matches(p, barrios.keys(), n=1, cutoff=0.85)
        if similar:
            return barrios[similar[0]]

    return None, None


df[["barrio_normalizado", "zona"]] = df["ubicacion"].apply(
    lambda x: pd.Series(normalizar_barrio_texto(x))
)


df_sin_ubicacion = df[
    df["barrio_normalizado"].isna() |
    df["zona"].isna()
].copy()

print("Avisos sin ubicación clara:", len(df_sin_ubicacion))





output_sin_ubicacion = os.path.expanduser(
    "~/Downloads/avisos_sin_ubicacion.xlsx"
)

df_sin_ubicacion.to_excel(output_sin_ubicacion, index=False)

print("Archivo descartados:", output_sin_ubicacion)




df = df.drop(df_sin_ubicacion.index).copy()

print("ubicación válida:", len(df))

def validar_aviso(row):
    precio = pd.to_numeric(row["precio"], errors="coerce")

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

output_final = os.path.expanduser(
    "~/Downloads/dataset_geo_simple.xlsx"
)
recuperados = df[
    df["barrio_normalizado"].notna() &
    df["zona"].notna()
]
mask_sin_ubicacion = (
    df["barrio_normalizado"].isna() |
    df["zona"].isna()
)

df.loc[mask_sin_ubicacion, ["barrio_normalizado", "zona"]] = (
    df.loc[mask_sin_ubicacion, "ubicacion"]
      .apply(lambda x: pd.Series(normalizar_barrio_texto(x)))
)


print( len(recuperados))


df_final.to_excel(output_final, index=False)

print( output_final)
print(df_final["estado_aviso"].value_counts())
