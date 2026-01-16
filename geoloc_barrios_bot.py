import pandas as pd
import os
import re
from difflib import get_close_matches


original_path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df = pd.read_excel(original_path)

print("=" * 90)
print("GEOLOCALIZACIÓN Y NORMALIZACIÓN DE BARRIOS")
print("=" * 90)

print("\n" + "=" * 90)
print("1. NORMALIZACIÓN DE NOMBRES DE BARRIOS")
print("=" * 90)

barrios_normalizacion = {
    "centro": {"nombre": "Centro", "zona": "Centro", "lat": -27.4819, "lon": -55.5048, "region": "Central"},
    "barrio centro": {"nombre": "Centro", "zona": "Centro", "lat": -27.4819, "lon": -55.5048, "region": "Central"},
    "b° centro": {"nombre": "Centro", "zona": "Centro", "lat": -27.4819, "lon": -55.5048, "region": "Central"},
    
    "camba cua": {"nombre": "Camba Cuá", "zona": "Oeste", "lat": -27.4920, "lon": -55.5230, "region": "Oeste"},
    "camba cuá": {"nombre": "Camba Cuá", "zona": "Oeste", "lat": -27.4920, "lon": -55.5230, "region": "Oeste"},
    "b° camba cua": {"nombre": "Camba Cuá", "zona": "Oeste", "lat": -27.4920, "lon": -55.5230, "region": "Oeste"},
    "b° camba cuá": {"nombre": "Camba Cuá", "zona": "Oeste", "lat": -27.4920, "lon": -55.5230, "region": "Oeste"},
    "bº camba cua": {"nombre": "Camba Cuá", "zona": "Oeste", "lat": -27.4920, "lon": -55.5230, "region": "Oeste"},
    "barrio camba cua": {"nombre": "Camba Cuá", "zona": "Oeste", "lat": -27.4920, "lon": -55.5230, "region": "Oeste"},
    "barrio camba cuá": {"nombre": "Camba Cuá", "zona": "Oeste", "lat": -27.4920, "lon": -55.5230, "region": "Oeste"},
    
    "libertad": {"nombre": "Libertad", "zona": "Oeste", "lat": -27.4950, "lon": -55.5280, "region": "Oeste"},
    "barrio libertad": {"nombre": "Libertad", "zona": "Oeste", "lat": -27.4950, "lon": -55.5280, "region": "Oeste"},
    "b° libertad": {"nombre": "Libertad", "zona": "Oeste", "lat": -27.4950, "lon": -55.5280, "region": "Oeste"},
    
    "la cruz": {"nombre": "La Cruz", "zona": "Norte", "lat": -27.4600, "lon": -55.5100, "region": "Norte"},
    "barrio la cruz": {"nombre": "La Cruz", "zona": "Norte", "lat": -27.4600, "lon": -55.5100, "region": "Norte"},
    "b° la cruz": {"nombre": "La Cruz", "zona": "Norte", "lat": -27.4600, "lon": -55.5100, "region": "Norte"},
    
    "apipe": {"nombre": "Apipé", "zona": "Este", "lat": -27.4750, "lon": -55.4850, "region": "Este"},
    "apipé": {"nombre": "Apipé", "zona": "Este", "lat": -27.4750, "lon": -55.4850, "region": "Este"},
    "barrio apipe": {"nombre": "Apipé", "zona": "Este", "lat": -27.4750, "lon": -55.4850, "region": "Este"},
    "barrio apipé": {"nombre": "Apipé", "zona": "Este", "lat": -27.4750, "lon": -55.4850, "region": "Este"},
    
    "san juan": {"nombre": "San Juan", "zona": "Centro", "lat": -27.4850, "lon": -55.5050, "region": "Central"},
    "barrio san juan": {"nombre": "San Juan", "zona": "Centro", "lat": -27.4850, "lon": -55.5050, "region": "Central"},
    
    "belgrano": {"nombre": "Belgrano", "zona": "Centro", "lat": -27.4880, "lon": -55.5080, "region": "Central"},
    "barrio belgrano": {"nombre": "Belgrano", "zona": "Centro", "lat": -27.4880, "lon": -55.5080, "region": "Central"},
}

