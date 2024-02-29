import tkinter as tk
from tkinter import ttk, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


class ScrapingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Scraping y Exportación")
        self.master.geometry("500x400")
        self.master.resizable(False, False)

        # Creamos un estilo para el fondo del LabelFrame
        self.style = ttk.Style()
        self.style.configure("Background.TFrame", background="#f0f0f0")

        # Variables de control
        self.check_farmacia_red = tk.BooleanVar()
        self.check_farmacia_lider = tk.BooleanVar()
        self.check_farmacia_general_paz = tk.BooleanVar()
        self.check_super_mami = tk.BooleanVar()
        self.num_pages_entry = None
        self.status_label = None

        # Encabezado
        self.header_label = ttk.Label(self.master, text="Scraping y Exportación", font=("Helvetica", 20))
        self.header_label.pack(pady=20)

        # Sección de opciones
        self.options_frame = ttk.LabelFrame(self.master,  style="Background.TFrame")
        self.options_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        ttk.Label(self.options_frame, text="Seleccione los sitios a escrapear:").grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self.check_farmacia_red_button = ttk.Checkbutton(self.options_frame, text="Farmacia Red", variable=self.check_farmacia_red)
        self.check_farmacia_red_button.grid(row=1, column=0, pady=5, sticky="w")

        self.check_farmacia_lider_button = ttk.Checkbutton(self.options_frame, text="Farmacia Líder", variable=self.check_farmacia_lider)
        self.check_farmacia_lider_button.grid(row=2, column=0, pady=5, sticky="w")

        self.check_farmacia_general_paz_button = ttk.Checkbutton(self.options_frame, text="Farmacia General Paz", variable=self.check_farmacia_general_paz)
        self.check_farmacia_general_paz_button.grid(row=3, column=0, pady=5, sticky="w")

        self.check_super_mami_button = ttk.Checkbutton(self.options_frame, text="Super Mami", variable=self.check_super_mami)
        self.check_super_mami_button.grid(row=4, column=0, pady=5, sticky="w")

        ttk.Label(self.options_frame, text="Número de páginas a escrapear:").grid(row=1, column=1, pady=10, padx=20, sticky="w")

        self.num_pages_entry = ttk.Entry(self.options_frame)
        self.num_pages_entry.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Botón de acción
        self.scrape_button = ttk.Button(self.master, text="INICIAR EXTRACCION DE DATOS", command=self.realizar_scraping_y_exportar)
        self.scrape_button.pack(pady=20)

        # Mensaje de estado
        self.status_label = ttk.Label(self.master, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

    def realizar_scraping_y_exportar(self):
        resultados = {}

        if self.check_farmacia_red.get():
            resultados['Farmacia Red'] = self.obtener_productos_farmacia_red(int(self.num_pages_entry.get()))
        if self.check_farmacia_lider.get():
            resultados['Farmacia Líder'] = self.obtener_productos_farmacia_lider(int(self.num_pages_entry.get()))
        if self.check_farmacia_general_paz.get():
            resultados['Farmacia General Paz'] = self.obtener_productos_farmacia_general_paz(int(self.num_pages_entry.get()))
        if self.check_super_mami.get():
            resultados['Super Mami'] = self.obtener_productos_super_mami(int(self.num_pages_entry.get()))

        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")])
        self.exportar_a_excel(resultados, nombre_archivo)
        self.status_label.config(text=f"Resultados exportados a {nombre_archivo}")

    def obtener_productos_farmacia_red(self, num_paginas=50):
        resultados_farmacia_red = []

        for pagina in range(1, num_paginas + 1):
            url_pagina = f"https://www.farmaciasred.com.ar/shop?page={pagina}"
            response_pagina = requests.get(url_pagina)

            if response_pagina.status_code == 200:
                soup_pagina = BeautifulSoup(response_pagina.text, 'html.parser')
                productos = soup_pagina.find_all('div', class_='product-list-item')

                for producto in productos:
                    nombre_producto = producto.find('span', class_='child-top').text.strip()

                    # Buscar el precio dentro del contenedor del producto
                    precio_span = producto.find('span', class_='amount')

                    if precio_span:
                        # Extraer el texto del precio y eliminar espacios en blanco
                        precio_texto = precio_span.text.strip()
                        # Utilizar expresiones regulares para extraer solo el valor numérico
                        precio_producto = re.search(r'\d+(\.\d+)?', precio_texto).group()
                        resultados_farmacia_red.append([nombre_producto, precio_producto])

        return resultados_farmacia_red

    def obtener_productos_farmacia_lider(self, num_paginas=15):
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

    def obtener_productos_farmacia_general_paz(self, num_paginas=50):
        resultados_farmacia_general_paz = []

        urls_farmacia_general_paz = [
            "https://www.farmaciasred.com.ar/shop/dermocosmetica-PC35459",
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

    def obtener_productos_super_mami(self, num_paginas=65):
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

    def exportar_a_excel(self, resultados, nombre_archivo):
        if resultados:
            with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
                for origen, data in resultados.items():
                    df = pd.DataFrame(data, columns=["Nombre del Producto", "Precio"])
                    df['Origen'] = origen  # Agregar una columna 'Origen' con el nombre del origen
                    df.to_excel(writer, sheet_name=origen, index=False)

                # Agregar una hoja adicional con todos los productos y su origen
                df_all = pd.concat([pd.DataFrame(data, columns=["Nombre del Producto", "Precio"]).assign(Origen=origen) for origen, data in resultados.items()], ignore_index=True)
                df_all.to_excel(writer, sheet_name='Todos los Productos', index=False)


def main():
    root = tk.Tk()
    app = ScrapingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
