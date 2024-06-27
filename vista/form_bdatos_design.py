# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:51:18 2024

@author: paulo
"""

import customtkinter as ctk
from tkinter import ttk

class VistaBDatosDesign(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paneles()
        self.controles_panel_izquierdo()
        self.controles_panel_derecho()
        
    def paneles(self):
        # Crear dos paneles (frames) dentro del panel principal
        self.panel_izquierdo = ctk.CTkFrame(self, width=250)
        self.panel_derecho = ctk.CTkFrame(self)
        
        self.panel_izquierdo.pack(side=ctk.LEFT, fill='y')
        self.panel_derecho.pack(side=ctk.RIGHT, fill='both', expand=True)
        
        
    def controles_panel_izquierdo(self):
        
        self.panel_izquierdo.grid_columnconfigure(1, weight=1)
        self.panel_izquierdo.grid_columnconfigure(2, weight=3)
        self.panel_izquierdo.grid_columnconfigure(3, weight=1)
        
        self.panel_izquierdo.grid_columnconfigure(2, weight=1)
        # Ubicación datos de entrenamiento
        ctk.CTkLabel(self.panel_izquierdo, text="Archivo Dataset:").grid(row=1, column=1, pady=5)
        self.entry_data_train = ctk.CTkEntry(self.panel_izquierdo,)
        self.entry_data_train.grid(row=1, column=2, sticky="ew", pady=5)
        self.boton_ruta_dataset = ctk.CTkButton(self.panel_izquierdo, text="Seleccionar", width=50)
        self.boton_ruta_dataset.grid(row=1, column=3, pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación indices:").grid(row=2, column=1, pady=5)
        self.entry_destino_train = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_destino_train.grid(row=2, column=2, sticky="ew", pady=5)
        self.boton_ruta_indices = ctk.CTkButton(self.panel_izquierdo, text="Seleccionar", width=50)
        self.boton_ruta_indices.grid(row=2, column=3, pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Nombre archivo índices Pristine:").grid(row=3, column=1, pady=5)
        self.entry_nombre_pristine = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_nombre_pristine.grid(row=3, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Nombre archivo índices Damage:").grid(row=4, column=1, pady=5)
        self.entry_nombre_damage = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_nombre_damage.grid(row=4, column=2, sticky="ew", pady=5)
        
        # Variable para el estado del checkbox de ClassName
        self.check_filtro = ctk.IntVar()
        self.checkbutton_filtro = ctk.CTkCheckBox(self.panel_izquierdo, text="¿Quieres aplicar filtros?", variable=self.check_filtro)
        self.checkbutton_filtro.grid(row=5, column=1, columnspan=3, pady=5)
        
        # Filtro por rango de Frecuencia
        ctk.CTkLabel(self.panel_izquierdo, text="Transmisor:").grid(row=6, column=1, pady=5)
        self.transmisor_entry = ctk.CTkEntry(self.panel_izquierdo)
        self.transmisor_entry.grid(row=6, column=2, sticky="ew", pady=5)
        self.transmisor_entry.configure(state='disabled')
    
        ctk.CTkLabel(self.panel_izquierdo, text="Receptor:").grid(row=7, column=1, pady=5)
        self.receptor_entry = ctk.CTkEntry(self.panel_izquierdo)
        self.receptor_entry.grid(row=7, column=2, sticky="ew", pady=5)
        self.receptor_entry.configure(state='disabled')
    
        # Variable para el estado del checkbox de ClassName
        self.check_ruido = ctk.IntVar()
        self.checkbutton_ruido = ctk.CTkCheckBox(self.panel_izquierdo, text="¿Quieres los datos con ruido gausiano?", variable=self.check_ruido)
        self.checkbutton_ruido.grid(row=8, column=1, columnspan=3, pady=5)
        self.checkbutton_ruido.configure(state='disabled')
        
        #Botón para iniciar la creación del dataset
        self.button_crear_indices = ctk.CTkButton(self.panel_izquierdo, text="Crear archivos índices")
        self.button_crear_indices.grid(row=9, column=2, pady=10)
        
        
        
    def controles_panel_derecho(self):
        # Configuración de grid en panel_derecho para que el Treeview se expanda
        
        self.label_panel_dch1 = ctk.CTkLabel(self.panel_derecho, text="", anchor="center")
        self.label_panel_dch1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
        # Segundo label justo debajo del primero en panel_derecho
        self.label_panel_dch2 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
        # Treeview que ocupa el espacio restante en panel_derecho
        self.tree = ttk.Treeview(self.panel_derecho)
        #self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.scrollbar = ttk.Scrollbar(self.panel_derecho, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.panel_derecho.grid_rowconfigure(2, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        

        
            