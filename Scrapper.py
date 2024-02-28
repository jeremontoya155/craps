import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog
from openpyxl import Workbook
from openpyxl import load_workbook  

# Función para obtener productos y precios de Farmacia Red
# def obtener_productos_farmacia_red(num_paginas=50):
#     resultados_farmacia_red = []

#     urls_farmacia_red = [
#         "https://farmaciasred.com.ar/collections/dermocosmetica",
#         "https://farmaciasred.com.ar/collections/maquillaje",
#         "https://farmaciasred.com.ar/collections/perfumes-y-fragancias",
#         "https://farmaciasred.com.ar/collections/cuidado-personal"
#     ]

#     for url_categoria in urls_farmacia_red:
#         for pagina in range(1, num_paginas + 1):
#             url_pagina = f"{url_categoria}?page={pagina}"
#             response_pagina = requests.get(url_pagina)

#             if response_pagina.status_code == 200:
#                 soup_pagina = BeautifulSoup(response_pagina.text, 'html.parser')
#                 productos = soup_pagina.find_all('h2', class_='productitem--title')
                
#                 # Modificación: Buscar los precios dentro de cada producto
#                 for producto in productos:
#                     nombre_producto = producto.find('a').text.strip()

#                     # Buscar el contenedor que incluye tanto el título como el precio
#                     contenedor_producto = producto.find_parent('div', class_='productitem--content')

#                     # Verificar si se encontró el contenedor del producto
#                     if contenedor_producto:
#                         # Buscar el precio dentro del contenedor del producto
#                         precio_span = contenedor_producto.find('span', class_='money')

#                         if precio_span:
#                             precio_producto = re.sub('[^\d,]', '', precio_span.text)  # Eliminar caracteres no numéricos excepto ',' (coma)
#                             precio_producto = precio_producto.replace(',', '.')  # Reemplazar ',' (coma) con '.' (punto) para formateo numérico
                            
#                             # Verificar si la cadena no está vacía antes de convertirla a número flotante
#                             if precio_producto:
#                                 precio_producto = float(precio_producto)
#                                 resultados_farmacia_red.append([nombre_producto, precio_producto])

#     return resultados_farmacia_red
   

# Función para obtener productos y precios de Farmacia Líder
def obtener_productos_farmacia_lider(num_paginas=15):
    resultados_farmacia_lider = []

    urls_farmacia_lider = [
        "https://farmaciaslider.com.ar/10-dermocosmetica",
        "https://farmaciaslider.com.ar/12-cuidado-e-higiene-personal",
        "https://farmaciaslider.com.ar/21-perfumes-y-fragancias",
        "https://farmaciaslider.com.ar/14-maquillaje",
        "https://farmaciaslider.com.ar/70-nutricion"
    ]

    for url_categoria in urls_farmacia_lider:
        for pagina in range(1, num_paginas + 1):
            url_pagina = f"{url_categoria}?page={pagina}"
            response_pagina = requests.get(url_pagina)

            if response_pagina.status_code == 200:
                soup_pagina = BeautifulSoup(response_pagina.text, 'html.parser')
                productos = soup_pagina.find_all('h3', class_='h3 product-title')
                precios = soup_pagina.find_all('span', class_='product-price')

                for producto, precio in zip(productos, precios):
                    nombre_producto = producto.text.strip()
                    precio_producto = precio.text.strip()
                    resultados_farmacia_lider.append([nombre_producto, precio_producto])

    return resultados_farmacia_lider

# Función para obtener productos de Farmacia General Paz
def obtener_productos_farmacia_general_paz(num_paginas=50):
    resultados_farmacia_general_paz = []

    urls_farmacia_general_paz = [
        "https://www.farmaciageneralpaz.com/shop/dermocosmetica-PC1155",
        "https://www.farmaciageneralpaz.com/shop/perfumes-PC1156",
        "https://www.farmaciageneralpaz.com/shop/maquillajes",
        "https://www.farmaciageneralpaz.com/shop/cuidado-personal-PC8877"
    ]

    for url_categoria in urls_farmacia_general_paz:
        for pagina in range(1, num_paginas + 1):
            url_pagina = f"{url_categoria}?pagina={pagina}"
            response_pagina = requests.get(url_pagina)

            if response_pagina.status_code == 200:
                soup_pagina = BeautifulSoup(response_pagina.text, 'html.parser')
                nombres_productos_pagina = soup_pagina.find_all('h3', class_='kw-details-title')
                precios_pagina = soup_pagina.find_all('span', class_='amount')

                for nombre, precio in zip(nombres_productos_pagina, precios_pagina):
                    nombre_producto = nombre.find('span', class_='child-top').get_text().strip()
                    precio_producto = precio.get_text().strip()
                    resultados_farmacia_general_paz.append([nombre_producto, precio_producto])

    return resultados_farmacia_general_paz

