import pandas as pd
import os

path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(path)

df["tipo_operacion"] = df["tipo_operacion"].str.lower().str.strip()
df["moneda"] = df["moneda"].str.upper().str.strip()

ventas_en_pesos = df[
    (df["tipo_operacion"].str.contains("venta", na=False)) &
    (df["moneda"] == "ARS")
]

alquileres_en_dolares = df[
    (df["tipo_operacion"].str.contains("alquiler", na=False)) &
    (df["moneda"] == "USD")
]

print("VENTAS EN PESOS:")
print(f"Total: {len(ventas_en_pesos)}")

print("\nALQUILERES EN DÓLARES:")
print(f"Total: {len(alquileres_en_dolares)}")

revision = pd.concat([
    ventas_en_pesos.assign(tipo_error="Venta en Pesos"),
    alquileres_en_dolares.assign(tipo_error="Alquiler en USD")
])

output_path = os.path.expanduser("~/Downloads/revision_moneda_vs_operacion.xlsx")
revision.to_excel(output_path, index=False)

print(f"\nEjemplos guardados para validación manual en:")
print(output_path)

output_path = os.path.expanduser("~/Downloads/revision_moneda_vs_operacion.xlsx")
revision.to_excel(output_path, index=False)


#alquileres en dolares 12
#ventas en peso 45 
#total 57 (1.3% del total)