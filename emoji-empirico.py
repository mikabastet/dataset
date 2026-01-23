import pandas as pd
import os
import re

path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(path)

def tiene_emoji(texto):
    if not isinstance(texto, str):
        return False
    return bool(re.search(r'[\U00010000-\U0010ffff]', texto))

def tiene_patron_precio(texto):
    if not isinstance(texto, str):
        return False
    texto = texto.lower()
    patrones = [
        r'\$\s?\d',
        r'usd\s?\d',
        r'u\$s\s?\d',
        r'ars\s?\d',
        r'pesos\s?\d',
        r'dólar',
        r'dolares',
        r'precio',
        r'valor'
    ]
    return any(re.search(p, texto) for p in patrones)

df["tiene_emoji"] = df["post_descripcion"].apply(tiene_emoji)
df["precio_extraido"] = df["precio"].notna()
df["tiene_patron_precio"] = df["post_descripcion"].apply(tiene_patron_precio)

fallos_reales = df[
    (df["tiene_emoji"] == True) &
    (df["precio_extraido"] == False) &
    (df["tiene_patron_precio"] == True)
]

print(f"Fallos REALES de extracción: {len(fallos_reales)}")

output = os.path.expanduser("~/Downloads/fallos_reales_por_emoji.xlsx")
fallos_reales[
    ["post_descripcion", "precio", "tiene_emoji"]
].to_excel(output, index=False)

print("Archivo guardado en:", output)