def normalizar_barrio(barrio):
    if pd.isna(barrio):
        return None, None, None, None, None
    
    barrio_limpio = str(barrio).lower().strip()
    
    if barrio_limpio in barrios_normalizacion:
        info = barrios_normalizacion[barrio_limpio]
        return info["nombre"], info["zona"], info["lat"], info["lon"], info["region"]
    
    claves = list(barrios_normalizacion.keys())
    similares = get_close_matches(barrio_limpio, claves, n=1, cutoff=0.80)
    
    if similares:
        info = barrios_normalizacion[similares[0]]
        return info["nombre"], info["zona"], info["lat"], info["lon"], info["region"]
    
    return barrio, None, None, None, None

df[["barrio_normalizado", "zona", "latitud", "longitud", "region"]] = df["ubicacion"].apply(
    lambda x: pd.Series(normalizar_barrio(x))
)

print(f"\nBarrios únicos originales: {df['ubicacion'].nunique()}")
print(f"Barrios normalizados: {df['barrio_normalizado'].nunique()}")
print(f"Barrios sin mapeo: {df[df['zona'].isna()]['barrio_normalizado'].nunique()}")

print("\n" + "=" * 90)
print("2. ANÁLISIS DE AVISOS POR ZONA")
print("=" * 90)

df_con_zona = df[df["zona"].notna()]

zona_stats = []
for zona in sorted(df_con_zona["zona"].unique()):
    subset = df_con_zona[df_con_zona["zona"] == zona]
    precio_subset = subset[subset["precio"].notna() & (pd.to_numeric(subset["precio"], errors="coerce") > 0)]
    
    stats = {
        "Zona": zona,
        "Total Avisos": len(subset),
        "% del Total": f"{len(subset) / len(df) * 100:.1f}%",
        "Con Precio": len(precio_subset),
        "% Precio": f"{len(precio_subset) / len(subset) * 100:.1f}%",
        "Avisos Válidos*": len(subset[(subset["precio"].notna() | subset["ubicacion"].notna())]),
    }
    zona_stats.append(stats)

zona_df = pd.DataFrame(zona_stats).sort_values("Total Avisos", ascending=False)
print("\n* Avisos válidos = tienen al menos barrio o precio")
print(zona_df.to_string(index=False))


print("\n" + "=" * 90)
print("3. TOP BARRIOS POR CANTIDAD DE AVISOS")
print("=" * 90)

barrio_stats = []
for barrio in df_con_zona["barrio_normalizado"].value_counts().head(20).index:
    subset = df_con_zona[df_con_zona["barrio_normalizado"] == barrio]
    precio_subset = subset[subset["precio"].notna() & (pd.to_numeric(subset["precio"], errors="coerce") > 0)]
    zona = subset["zona"].iloc[0]
    
    if len(precio_subset) > 0:
        precio_medio = precio_subset["precio"].astype(float).mean()
    else:
        precio_medio = 0
    
    stats = {
        "Barrio": barrio,
        "Zona": zona,
        "Total": len(subset),
        "Con Precio": len(precio_subset),
        "% Precio": f"{len(precio_subset) / len(subset) * 100:.1f}%",
        "Precio Promedio": f"${precio_medio:,.0f}" if precio_medio > 0 else "N/A"
    }
    barrio_stats.append(stats)

barrio_df = pd.DataFrame(barrio_stats)
print(barrio_df.to_string(index=False))


print("\n" + "=" * 90)
print("4. SISTEMA DE VALIDACIÓN: AVISOS 'ENVIABLES' vs 'BASURA'")
print("=" * 90)

