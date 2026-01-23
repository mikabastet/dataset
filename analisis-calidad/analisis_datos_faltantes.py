import pandas as pd
import os
import numpy as np

path = os.path.expanduser("~/Downloads/Ogappy_14_01_2026.xlsx")
df = pd.read_excel(path)
total = len(df)

print("=" * 50)
print(f"egistros analizados: {total}")

print("\n1. Completitud de campos clave\n")

campos = {
    "ubicacion": "Barrio",
    "precio": "Precio",
    "superficie_cubierta": "M2 cubiertos",
    "superficie_total": "M2 totales",
    "tipo_propiedad": "Tipo de propiedad",
    "habitaciones": "Habitaciones"
}

resumen = []
for col, nombre in campos.items():
    completos = df[col].notna().sum()
    resumen.append({
        "Campo": nombre,
        "Completitud (%)": round(completos / total * 100, 1)
    })

faltantes_df = pd.DataFrame(resumen).sort_values("Completitud (%)", ascending=False)
print(faltantes_df.to_string(index=False))

fuentes = []
for src in df["source"].dropna().unique():
    sub = df[df["source"] == src]
    fuentes.append({
        "Fuente": src,
        "Total": len(sub),
        "% sin precio": round(sub["precio"].isna().mean() * 100, 1),
        "% sin barrio": round(sub["ubicacion"].isna().mean() * 100, 1)
    })

fuentes_df = pd.DataFrame(fuentes).sort_values("Total", ascending=False)
print(fuentes_df.to_string(index=False))

df["precio_num"] = pd.to_numeric(df["precio"], errors="coerce")
precios = df[df["precio_num"] > 0]["precio_num"]
print(f"Registros con precio válido: {len(precios)} ({len(precios)/total*100:.1f}%)")
if len(precios) > 0:
    print(f"Precio medio: ${precios.mean():,.0f}")
    print(f"Precio mediano: ${precios.median():,.0f}")
    print(f"Rango típico: ${precios.quantile(0.25):,.0f} – ${precios.quantile(0.75):,.0f}")

df["superficie"] = pd.to_numeric(
    df["superficie_cubierta"].fillna(df["superficie_total"]),
    errors="coerce"
)
sup = df[df["superficie"] > 0]["superficie"]
print(f"Registros con superficie válida: {len(sup)} ({len(sup)/total*100:.1f}%)")
if len(sup) > 0:
    print(f"Superficie media: {sup.mean():.1f} m2")
    print(f"Superficie mediana: {sup.median():.1f} m2")


df["precio_m2"] = df["precio_num"] / df["superficie"]
precio_m2 = df[(df["precio_m2"] > 0) & (df["precio_m2"] < 100000)]["precio_m2"]
print(f"Registros con precio/m2 válido: {len(precio_m2)}")
if len(precio_m2) > 0:
    print(f"Precio/m2 medio: ${precio_m2.mean():,.0f}")
    print(f"Rango típico: ${precio_m2.quantile(0.25):,.0f} – ${precio_m2.quantile(0.75):,.0f}")



df["fecha"] = pd.to_datetime(df["timecreate"], errors="coerce").dt.date
por_dia = df.groupby("fecha").size()

print(f"Días con actividad: {len(por_dia)}")
print(f"Promedio posteos/día: {por_dia.mean():.1f}")
print(f"Día más activo: {por_dia.idxmax()} ({por_dia.max()} posteos)")



stats = []
for op in df["tipo_operacion"].dropna().unique():
    sub = df[df["tipo_operacion"] == op]
    precios_op = sub[sub["precio_num"] > 0]["precio_num"]
    stats.append({
        "Tipo operación": op,
        "Total": len(sub),
        "Con precio": len(precios_op),
        "Precio medio": f"${precios_op.mean():,.0f}" if len(precios_op) > 0 else "N/A"
    })

operacion_df = pd.DataFrame(stats).sort_values("Total", ascending=False)
print(operacion_df.to_string(index=False))
print("\nCONCLUSIÓN")
print("-" * 50)

out = os.path.expanduser("~/Downloads/resumen_analisis.xlsx")
with pd.ExcelWriter(out) as writer:
    faltantes_df.to_excel(writer, sheet_name="Completitud", index=False)
    fuentes_df.to_excel(writer, sheet_name="Fuentes", index=False)
    operacion_df.to_excel(writer, sheet_name="Operaciones", index=False)

print(f"\nArchivo generado: {out}")

#ataset refleja  la información disponible en los avisos
#Los datos faltantes es principalmente a información no incluida en el posteo original
#Para automatización, ubicación, tipo de operación y tipo de propiedad son los campos más confiables