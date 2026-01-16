import pandas as pd
import os
import re
from collections import Counter

original_path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df_original = pd.read_excel(original_path)

clean_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df_limpio = pd.read_excel(clean_path)

print("=" * 80)
print("ANÁLISIS AVANZADO: PATRONES DE ERROR EN EXTRACCIÓN")
print("=" * 80)


print("\n" + "=" * 80)
print("1. ERRORES POR INMOBILIARIA (Top 15)")
print("=" * 80)

# Analizar completitud por inmobiliaia
inmobiliaria_stats = []
for inmo in df_original["inmobiliaria"].dropna().unique()[:15]:  # Top 15
    if pd.isna(inmo):
        continue
    subset = df_original[df_original["inmobiliaria"] == inmo]
    total = len(subset)
    stats = {
        "Inmobiliaria": inmo,
        "Total Posts": total,
        "% Precio": (subset["precio"].notna().sum() / total * 100).round(1),
        "% Habitaciones": (subset["habitaciones"].notna().sum() / total * 100).round(1),
        "% Superficie": ((subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).sum() / total * 100).round(1),
        "% Titulo": (subset["titulo"].notna().sum() / total * 100).round(1),
        "% Antiguedad": (subset["antiguedad"].notna().sum() / total * 100).round(1),
    }
    inmobiliaria_stats.append(stats)

inmobiliaria_df = pd.DataFrame(inmobiliaria_stats).sort_values("Total Posts", ascending=False).head(15)
print(inmobiliaria_df.to_string(index=False))


print("\n" + "=" * 80)
print("2. ERRORES POR FUENTE (Source/Type of Post)")
print("=" * 80)

source_stats = []
for source in df_original["source"].dropna().unique():
    subset = df_original[df_original["source"] == source]
    total = len(subset)
    stats = {
        "Fuente": source,
        "Total": total,
        "% Precio": (subset["precio"].notna().sum() / total * 100).round(1),
        "% Habitaciones": (subset["habitaciones"].notna().sum() / total * 100).round(1),
        "% Superficie": ((subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).sum() / total * 100).round(1),
        "% Titulo": (subset["titulo"].notna().sum() / total * 100).round(1),
    }
    source_stats.append(stats)

source_df = pd.DataFrame(source_stats).sort_values("Total", ascending=False)
print(source_df.to_string(index=False))


print("\n" + "=" * 80)
print("3. ERRORES SEGÚN LONGITUD DE DESCRIPCIÓN")
print("=" * 80)

df_original["text_length"] = df_original["post_descripcion"].fillna("").str.len()

# Categorizar por longitud
df_original["text_category"] = pd.cut(df_original["text_length"], 
                                       bins=[0, 100, 300, 500, 1000, float("inf")],
                                       labels=["Muy Corto (0-100)", "Corto (100-300)", 
                                              "Medio (300-500)", "Largo (500-1000)", "Muy Largo (1000+)"])

length_stats = []
for cat in ["Muy Corto (0-100)", "Corto (100-300)", "Medio (300-500)", "Largo (500-1000)", "Muy Largo (1000+)"]:
    subset = df_original[df_original["text_category"] == cat]
    if len(subset) > 0:
        total = len(subset)
        stats = {
            "Longitud Texto": cat,
            "Registros": total,
            "% Precio": (subset["precio"].notna().sum() / total * 100).round(1),
            "% Habitaciones": (subset["habitaciones"].notna().sum() / total * 100).round(1),
            "% Superficie": ((subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).sum() / total * 100).round(1),
        }
        length_stats.append(stats)

length_df = pd.DataFrame(length_stats)
print(length_df.to_string(index=False))

print("\n" + "=" * 80)
print("4. ANÁLISIS DE FALLOS: PRECIO NO EXPLÍCITO")
print("=" * 80)

precio_keywords = ["precio", "costo", "valor", "usd", "usd", "ars", "$", "consulta", "oferta"]
moneda_keywords = ["usd", "ars", "dólar", "peso", "uyu"]

