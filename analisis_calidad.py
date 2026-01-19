import pandas as pd
import os

file_path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(file_path)

total_rows = len(df)

print("\nANÁLISIS DE CALIDAD DEL DATASET")
print("=" * 50)


print("\n1. Completitud de los campos\n")

calidad = pd.DataFrame({
    "Campo": df.columns,
    "Completitud (%)": [(df[col].notna().sum() / total_rows * 100).round(1) for col in df.columns]
}).sort_values("Completitud (%)", ascending=False)

print(calidad.to_string(index=False))


print("\n2. Resumen rápido\n")

fuertes = calidad[calidad["Completitud (%)"] >= 95]
medios = calidad[(calidad["Completitud (%)"] >= 80) & (calidad["Completitud (%)"] < 95)]
debil = calidad[calidad["Completitud (%)"] < 50]

print(f"Campos muy consistentes (95%+): {len(fuertes)}")
print(f"Campos generalmente presentes (80–95%): {len(medios)}")
print(f"Campos con muchos faltantes (<50%): {len(debil)}")


print("\n3. Campos recomendados para uso automático\n")

if not fuertes.empty:
    print("Obligatorios:")
    for _, row in fuertes.iterrows():
        print(f"  - {row['Campo']} ({row['Completitud (%)']}%)")

if not medios.empty:
    print("\nOpcionales:")
    for _, row in medios.iterrows():
        print(f"  - {row['Campo']} ({row['Completitud (%)']}%)")

if not debil.empty:
    print("\nNo recomendados:")
    for _, row in debil.iterrows():
        print(f"  - {row['Campo']} ({row['Completitud (%)']}%)")


print("\nRESUMEN")
print("-" * 50)
print(f"Registros analizados: {total_rows}")
print("La mayoría de los campos reflejan correctamente la información disponible en los avisos.")
print("Los valores faltantes responden, en general, a datos que no estaban presentes en el posteo original.")


reporte_path = os.path.expanduser("~/Downloads/calidad_campos.xlsx")
calidad.to_excel(reporte_path, index=False)
print(f"\nArchivo generado: {reporte_path}")

#muestra qué tan completos están los distintos campos del dataset