def validar_aviso(row):
    """Determina si un aviso es válido para enviar al usuario"""
    
    if pd.isna(row["barrio_normalizado"]) or pd.isna(row["zona"]):
        return "RECHAZADO", "Sin ubicación clara"
    
    precio = pd.to_numeric(row["precio"], errors="coerce")
    if pd.isna(precio) or precio <= 0:
        return "RECHAZADO", "Sin precio válido"
    
    if precio < 11 or precio > 195000000:
        return "RECHAZADO", "Precio fuera de rango"
    
    if pd.notna(row["post_descripcion"]):
        emoji_pattern = r'[😀-🙏🌀-🗿🚀-🛿]'
        if re.search(emoji_pattern, str(row["post_descripcion"])):
            return "ADVERTENCIA", "Contiene emojis (validar)"
    
    text_length = len(str(row["post_descripcion"]).strip()) if pd.notna(row["post_descripcion"]) else 0
    if text_length < 50:
        return "ADVERTENCIA", "Descripción muy corta"
    
    if row["source"] in ["instagram", "RE/MAX"]:
        return "ADVERTENCIA", f"Fuente {row['source']} (baja confiabilidad)"
    
    return "VÁLIDO", "Apto para envío"

df[["validez", "motivo"]] = df.apply(
    lambda row: pd.Series(validar_aviso(row)), axis=1
)

print("\nResumen de validación:")
validez_resumen = df["validez"].value_counts()
for validez, count in validez_resumen.items():
    porcentaje = (count / len(df) * 100)
    print(f"  {validez}: {count} avisos ({porcentaje:.1f}%)")

print("\nTop motivos de rechazo:")
rechazados = df[df["validez"] == "RECHAZADO"]
motivos = rechazados["motivo"].value_counts().head(10)
for motivo, count in motivos.items():
    print(f"  - {motivo}: {count}")

print("\n" + "=" * 90)
print("5. EJEMPLO DE FORMATO DE MENSAJE PARA BOT")
print("=" * 90)

def generar_mensaje_bot(row):
    """Genera mensaje limpio para enviar al usuario"""
    
    if row["validez"] != "VÁLIDO":
        return None
    
    barrio = row["barrio_normalizado"]
    zona = row["zona"]
    
    precio = pd.to_numeric(row["precio"], errors="coerce")
    precio_str = f"${precio:,.0f}" if precio > 0 else "Consultar"
    
    super_cubierta = row["superficie_cubierta"]
    super_total = row["superficie_total"]
    super_str = ""
    if pd.notna(super_cubierta) and super_cubierta > 0:
        super_str = f"{super_cubierta:.0f} m2"
    elif pd.notna(super_total) and super_total > 0:
        super_str = f"{super_total:.0f} m2"
    
    hab = row["habitaciones"]
    hab_str = f"{int(hab)} dorm" if pd.notna(hab) and hab > 0 and hab <= 10 else ""
    
    tipo = row["tipo_propiedad"]
    tipo_str = str(tipo).title() if pd.notna(tipo) else "Propiedad"
    
    operacion = row["tipo_operacion"]
    
    mensaje = f"{tipo_str} - {barrio}, {zona}\n"
    
    detalles = []
    detalles.append(f"Precio: {precio_str}")
    if super_str:
        detalles.append(f"Superficie: {super_str}")
    if hab_str:
        detalles.append(hab_str)
    detalles.append(f"Operación: {operacion.title() if pd.notna(operacion) else 'Consultar'}")
    
    mensaje += " | ".join(detalles) + "\n"
    
    if pd.notna(row["Ogappy Link"]):
        mensaje += f"Enlace: {row['Ogappy Link']}"
    
    return mensaje

validos = df[df["validez"] == "VÁLIDO"].head(5)
print("\nEJEMPLOS DE MENSAJES PARA ENVIAR AL USUARIO:\n")
for idx, (i, row) in enumerate(validos.iterrows(), 1):
    msg = generar_mensaje_bot(row)
    if msg:
        print(f"--- Ejemplo {idx} ---")
        print(msg)
        print()


