import pandas as pd
import os
import re

file_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(file_path)



def tiene_emoji(texto):
    if not isinstance(texto, str):
        return False
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticonos
        "\U0001F300-\U0001F5FF"  # símbolos
        "\U0001F680-\U0001F6FF"  # transporte
        "\U0001F1E0-\U0001F1FF"  # banderas
        "]+",
        flags=re.UNICODE
    )
    return bool(emoji_pattern.search(texto))

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

# 79.1 % sin emoji 
#45.3 con emoji 
#faalos en extraccion 