# Función para obtener productos de Super Mami
def obtener_productos_super_mami(num_paginas=65):
    resultados_super_mami = []

    for pagina in range(1, num_paginas + 1):
        url_pagina = f"https://www.dinoonline.com.ar/super/categoria/supermami-perfumeria/_/N-146amvi?No={pagina * 36}&Nrpp=36"
        response_pagina = requests.get(url_pagina)

        if response_pagina.status_code == 200:
            soup_pagina = BeautifulSoup(response_pagina.text, 'html.parser')
            nombres_productos_pagina = soup_pagina.find_all('div', class_='description limitRow tooltipHere')
            precios_pagina = soup_pagina.find_all('div', class_='precio-unidad')

            for nombre, precio in zip(nombres_productos_pagina, precios_pagina):
                nombre_producto = nombre.get_text().strip()
                precio_producto = precio.find('span').get_text().strip()
                resultados_super_mami.append([nombre_producto, precio_producto])

    return resultados_super_mami

# Función para exportar resultados a un archivo Excel
def exportar_a_excel(resultados, nombre_archivo):
    if resultados:
        with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
            for origen, data in resultados.items():
                df = pd.DataFrame(data, columns=["Nombre del Producto", "Precio"])
                df['Origen'] = origen  # Agregar una columna 'Origen' con el nombre del origen
                df.to_excel(writer, sheet_name=origen, index=False)
            
            # Agregar una hoja adicional con todos los productos y su origen
            df_all = pd.concat([pd.DataFrame(data, columns=["Nombre del Producto", "Precio"]).assign(Origen=origen) for origen, data in resultados.items()], ignore_index=True)
            df_all.to_excel(writer, sheet_name='Todos los Productos', index=False)

# Función para realizar scraping y exportación
def realizar_scraping_y_exportar():
    resultados = {}

#    if check_farmacia_red.get():
#        resultados['Farmacia Red'] = obtener_productos_farmacia_red(int(entry_farmacia_red.get()))
    if check_farmacia_lider.get():
        resultados['Farmacia Líder'] = obtener_productos_farmacia_lider(int(entry_farmacia_lider.get()))
    if check_farmacia_general_paz.get():
        resultados['Farmacia General Paz'] = obtener_productos_farmacia_general_paz(int(entry_farmacia_general_paz.get()))
    if check_super_mami.get():
        resultados['Super Mami'] = obtener_productos_super_mami(int(entry_super_mami.get()))

    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")])
    exportar_a_excel(resultados, nombre_archivo)
    mensaje.config(text=f"Resultados exportados a {nombre_archivo}")

# Crear la ventana principal de tkinter
root = tk.Tk()
root.title("Scraping y Exportación")

# Variables para controlar la selección de sitios
#check_farmacia_red = tk.BooleanVar()
check_farmacia_lider = tk.BooleanVar()
check_farmacia_general_paz = tk.BooleanVar()
check_super_mami = tk.BooleanVar()

# Crear y configurar elementos de la interfaz
label_paginas = tk.Label(root, text="Número de Páginas:")
#label_farmacia_red = tk.Label(root, text="Farmacia Red")
label_farmacia_lider = tk.Label(root, text="Farmacia Líder")
label_farmacia_general_paz = tk.Label(root, text="Farmacia General Paz")
label_super_mami = tk.Label(root, text="Super Mami")
#entry_farmacia_red = tk.Entry(root)
entry_farmacia_lider = tk.Entry(root)
entry_farmacia_general_paz = tk.Entry(root)
entry_super_mami = tk.Entry(root)
boton_realizar_scraping = tk.Button(root, text="Realizar Scraping y Exportar", command=realizar_scraping_y_exportar)
mensaje = tk.Label(root, text="Resultados")

#check_red = tk.Checkbutton(root, variable=check_farmacia_red)
check_lider = tk.Checkbutton(root, variable=check_farmacia_lider)
check_paz = tk.Checkbutton(root, variable=check_farmacia_general_paz)
check_mami = tk.Checkbutton(root, variable=check_super_mami)

# Colocar elementos en la ventana
label_paginas.grid(row=0, column=0)
#label_farmacia_red.grid(row=1, column=1)
label_farmacia_lider.grid(row=2, column=1)
label_farmacia_general_paz.grid(row=3, column=1)
label_super_mami.grid(row=4, column=1)
#entry_farmacia_red.grid(row=1, column=2)
entry_farmacia_lider.grid(row=2, column=2)
entry_farmacia_general_paz.grid(row=3, column=2)
entry_super_mami.grid(row=4, column=2)
boton_realizar_scraping.grid(row=6, column=1, columnspan=2)
mensaje.grid(row=7, column=1, columnspan=2)
#check_red.grid(row=1, column=0)
check_lider.grid(row=2, column=0)
check_paz.grid(row=3, column=0)
check_mami.grid(row=4, column=0)

# Iniciar la interfaz de usuario
root.mainloop()
