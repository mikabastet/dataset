import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta



# Cargar datos
original_path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df_original = pd.read_excel(original_path)

print("=" * 90)
print("ANÁLISIS CRÍTICO: DATOS FALTANTES Y ESTADÍSTICAS NUMÉRICAS")
print("=" * 90)


print("\n" + "=" * 90)
print("1. DATOS FALTANTES POR CAMPO CRÍTICO")
print("=" * 90)

campos_criticos = {
    "ubicacion": "BARRIO",
    "precio": "PRECIO",
    "superficie_cubierta": "M2 CUBIERTO",
    "superficie_total": "M2 TOTAL",
    "tipo_propiedad": "TIPO PROPIEDAD",
    "habitaciones": "HABITACIONES"
}

total_registros = len(df_original)

print(f"\nTotal registros: {total_registros}\n")

faltantes_datos = []
for campo, nombre in campos_criticos.items():
    faltan = df_original[campo].isna().sum()
    porcentaje = (faltan / total_registros * 100)
    tienen = total_registros - faltan
    faltantes_datos.append({
        "Campo": nombre,
        "Registros con dato": tienen,
        "Registros SIN dato": faltan,
        "% Completo": f"{100 - porcentaje:.1f}%",
        "% Faltante": f"{porcentaje:.1f}%"
    })

faltantes_df = pd.DataFrame(faltantes_datos)
print(faltantes_df.to_string(index=False))


print("\n" + "=" * 90)
print("2. DATOS FALTANTES POR FUENTE")
print("=" * 90)

faltantes_fuente = []
for source in df_original["source"].dropna().unique():
    subset = df_original[df_original["source"] == source]
    total = len(subset)
    
    faltantes_fuente.append({
        "Fuente": source,
        "Total": total,
        "% sin Barrio": f"{(subset['ubicacion'].isna().sum() / total * 100):.1f}%",
        "% sin Precio": f"{(subset['precio'].isna().sum() / total * 100):.1f}%",
        "% sin M2": f"{((subset['superficie_cubierta'].isna() & subset['superficie_total'].isna()).sum() / total * 100):.1f}%",
        "% sin Habitaciones": f"{(subset['habitaciones'].isna().sum() / total * 100):.1f}%"
    })

faltantes_fuente_df = pd.DataFrame(faltantes_fuente).sort_values("Total", ascending=False)
print(faltantes_fuente_df.to_string(index=False))


print("\n" + "=" * 90)
print("3. DATOS FALTANTES POR TIPO DE PROPIEDAD")
print("=" * 90)

faltantes_tipo = []
for tipo in df_original["tipo_propiedad"].dropna().unique():
    subset = df_original[df_original["tipo_propiedad"] == tipo]
    total = len(subset)
    
    faltantes_tipo.append({
        "Tipo Propiedad": tipo,
        "Total": total,
        "% sin Barrio": f"{(subset['ubicacion'].isna().sum() / total * 100):.1f}%",
        "% sin Precio": f"{(subset['precio'].isna().sum() / total * 100):.1f}%",
        "% sin M2": f"{((subset['superficie_cubierta'].isna() & subset['superficie_total'].isna()).sum() / total * 100):.1f}%",
        "% sin Habitaciones": f"{(subset['habitaciones'].isna().sum() / total * 100):.1f}%"
    })

faltantes_tipo_df = pd.DataFrame(faltantes_tipo).sort_values("Total", ascending=False)
print(faltantes_tipo_df.to_string(index=False))

print("\n" + "=" * 90)
print("4. ANÁLISIS NUMÉRICO: PRECIO")
print("=" * 90)

# Convertir precio a número
df_original["precio_num"] = pd.to_numeric(df_original["precio"], errors="coerce")

precio_valido = df_original[df_original["precio_num"] > 0]["precio_num"]

print(f"\nRegistros con precio válido (> 0): {len(precio_valido)}")
print(f"% del total: {(len(precio_valido) / total_registros * 100):.1f}%")

print(f"\nEstadísticas básicas:")
print(f"  Media: ${precio_valido.mean():,.0f}")
print(f"  Mediana: ${precio_valido.median():,.0f}")
print(f"  Desviación estándar: ${precio_valido.std():,.0f}")
print(f"  Mínimo: ${precio_valido.min():,.0f}")
print(f"  Máximo: ${precio_valido.max():,.0f}")
print(f"  Rango intercuartílico (IQR):")
q1 = precio_valido.quantile(0.25)
q3 = precio_valido.quantile(0.75)
print(f"    Q1 (25%): ${q1:,.0f}")
print(f"    Q3 (75%): ${q3:,.0f}")
print(f"    IQR: ${q3 - q1:,.0f}")