def has_precio_keyword(text):
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    return any(keyword in text_lower for keyword in precio_keywords)

def has_moneda_info(text):
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    return any(keyword in text_lower for keyword in moneda_keywords)

df_original["has_price_keyword"] = df_original["post_descripcion"].apply(has_precio_keyword)
df_original["has_currency_info"] = df_original["post_descripcion"].apply(has_moneda_info)

sin_precio_pero_palabra = df_original[(df_original["has_price_keyword"]) & (df_original["precio"].isna())]

print(f"\nTotal registros con palabra 'precio': {df_original['has_price_keyword'].sum()}")
print(f"Total registros con info de moneda: {df_original['has_currency_info'].sum()}")
print(f"Registros con PALABRA precio pero SIN precio extraído: {len(sin_precio_pero_palabra)}")
print(f"  % de fallos: {(len(sin_precio_pero_palabra) / df_original['has_price_keyword'].sum() * 100).round(1)}%")

# Ejemplos de fallos
print("\nEjemplos de descripciones con 'precio' pero sin extracción:")
ejemplos = sin_precio_pero_palabra["post_descripcion"].head(3)
for idx, (i, texto) in enumerate(ejemplos.items(), 1):
    print(f"  {idx}. {str(texto)[:100]}...")


print("\n" + "=" * 80)
print("5. PATRONES DE ERROR: EMOJIS Y CARACTERES ESPECIALES")
print("=" * 80)

def has_emoji(text):
    if pd.isna(text):
        return False
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  #
        "\u3030"
        "]+", flags=re.UNICODE
    )
    return bool(emoji_pattern.search(str(text)))

df_original["has_emoji"] = df_original["post_descripcion"].apply(has_emoji)

con_emoji = df_original[df_original["has_emoji"] == True]
sin_emoji = df_original[df_original["has_emoji"] == False]

print(f"\nRegistros CON emojis: {len(con_emoji)}")
print(f"Registros SIN emojis: {len(sin_emoji)}")

print(f"\nComparativa de extracción (Precio):")
print(f"  Con emojis - % Precio extraído: {(con_emoji['precio'].notna().sum() / len(con_emoji) * 100).round(1)}%")
print(f"  Sin emojis - % Precio extraído: {(sin_emoji['precio'].notna().sum() / len(sin_emoji) * 100).round(1)}%")

print(f"\nComparativa de extracción (Superficie):")
print(f"  Con emojis - % Superficie: {((con_emoji['superficie_cubierta'].notna() | con_emoji['superficie_total'].notna()).sum() / len(con_emoji) * 100).round(1)}%")
print(f"  Sin emojis - % Superficie: {((sin_emoji['superficie_cubierta'].notna() | sin_emoji['superficie_total'].notna()).sum() / len(sin_emoji) * 100).round(1)}%")


print("\n" + "=" * 80)
print("6. ANÁLISIS: CONFUSIÓN M2 CON AMBIENTES")
print("=" * 80)

print("\nAmbientes extraídos - Distribución:")
ambientes_no_nulos = df_original[df_original["ambientes"].notna()]["ambientes"]
print(f"  Mínimo: {ambientes_no_nulos.min()}")
print(f"  Máximo: {ambientes_no_nulos.max()}")
print(f"  Media: {ambientes_no_nulos.mean():.2f}")

sospechosos = df_original[df_original["ambientes"] > 10]
print(f"\nRegistros con AMBIENTES > 10 (probablemente confusión con m2): {len(sospechosos)}")
if len(sospechosos) > 0:
    print("  Ejemplos sospechosos:")
    for idx, row in sospechosos.head(5).iterrows():
        print(f"    - Ambientes: {row['ambientes']}, Superficie cubierta: {row['superficie_cubierta']}")


print("\n" + "=" * 80)
print("7. ANÁLISIS: BARRIOS MAL ESCRITOS / INCONSISTENCIAS")
print("=" * 80)

ubicaciones = df_original["ubicacion"].dropna()
print(f"\nTotal ubicaciones únicas: {len(ubicaciones.unique())}")

