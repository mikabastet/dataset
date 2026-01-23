import pandas as pd
import os

ruta = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df = pd.read_excel(ruta)

print(f"Original: {df.shape[0]} filas, {df.shape[1]} columnas")
print("Porcentaje de datos faltantes por columna:")
print((df.isna().mean() * 100).round(2))

umbral = df.shape[1] * 0.5
df = df.dropna(thresh=umbral)

print(f"\nDespués de limpiar: {df.shape[0]} filas")
print(f"Filas eliminadas: {df.shape[0] - len(df)}")  

output = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df.to_excel(output, index=False)
cols_num = ["precio", "habitaciones", "banos", "ambientes", "antiguedad", "superficie_cubierta", "superficie_total"]

for c in cols_num:
    if c in df.columns:
        df[c] = (
            df[c].astype(str)
            .str.replace(",", ".", regex=False)
            .str.extract(r"([-+]?\d*\.?\d+)")
            .astype(float)
        )

if "moneda" in df.columns:
    df["moneda"] = df["moneda"].str.upper().str.strip()

for fecha_col in ["post_fecha", "timecreate"]:
    if fecha_col in df.columns:
        df[fecha_col] = pd.to_datetime(df[fecha_col], errors="coerce")

df["precio_error"] = (df["precio"] <= 0) | (df["precio"] > 1_000_000_000)
df["superficie_error"] = (df["superficie_cubierta"] <= 5) | (df["superficie_cubierta"] > 2000)

print(f"\nErrores detectados: Precios inválidos = {df['precio_error'].sum()}, Superficies inválidas = {df['superficie_error'].sum()}")

df.to_excel(output, index=False)
print(f"Archivo limpio guardado en: {output}")

#Borra filas que tienen más del 50% de datos vacíos
#Limpie columnas numéricas para que sean números bien formateados
#Arregla formato de moneda (mayúsculas y sin espacios)
#Marca como error precios negativos, cero o demasiado altos y superficies fuera de rango

