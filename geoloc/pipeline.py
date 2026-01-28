import re
import pandas as pd
import os

path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df = pd.read_excel(path)

def extraer_ubicacion_descripcion(texto):
    if pd.isna(texto):
        return None

    texto = texto.lower()

    patrones = [
        r"barrio\s+[a-záéíóúñ\s]+",
        r"b°\s*[a-záéíóúñ\s]+",
        r"zona\s+[a-záéíóúñ\s]+",
        r"[a-záéíóúñ]+\s+\d{2,5}"   # calle + número
    ]

    for patron in patrones:
        match = re.search(patron, texto)
        if match:
            return match.group(0)

    return None
df["ubicacion_alternativa"] = df["post_descripcion"].apply(
    extraer_ubicacion_descripcion
)
df["ubicacion_final"] = df["ubicacion"]

df.loc[
    df["ubicacion_final"].isna(),
    "ubicacion_final"
] = df["ubicacion_alternativa"]
df["direccion_limpia"] = (
    df["ubicacion_final"]
    .astype(str)
    .str.lower()
    .str.replace(r"[^\w\s]", "", regex=True)
    .str.strip()
)

df_test = df.head(20).copy()

df_test["ubicacion_final"] = df_test["post_descripcion"].apply(
    extraer_ubicacion_descripcion
)

print(df_test[["post_descripcion", "ubicacion_alternativa", "ubicacion_final", "direccion_limpia"]])
