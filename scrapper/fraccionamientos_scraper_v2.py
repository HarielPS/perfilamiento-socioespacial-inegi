from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# URLs disponibles
urls = {
    "1": ("Guadalajara", "https://www.rho.mx/ccdb/cp/NULL/2/14/2"),
    "2": ("Monterrey", "https://www.rho.mx/ccdb/cp/NULL/2/19/2"),
    "3": ("Puebla", "https://www.rho.mx/ccdb/cp/NULL/2/21/2")
}

# Límites por ciudad
paginas_limite = {
    "Guadalajara": 10,
    "Monterrey": 20,
    "Puebla": 20
}

# Menú
print("Selecciona la ciudad para extraer los fraccionamientos:")
for k, v in urls.items():
    print(f"{k}. {v[0]}")
opcion = input("Escribe el número de tu elección: ").strip()

if opcion not in urls:
    print(" Opción no válida. Intenta de nuevo.")
    exit()

ciudad, base_url = urls[opcion]
limite = paginas_limite[ciudad]
print(f" Extrayendo fraccionamientos del municipio '{ciudad}'...\n")

# Configurar el driver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

datos = []

# Recorrer páginas de forma directa (evitando clicks)
for pagina in range(1, limite + 1):
    if pagina == 1:
        url = base_url
    else:
        url = f"{base_url}/{pagina}"
    
    print(f" Página {pagina} → {url}")
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.con tbody tr"))
        )
    except:
        print(" No se pudo cargar la tabla. Saliendo...")
        break

    filas = driver.find_elements(By.CSS_SELECTOR, "table.con tbody tr")
    for fila in filas:
        columnas = fila.find_elements(By.TAG_NAME, 'td')
        if len(columnas) == 6:
            cp = columnas[1].text
            entidad = columnas[2].text
            municipio = columnas[3].text.strip()
            asentamiento = columnas[4].text.strip()
            ambito = columnas[5].text

            if asentamiento.lower().startswith('fracc.') and ciudad.lower() in municipio.lower():
                datos.append({
                    'CP': cp,
                    'Entidad': entidad,
                    'Municipio': municipio,
                    'Asentamiento': asentamiento,
                    'Ámbito': ambito
                })

    time.sleep(1)

driver.quit()

# Guardar resultados
df = pd.DataFrame(datos)
archivo_excel = f"fraccionamientos_{ciudad.lower()}.xlsx"
archivo_csv = f"fraccionamientos_{ciudad.lower()}.csv"

df.to_excel(archivo_excel, index=False)
df.to_csv(archivo_csv, index=False)

print(f"\n ¡Listo! Se guardaron {len(df)} fraccionamientos en:")
print(f"   - Excel: {archivo_excel}")
print(f"   - CSV:   {archivo_csv}")
