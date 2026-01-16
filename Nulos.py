import pandas as pd
import os


file_path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")

df = pd.read_excel(file_path)

print("=" * 50)
print("INFORMACIÓN DEL ARCHIVO ORIGINAL")
print("=" * 50)
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")
print(f"\nPorcentaje de nulos (valores faltantes) por columna:")
print((df.isna().mean() * 100).round(2))

umbral_nulos = df.shape[1] * 0.5  # 50% de columnas
df_limpio = df.dropna(thresh=umbral_nulos)

print("\n" + "=" * 50)
print("INFORMACIÓN DEL ARCHIVO LIMPIO")
print("=" * 50)
print(f"Filas: {df_limpio.shape[0]}")
print(f"Columnas: {df_limpio.shape[1]}")
print(f"Filas eliminadas: {df.shape[0] - df_limpio.shape[0]}")


output_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df_limpio.to_excel(output_path, index=False)

print(f"\nArchivo guardado en: {output_path}")
print("\nPrimeras 5 filas del archivo limpio:")
print(df_limpio.head())



numeric_cols = [
    "precio", "habitaciones", "banos", "ambientes",
    "antiguedad", "superficie_cubierta", "superficie_total"
]

for col in numeric_cols:
    if col in df_limpio.columns:
       
        df_limpio[col] = (
            df_limpio[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.extract(r"([-+]?\d*\.?\d+)")
            .astype(float)
        )


df_limpio["moneda"] = df_limpio["moneda"].str.upper().str.strip()


df_limpio["post_fecha"] = pd.to_datetime(df_limpio["post_fecha"], errors="coerce")
df_limpio["timecreate"] = pd.to_datetime(df_limpio["timecreate"], errors="coerce")


df_limpio["precio_error"] = (df_limpio["precio"] <= 0) | (df_limpio["precio"] > 1_000_000_000)

df_limpio["superficie_error"] = (
    (df_limpio["superficie_cubierta"] <= 5) | (df_limpio["superficie_cubierta"] > 2000)
)


error_summary = {
    "precio_errors": df_limpio["precio_error"].sum(),
    "superficie_errors": df_limpio["superficie_error"].sum()
}

print("\n" + "=" * 50)
print("RESUMEN DE ERRORES DETECTADOS")
print("=" * 50)
print(f"Precios inválidos: {error_summary['precio_errors']}")
print(f"Superficies inválidas: {error_summary['superficie_errors']}")

clean_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df_limpio.to_excel(clean_path, index=False)

print(f"\nArchivo final guardado en: {clean_path}")