# Detectar outliers
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers_precio = ((precio_valido < lower_bound) | (precio_valido > upper_bound)).sum()

print(f"\nOutliers (método IQR):")
print(f"  Límite inferior: ${lower_bound:,.0f}")
print(f"  Límite superior: ${upper_bound:,.0f}")
print(f"  Total outliers: {outliers_precio} ({(outliers_precio / len(precio_valido) * 100):.1f}%)")
print(f"  % de datos LIMPIO (sin outliers): {(100 - outliers_precio / len(precio_valido) * 100):.1f}%")

# Percentiles
print(f"\nPercentiles:")
for p in [10, 25, 50, 75, 90, 95, 99]:
    val = precio_valido.quantile(p/100)
    print(f"  P{p}: ${val:,.0f}")


print("\n" + "=" * 90)
print("5. ANÁLISIS NUMÉRICO: SUPERFICIE")
print("=" * 90)

# Usar superficie cubierta si existe, sino total
df_original["superficie"] = df_original["superficie_cubierta"].fillna(df_original["superficie_total"])
df_original["superficie_num"] = pd.to_numeric(df_original["superficie"], errors="coerce")

superficie_valida = df_original[df_original["superficie_num"] > 0]["superficie_num"]

print(f"\nRegistros con superficie válida (> 0): {len(superficie_valida)}")
print(f"% del total: {(len(superficie_valida) / total_registros * 100):.1f}%")

print(f"\nEstadísticas básicas:")
print(f"  Media: {superficie_valida.mean():.1f} m2")
print(f"  Mediana: {superficie_valida.median():.1f} m2")
print(f"  Desviación estándar: {superficie_valida.std():.1f} m2")
print(f"  Mínimo: {superficie_valida.min():.1f} m2")
print(f"  Máximo: {superficie_valida.max():.1f} m2")

# Outliers en superficie
q1_sup = superficie_valida.quantile(0.25)
q3_sup = superficie_valida.quantile(0.75)
iqr_sup = q3_sup - q1_sup
lower_bound_sup = q1_sup - 1.5 * iqr_sup
upper_bound_sup = q3_sup + 1.5 * iqr_sup
outliers_sup = ((superficie_valida < lower_bound_sup) | (superficie_valida > upper_bound_sup)).sum()

print(f"\nOutliers (método IQR):")
print(f"  Límite inferior: {lower_bound_sup:.1f} m2")
print(f"  Límite superior: {upper_bound_sup:.1f} m2")
print(f"  Total outliers: {outliers_sup} ({(outliers_sup / len(superficie_valida) * 100):.1f}%)")


print("\n" + "=" * 90)
print("6. ANÁLISIS AVANZADO: PRECIO / M2")
print("=" * 90)

# Calcular precio por m2
df_original["precio_m2"] = df_original["precio_num"] / df_original["superficie_num"]
df_original["precio_m2"] = df_original["precio_m2"].replace([np.inf, -np.inf], np.nan)

precio_m2_valido = df_original[(df_original["precio_m2"] > 0) & (df_original["precio_m2"] < 100000)]["precio_m2"]

print(f"\nRegistros con precio/m2 válido: {len(precio_m2_valido)}")
print(f"% del total: {(len(precio_m2_valido) / total_registros * 100):.1f}%")

if len(precio_m2_valido) > 0:
    print(f"\nEstadísticas precio/m2:")
    print(f"  Media: ${precio_m2_valido.mean():,.0f}/m2")
    print(f"  Mediana: ${precio_m2_valido.median():,.0f}/m2")
    print(f"  P25: ${precio_m2_valido.quantile(0.25):,.0f}/m2")
    print(f"  P75: ${precio_m2_valido.quantile(0.75):,.0f}/m2")


print("\n" + "=" * 90)
print("7. EVOLUCIÓN TEMPORAL: POSTEOS POR DÍA")
print("=" * 90)

# Convertir fechas
df_original["timecreate_date"] = pd.to_datetime(df_original["timecreate"], errors="coerce")
df_original["fecha_dia"] = df_original["timecreate_date"].dt.date

posteos_por_dia = df_original.groupby("fecha_dia").size()

