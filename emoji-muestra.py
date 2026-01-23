import pandas as pd
import os
import re

file_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(file_path)

def tiene_emoji(texto):
    if not isinstance(texto, str):
        return False
    return bool(re.search(r'[\U00010000-\U0010ffff]', texto))

df["tiene_emoji"] = df["post_descripcion"].apply(tiene_emoji)
df["precio_extraido"] = df["precio"].notna()

resumen = (
    df
    .groupby("tiene_emoji")["precio_extraido"]
    .mean()
    .reset_index()
)

resumen["porcentaje_exito"] = (resumen["precio_extraido"] * 100).round(1)
print(resumen)

ejemplos_fallos = df[
    (df["tiene_emoji"] == True) &
    (df["precio_extraido"] == False)
]

output = os.path.expanduser("~/Downloads/ejemplos_fallos_emojis.xlsx")
ejemplos_fallos.to_excel(output, index=False)

print("Archivo generado:", output)
