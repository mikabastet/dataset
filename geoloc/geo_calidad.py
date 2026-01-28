import pandas as pd
import os

file_path = os.path.expanduser("~/Downloads/dataset_geocodificado_completo.xlsx")
df = pd.read_excel(file_path)

muestra = df.sample(10, random_state=42)

output_path = r"C:\Users\mika\Downloads\muestra_revision_manual.xlsx"
muestra.to_excel(output_path, index=False)

print("Archivo generado en:", output_path)
#Muestra aleatoria de 50 avisos para revisión manual