from difflib import get_close_matches

top_ubicaciones = ubicaciones.value_counts().head(20)
print("\nTop 20 ubicaciones más frecuentes:")
print(top_ubicaciones)

print("\nVerificando similares:")
ubicaciones_lista = ubicaciones.unique().tolist()
posibles_duplicados = []

for i, ubi1 in enumerate(ubicaciones_lista[:100]):  # Limitar para velocidad
    similares = get_close_matches(ubi1, ubicaciones_lista, n=3, cutoff=0.85)
    if len(similares) > 1:
        posibles_duplicados.append(similares)

if posibles_duplicados:
    print("Posibles duplicados encontrados (escriba similar):")
    for grupo in posibles_duplicados[:10]:
        print(f"  - {grupo}")


print("\n" + "=" * 80)
print("8. FALLOS SISTEMÁTICOS DE LA IA - PATRONES DETECTADOS")
print("=" * 80)




print("\n" + "=" * 80)
print("9. RANKING: ESCENARIOS CON MÁS FALLOS DE IA (Top 10)")
print("=" * 80)

fallos = []

# Por fuente
for source in df_original["source"].dropna().unique():
    subset = df_original[df_original["source"] == source]
    fail_rate_precio = (1 - subset["precio"].notna().sum() / len(subset)) * 100
    fail_rate_super = (1 - (subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).sum() / len(subset)) * 100
    fallos.append({
        "Escenario": f"Fuente: {source}",
        "Registros": len(subset),
        "% Fallo Precio": fail_rate_precio,
        "% Fallo Superficie": fail_rate_super,
    })

# Por longitud
for cat in ["Muy Corto (0-100)", "Corto (100-300)", "Medio (300-500)"]:
    subset = df_original[df_original["text_category"] == cat]
    if len(subset) > 0:
        fail_rate_precio = (1 - subset["precio"].notna().sum() / len(subset)) * 100
        fail_rate_super = (1 - (subset["superficie_cubierta"].notna() | subset["superficie_total"].notna()).sum() / len(subset)) * 100
        fallos.append({
            "Escenario": f"Texto: {cat}",
            "Registros": len(subset),
            "% Fallo Precio": fail_rate_precio,
            "% Fallo Superficie": fail_rate_super,
        })


fallos.append({
    "Escenario": "Con Emojis",
    "Registros": len(con_emoji),
    "% Fallo Precio": (1 - con_emoji["precio"].notna().sum() / len(con_emoji)) * 100,
    "% Fallo Superficie": (1 - (con_emoji["superficie_cubierta"].notna() | con_emoji["superficie_total"].notna()).sum() / len(con_emoji)) * 100,
})

fallos.append({
    "Escenario": "Sin Emojis",
    "Registros": len(sin_emoji),
    "% Fallo Precio": (1 - sin_emoji["precio"].notna().sum() / len(sin_emoji)) * 100,
    "% Fallo Superficie": (1 - (sin_emoji["superficie_cubierta"].notna() | sin_emoji["superficie_total"].notna()).sum() / len(sin_emoji)) * 100,
})

fallos_df = pd.DataFrame(fallos).sort_values("% Fallo Precio", ascending=False)
print(fallos_df.to_string(index=False))


print("\n" + "=" * 80)
print("10. GUARDANDO REPORTES")
print("=" * 80)

reporte_path = os.path.expanduser("~/Downloads/patrones_errores.xlsx")
with pd.ExcelWriter(reporte_path) as writer:
    inmobiliaria_df.to_excel(writer, sheet_name="Errores por Inmobiliaria", index=False)
    source_df.to_excel(writer, sheet_name="Errores por Fuente", index=False)
    length_df.to_excel(writer, sheet_name="Errores por Longitud", index=False)
    fallos_df.to_excel(writer, sheet_name="Fallos Sistemáticos", index=False)

print(f"\nReporte de patrones de error guardado en:")
print(f"  {reporte_path}")
