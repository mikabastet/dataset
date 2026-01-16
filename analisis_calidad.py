import pandas as pd
import os


file_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(file_path)

print("=" * 70)
print("ANÁLISIS DE CALIDAD DEL DATASET")
print("=" * 70)


print("\n1. PORCENTAJE DE COMPLETITUD POR CAMPO")
print("-" * 70)

null_count = df.isna().sum()
non_null_count = df.notna().sum()
total_rows = len(df)

calidad = pd.DataFrame({
    "Campo": df.columns,
    "No Nulos": [non_null_count[col] for col in df.columns],
    "Nulos": [null_count[col] for col in df.columns],
    "% No Nulos": [(non_null_count[col] / total_rows * 100).round(2) for col in df.columns],
    "% Nulos": [(null_count[col] / total_rows * 100).round(2) for col in df.columns]
})

calidad_ordenada = calidad.sort_values("% Nulos")

print(calidad_ordenada.to_string(index=False))


print("\n" + "=" * 70)
print("2. RANKING DE CAMPOS MÁS DÉBILES (Mayor % de nulos)")
print("=" * 70)

debiles = calidad_ordenada.tail(10).copy()
debiles["Ranking"] = range(10, 0, -1)
print(debiles[["Ranking", "Campo", "% Nulos", "% No Nulos"]].to_string(index=False))
print("\n" + "=" * 70)
print("3. RANKING DE CAMPOS MÁS FUERTES (Menor % de nulos)")
print("=" * 70)
fuertes = calidad_ordenada.head(10).copy()
fuertes["Ranking"] = range(1, 11)
print(fuertes[["Ranking", "Campo", "% Nulos", "% No Nulos"]].to_string(index=False))

print("\n" + "=" * 70)
print("4. CLASIFICACIÓN DE CAMPOS POR CALIDAD")
print("=" * 70)

calidad["Clasificación"] = calidad["% No Nulos"].apply(
    lambda x: "EXCELENTE (95%+)" if x >= 95 
    else "BUENO (80-95%)" if x >= 80
    else "ACEPTABLE (50-80%)" if x >= 50
    else "DÉBIL (20-50%)" if x >= 20
    else "MUY DÉBIL (<20%)"
)

print("\nCampos por nivel de calidad:")
for clasificacion in ["EXCELENTE (95%+)", "BUENO (80-95%)", "ACEPTABLE (50-80%)", "DÉBIL (20-50%)", "MUY DÉBIL (<20%)"]:
    campos = calidad[calidad["Clasificación"] == clasificacion]
    if len(campos) > 0:
        print(f"\n{clasificacion}:")
        for idx, row in campos.iterrows():
            print(f"  - {row['Campo']}: {row['% No Nulos']}%")


print("\n" + "=" * 70)
print("5. RECOMENDACIÓN: CAMPOS OBLIGATORIOS PARA EL BOT")
print("=" * 70)

campos_obligatorios = calidad[calidad["% No Nulos"] >= 95]["Campo"].tolist()

print(f"\nCampos con 95%+ completitud (RECOMENDADO como obligatorios):")
for campo in campos_obligatorios:
    completitud = calidad[calidad["Campo"] == campo]["% No Nulos"].values[0]
    print(f"  - {campo}: {completitud}%")

campos_recomendados = calidad[(calidad["% No Nulos"] >= 80) & (calidad["% No Nulos"] < 95)]["Campo"].tolist()

if campos_recomendados:
    print(f"\nCampos con 80-95% completitud (RECOMENDADO como opcionales):")
    for campo in campos_recomendados:
        completitud = calidad[calidad["Campo"] == campo]["% No Nulos"].values[0]
        print(f"  - {campo}: {completitud}%")

campos_evitar = calidad[calidad["% No Nulos"] < 50]["Campo"].tolist()

if campos_evitar:
    print(f"\nCampos a EVITAR en el bot (menos del 50% completitud):")
    for campo in campos_evitar:
        completitud = calidad[calidad["Campo"] == campo]["% No Nulos"].values[0]
        print(f"  - {campo}: {completitud}%")


print("\n" + "=" * 70)
print("6. ANÁLISIS DE FALLOS SISTEMÁTICOS")
print("=" * 70)

print("\nPatrones sospechosos detectados:\n")

numeric_cols = ["precio", "habitaciones", "banos", "ambientes", "antiguedad", "superficie_cubierta", "superficie_total"]

for col in numeric_cols:
    if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
        valid = df[col].notna().sum()
        invalid = df[col].isna().sum()
        
        if valid > 0:
            media = df[col].mean()
            mediana = df[col].median()
            min_val = df[col].min()
            max_val = df[col].max()
            anomalias = []
            
            # Valores 0
            zeros = (df[col] == 0).sum()
            if zeros > 0:
                anomalias.append(f"{zeros} valores en 0")
            
            negatives = (df[col] < 0).sum()
            if negatives > 0:
                anomalias.append(f"{negatives} valores negativos")
            
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = ((df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)).sum()
            if outliers > 0:
                anomalias.append(f"{outliers} outliers")
            
            print(f"{col}:")
            print(f"  Completitud: {valid}/{len(df)} ({valid/len(df)*100:.1f}%)")
            print(f"  Rango: [{min_val:.1f} - {max_val:.1f}]")
            print(f"  Media: {media:.2f} | Mediana: {mediana:.2f}")
            if anomalias:
                print(f"  Anomalías: {', '.join(anomalias)}")
            print()


print("=" * 70)
print("7. ANÁLISIS DE CAMPOS DE TEXTO")
print("=" * 70)

text_cols = ["titulo", "post_descripcion", "ubicacion", "inmobiliaria", "source"]

for col in text_cols:
    if col in df.columns:
        valid = df[col].notna().sum()
        empty_strings = (df[col] == "").sum() if df[col].dtype == "object" else 0
        avg_length = df[col].fillna("").str.len().mean()
        
        print(f"\n{col}:")
        print(f"  Completitud: {valid}/{len(df)} ({valid/len(df)*100:.1f}%)")
        print(f"  Strings vacíos: {empty_strings}")
        print(f"  Longitud promedio: {avg_length:.1f} caracteres")


print("\n" + "=" * 70)
print("RESUMEN EJECUTIVO")
print("=" * 70)

print(f"\nTotal de registros: {len(df)}")
print(f"Total de campos: {len(df.columns)}")
print(f"\nCampos de calidad EXCELENTE (95%+): {len(calidad[calidad['% No Nulos'] >= 95])}")
print(f"Campos de calidad BUENA (80-95%): {len(calidad[(calidad['% No Nulos'] >= 80) & (calidad['% No Nulos'] < 95)])}")
print(f"Campos de calidad ACEPTABLE (50-80%): {len(calidad[(calidad['% No Nulos'] >= 50) & (calidad['% No Nulos'] < 80)])}")
print(f"Campos de calidad DÉBIL (<50%): {len(calidad[calidad['% No Nulos'] < 50])}")

reporte_path = os.path.expanduser("~/Downloads/analisis_calidad.xlsx")
with pd.ExcelWriter(reporte_path) as writer:
    calidad_ordenada.to_excel(writer, sheet_name="Calidad Campos", index=False)
    
print(f"\nReporte guardado en: {reporte_path}")
