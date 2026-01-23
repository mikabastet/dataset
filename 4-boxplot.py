import pandas as pd
import os
import matplotlib.pyplot as plt

path = os.path.expanduser("~/Downloads/datos_limpios.xlsx")
df = pd.read_excel(path)

df['precio_num'] = pd.to_numeric(df['precio'], errors='coerce')

precios_validos = df[df['precio_num'] > 0]

Q1 = precios_validos['precio_num'].quantile(0.25)
Q3 = precios_validos['precio_num'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers_bajos = precios_validos[precios_validos['precio_num'] < limite_inferior]
outliers_altos = precios_validos[precios_validos['precio_num'] > limite_superior]


print(f"Rangos esperados de precios (sin outliers):")
print(f"  - Límite inferior: ${limite_inferior:,.0f}")
print(f"  - Límite superior: ${limite_superior:,.0f}")
print(f"  - Cuartil 1 (Q1): ${Q1:,.0f}")
print(f"  - Cuartil 3 (Q3): ${Q3:,.0f}")
print(f"  - Rango Intercuartil (IQR): ${IQR:,.0f}")

print(f"\n Outliers ALTOS (precios por encima de ${limite_superior:,.0f}):")
print(f"  - Total: {len(outliers_altos)} ({len(outliers_altos)/len(df)*100:.2f}% del total)")
if len(outliers_altos) > 0:
    print(f"  - Rango: ${outliers_altos['precio_num'].min():,.0f} a ${outliers_altos['precio_num'].max():,.0f}")
    print(f"  - Precio promedio: ${outliers_altos['precio_num'].mean():,.0f}")
    print(f"  - Precio mediano: ${outliers_altos['precio_num'].median():,.0f}")
    print("  - Algunos ejemplos de outliers altos:")
    for i, row in outliers_altos.head(5).iterrows():
        print(f"    • ${row['precio_num']:,.0f} - {row.get('tipo_operacion', 'Desconocido')} en {row.get('ubicacion', 'Ubicación desconocida')}")

print(f"\n Outliers BAJOS (precios por debajo de ${limite_inferior:,.0f}):")
print(f"  - Total: {len(outliers_bajos)} ({len(outliers_bajos)/len(df)*100:.2f}% del total)")
if len(outliers_bajos) > 0:
    print(f"  - Rango: ${outliers_bajos['precio_num'].min():,.0f} a ${outliers_bajos['precio_num'].max():,.0f}")
    print(f"  - Precio promedio: ${outliers_bajos['precio_num'].mean():,.0f}")
    print(f"  - Precio mediano: ${outliers_bajos['precio_num'].median():,.0f}")
    print("  - Algunos ejemplos de outliers bajos:")
    for i, row in outliers_bajos.head(5).iterrows():
        print(f"    • ${row['precio_num']:,.0f} - {row.get('tipo_operacion', 'Desconocido')} en {row.get('ubicacion', 'Ubicación desconocida')}")

total_outliers = len(outliers_altos) + len(outliers_bajos)
print(f"\n Resumen total:")
print(f"  - Outliers ALTOS: {len(outliers_altos)} ({len(outliers_altos)/total_outliers*100 if total_outliers else 0:.1f}% de todos los outliers)")
print(f"  - Outliers BAJOS: {len(outliers_bajos)} ({len(outliers_bajos)/total_outliers*100 if total_outliers else 0:.1f}% de todos los outliers)")
print(f"  - Total outliers detectados: {total_outliers} ({total_outliers/len(df)*100:.2f}% del dataset)")

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

ax1 = axes[0]
ax1.hist(precios_validos['precio_num'], bins=50, color='#3498db', alpha=0.7, edgecolor='black')
ax1.axvline(limite_inferior, color='red', linestyle='--', linewidth=2, label=f'Límite inferior (${limite_inferior:,.0f})')
ax1.axvline(limite_superior, color='red', linestyle='--', linewidth=2, label=f'Límite superior (${limite_superior:,.0f})')
ax1.axvline(Q1, color='green', linestyle=':', linewidth=1.5, label=f'Q1 (${Q1:,.0f})')
ax1.axvline(Q3, color='green', linestyle=':', linewidth=1.5, label=f'Q3 (${Q3:,.0f})')
ax1.set_title('Distribución de Precios con Límites de Outliers')
ax1.set_xlabel('Precio')
ax1.set_ylabel('Frecuencia')
ax1.legend(fontsize=9)

ax2 = axes[1]
if total_outliers > 0:
    sizes = [len(outliers_altos), len(outliers_bajos)]
    labels = [f'Outliers ALTOS\n({len(outliers_altos)})', f'Outliers BAJOS\n({len(outliers_bajos)})']
    colors = ['#e74c3c', '#f39c12']
    ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Distribución de Outliers')

plt.tight_layout()
plt.savefig('analisis_outliers_detallado.png', dpi=150, bbox_inches='tight')
print("\n Gráfico guardado como 'analisis_outliers_detallado.png'\n")
plt.show()