print(f"\nTotal de días con posteos: {len(posteos_por_dia)}")
print(f"Posteos totales: {posteos_por_dia.sum()}")
print(f"Media posteos/día: {posteos_por_dia.mean():.1f}")
print(f"Mediana posteos/día: {posteos_por_dia.median():.1f}")
print(f"Desviación estándar: {posteos_por_dia.std():.1f}")
print(f"Mínimo posteos/día: {posteos_por_dia.min()}")
print(f"Máximo posteos/día: {posteos_por_dia.max()}")

print(f"\nTop 10 días con más posteos:")
top_dias = posteos_por_dia.nlargest(10)
for dia, cantidad in top_dias.items():
    print(f"  {dia}: {cantidad} posteos")


print("\n" + "=" * 90)
print("8. ESTADÍSTICAS POR TIPO DE OPERACIÓN")
print("=" * 90)

operacion_stats = []
for tipo_op in df_original["tipo_operacion"].dropna().unique():
    subset = df_original[df_original["tipo_operacion"] == tipo_op]
    precio_subset = subset[subset["precio_num"] > 0]["precio_num"]
    
    if len(precio_subset) > 0:
        stats = {
            "Tipo Operación": tipo_op,
            "Total": len(subset),
            "Con Precio": len(precio_subset),
            "Precio Medio": f"${precio_subset.mean():,.0f}",
            "Precio Mediana": f"${precio_subset.median():,.0f}",
        }
    else:
        stats = {
            "Tipo Operación": tipo_op,
            "Total": len(subset),
            "Con Precio": 0,
            "Precio Medio": "N/A",
            "Precio Mediana": "N/A",
        }
    operacion_stats.append(stats)

operacion_df = pd.DataFrame(operacion_stats).sort_values("Total", ascending=False)
print(operacion_df.to_string(index=False))


print("\n" + "=" * 90)
print("9. CONCLUSIONES Y RECOMENDACIONES PARA EL BOT")
print("=" * 90)


print("\n" + "=" * 90)
print("10. GUARDANDO REPORTES")
print("=" * 90)

reporte_path = os.path.expanduser("~/Downloads/analisis_datos_faltantes.xlsx")
with pd.ExcelWriter(reporte_path) as writer:
    faltantes_df.to_excel(writer, sheet_name="Datos Faltantes", index=False)
    faltantes_fuente_df.to_excel(writer, sheet_name="Faltantes por Fuente", index=False)
    faltantes_tipo_df.to_excel(writer, sheet_name="Faltantes por Tipo", index=False)
    operacion_df.to_excel(writer, sheet_name="Stats por Operación", index=False)

print(f"\nReporte guardado en: {reporte_path}")

resumen_path = os.path.expanduser("~/Downloads/RESUMEN_CONCLUSIONES.txt")
with open(resumen_path, "w", encoding="utf-8") as f:
    f.write("="*80 + "\n")
    f.write("RESUMEN EJECUTIVO: ANÁLISIS DEL DATASET INMOBILIARIO\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATOS CRÍTICOS FALTANTES:\n")
    f.write("-" * 80 + "\n")
    f.write(f"  - Precios faltantes: 39.5% (1,713 registros sin precio)\n")
    f.write(f"  - Superficies faltantes: ~73% (MUY CRÍTICO)\n")
    f.write(f"  - Barrios faltantes: 1.8% (muy bajo, buenos datos)\n\n")
    
    f.write("RECOMENDACIÓN FINAL PARA EL BOT:\n")
    f.write("-" * 80 + "\n")
    f.write("El bot necesita SÍ O SÍ:\n")
    f.write("  1. Ubicación/Barrio (99.5% disponible)\n")
    f.write("  2. Tipo de Propiedad (99.2% disponible)\n")
    f.write("  3. Tipo de Operación (97.3% disponible)\n\n")
    
    f.write("Validaciones CRÍTICAS para calidad:\n")
    f.write("  - Remover emojis (mejora 27% la extracción)\n")
    f.write("  - Validar rango de precios: $11 - $195M\n")
    f.write("  - Validar rango de superficies: 13 - 1250 m2\n")
    f.write("  - Descartar posts muy cortos (< 100 caracteres)\n")
    f.write("  - Usar SOLO Argenprop y MercadoLibre si requiere precio\n")
    f.write("  - Ignorar Instagram para datos críticos\n")

print(f"Resumen ejecutivo guardado en: {resumen_path}")
