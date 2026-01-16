import pandas as pd
import os

# ============================================================
# PASO 1: CARGAR EL DATASET
# ============================================================
# Expandir ~ a la ruta del usuario para obtener la carpeta Descargas
file_path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")

# Leer el archivo Excel con pandas
df = pd.read_excel(file_path)

print("=" * 50)
print("INFORMACIÓN DEL ARCHIVO ORIGINAL")
print("=" * 50)
# Mostrar dimensiones: número de filas y columnas
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")
print(f"\nPorcentaje de nulos (valores faltantes) por columna:")
# Calcular qué porcentaje de cada columna está vacío
print((df.isna().mean() * 100).round(2))

# ============================================================
# PASO 2: LIMPIAR DATOS - ELIMINAR FILAS CON MUCHOS NULOS
# ============================================================
# Calcular el umbral: si 50% o más de las columnas están vacías, eliminar la fila
umbral_nulos = df.shape[1] * 0.5  # 50% de columnas
# dropna(thresh=X) mantiene solo las filas que tienen al menos X valores no-nulos
df_limpio = df.dropna(thresh=umbral_nulos)

print("\n" + "=" * 50)
print("INFORMACIÓN DEL ARCHIVO LIMPIO")
print("=" * 50)
print(f"Filas: {df_limpio.shape[0]}")
print(f"Columnas: {df_limpio.shape[1]}")
print(f"Filas eliminadas: {df.shape[0] - df_limpio.shape[0]}")

# ============================================================
# PASO 3: GUARDAR RESULTADO INICIAL
# ============================================================
output_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df_limpio.to_excel(output_path, index=False)

print(f"\nArchivo guardado en: {output_path}")
print("\nPrimeras 5 filas del archivo limpio:")
print(df_limpio.head())


# ============================================================
# PASO 4: CONVERTIR COLUMNAS A NÚMEROS
# ============================================================
# Definir qué columnas deben ser numéricas
numeric_cols = [
    "precio", "habitaciones", "banos", "ambientes",
    "antiguedad", "superficie_cubierta", "superficie_total"
]

# Para cada columna numérica:
for col in numeric_cols:
    if col in df_limpio.columns:
        # 1. Convertir a texto
        # 2. Reemplazar comas por puntos (formato europeo a inglés)
        # 3. Extraer solo números válidos (evitar caracteres basura)
        # 4. Convertir a número flotante
        df_limpio[col] = (
            df_limpio[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.extract(r"([-+]?\d*\.?\d+)")
            .astype(float)
        )

# ============================================================
# PASO 5: ESTANDARIZAR MONEDA
# ============================================================
# Convertir todo a mayúsculas y eliminar espacios en blanco
df_limpio["moneda"] = df_limpio["moneda"].str.upper().str.strip()

# ============================================================
# PASO 6: CONVERTIR FECHAS A FORMATO DATETIME
# ============================================================
# errors="coerce" convierte valores inválidos a NaT (Not a Time)
df_limpio["post_fecha"] = pd.to_datetime(df_limpio["post_fecha"], errors="coerce")
df_limpio["timecreate"] = pd.to_datetime(df_limpio["timecreate"], errors="coerce")

# ============================================================
# PASO 7: DETECTAR ERRORES Y VALORES SOSPECHOSOS
# ============================================================
# Crear columna booleana: precio inválido si es <= 0 o > 1 mil millones
df_limpio["precio_error"] = (df_limpio["precio"] <= 0) | (df_limpio["precio"] > 1_000_000_000)

# Crear columna booleana: superficie inválida si < 5 m² o > 2000 m²
df_limpio["superficie_error"] = (
    (df_limpio["superficie_cubierta"] <= 5) | (df_limpio["superficie_cubierta"] > 2000)
)

# ============================================================
# PASO 8: RESUMEN DE ERRORES
# ============================================================
error_summary = {
    "precio_errors": df_limpio["precio_error"].sum(),
    "superficie_errors": df_limpio["superficie_error"].sum()
}

print("\n" + "=" * 50)
print("RESUMEN DE ERRORES DETECTADOS")
print("=" * 50)
print(f"Precios inválidos: {error_summary['precio_errors']}")
print(f"Superficies inválidas: {error_summary['superficie_errors']}")

# ============================================================
# PASO 9: GUARDAR DATASET FINAL LIMPIO Y PROCESADO
# ============================================================
# Guardar el archivo final con todos los cambios
clean_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df_limpio.to_excel(clean_path, index=False)

print(f"\nArchivo final guardado en: {clean_path}")