print("=" * 90)
print("6. CALIDAD DE DATOS POR ZONA (para tomar decisiones de envío)")
print("=" * 90)


print("\n" + "=" * 90)
print("6. CALIDAD DE DATOS POR ZONA (para tomar decisiones de envío)")
print("=" * 90)

calidad_zona = []
for zona in sorted(df_con_zona["zona"].unique()):
    subset = df[df["zona"] == zona]
    validos = subset[subset["validez"] == "VÁLIDO"]
    
    calidad = {
        "Zona": zona,
        "Total Avisos": len(subset),
        "Avisos Válidos": len(validos),
        "% Válidos": f"{len(validos) / len(subset) * 100:.1f}%",
        "Confiabilidad": "ALTA" if len(validos) / len(subset) > 0.7 else "MEDIA" if len(validos) / len(subset) > 0.4 else "BAJA"
    }
    calidad_zona.append(calidad)

calidad_zona_df = pd.DataFrame(calidad_zona).sort_values("% Válidos", ascending=False, key=lambda x: x.str.rstrip("%").astype(float))
print(calidad_zona_df.to_string(index=False))


print("\n" + "=" * 90)
print("7. RECOMENDACIONES FINALES PARA IMPLEMENTAR EL BOT")
print("=" * 90)



zonas_confiables = calidad_zona_df[calidad_zona_df["Confiabilidad"] == "ALTA"]["Zona"].tolist()
if zonas_confiables:
    print(f"   - {', '.join(zonas_confiables)}")




print("\n" + "=" * 90)
print("8. GUARDANDO DATASET ENRIQUECIDO")
print("=" * 90)

df_enriquecido = df[[
    "Ogappy Link",
    "barrio_normalizado",
    "zona",
    "region",
    "latitud",
    "longitud",
    "ubicacion",
    "tipo_propiedad",
    "tipo_operacion",
    "precio",
    "superficie_cubierta",
    "superficie_total",
    "habitaciones",
    "post_descripcion",
    "source",
    "validez",
    "motivo",
    "inmobiliaria"
]].copy()

# Guardar
enriched_path = os.path.expanduser("~/Downloads/dataset_enriquecido_geo.xlsx")
df_enriquecido.to_excel(enriched_path, index=False)

print(f"\nDataset enriquecido guardado en: {enriched_path}")
print(f"Columnas agregadas:")
print(f"  - barrio_normalizado")
print(f"  - zona (Centro, Oeste, Este, Norte)")
print(f"  - region")
print(f"  - latitud, longitud")
print(f"  - validez (VÁLIDO, ADVERTENCIA, RECHAZADO)")
print(f"  - motivo (razón de rechazo)")

normalizacion_df = pd.DataFrame([
    {
        "Zona": info["zona"],
        "Región": info["region"],
        "Latitud": info["lat"],
        "Longitud": info["lon"],
        "Barrio Estándar": info["nombre"],
        "Variantes": ", ".join([k for k, v in barrios_normalizacion.items() if v["nombre"] == info["nombre"]])
    }
    for nombre, info in {v["nombre"]: v for v in barrios_normalizacion.values()}.items()
]).drop_duplicates(subset=["Barrio Estándar"])

normalizacion_path = os.path.expanduser("~/Downloads/tabla_normalizacion_barrios.xlsx")
normalizacion_df.to_excel(normalizacion_path, index=False)

print(f"\nTabla de normalización guardada en: {normalizacion_path}")

stats_path = os.path.expanduser("~/Downloads/estadisticas_geo_por_zona.xlsx")
with pd.ExcelWriter(stats_path) as writer:
    zona_df.to_excel(writer, sheet_name="Por Zona", index=False)
    barrio_df.to_excel(writer, sheet_name="Top Barrios", index=False)
    calidad_zona_df.to_excel(writer, sheet_name="Calidad por Zona", index=False)

print(f"Estadísticas por zona guardadas en: {stats_path}")
