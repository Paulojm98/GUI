# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:20:46 2024

@author: paulo
"""

import customtkinter as ctk
from tkinter import ttk

class VistaEntrenamientoDesign(ctk.CTkFrame):
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

        # Nombre del modelo para el guardado
        ctk.CTkLabel(self.panel_izquierdo, text="Nombre modelo:").grid(row=1, column=1, pady=5)
        self.entry_nombre_modelo = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_nombre_modelo.grid(row=1, column=2, columnspan=2, sticky="ew", pady=5)

        # Carpeta destino guardado del modelo
        ctk.CTkLabel(self.panel_izquierdo, text="Carpeta destino modelo:").grid(row=2, column=1, pady=5)
        self.label_destino_modelo = ctk.CTkLabel(self.panel_izquierdo, text="")
        self.label_destino_modelo.grid(row=2, column=2, sticky="ew", pady=5)
        self.boton_destino_modelo = ctk.CTkButton(self.panel_izquierdo, text="Seleccionar", width=50)
        self.boton_destino_modelo.grid(row=2, column=3, pady=5)

        # Ruta a la carpeta H5
        ctk.CTkLabel(self.panel_izquierdo, text="Archivo dataset:").grid(row=3, column=1, pady=5)
        self.label_dataset = ctk.CTkLabel(self.panel_izquierdo, text="")
        self.label_dataset.grid(row=3, column=2, sticky="ew", pady=5)
        self.boton_dataset = ctk.CTkButton(self.panel_izquierdo, text="Seleccionar", width=50)
        self.boton_dataset.grid(row=3, column=3, pady=5)

        # Ruta a la carpeta pickle pristine
        ctk.CTkLabel(self.panel_izquierdo, text="Indices señales Pristine:").grid(row=4, column=1, pady=5)
        self.label_indices_pristine = ctk.CTkLabel(self.panel_izquierdo, text="")
        self.label_indices_pristine.grid(row=4, column=2, sticky="ew", pady=5)
        self.boton_pristine = ctk.CTkButton(self.panel_izquierdo, text="Seleccionar", width=50)
        self.boton_pristine.grid(row=4, column=3, pady=5)

        # Ruta a la carpeta
        ctk.CTkLabel(self.panel_izquierdo, text="Indices señales Damage:").grid(row=5, column=1, pady=5)
        self.label_indices_damage = ctk.CTkLabel(self.panel_izquierdo, text="")
        self.label_indices_damage.grid(row=5, column=2, sticky="ew", pady=5)
        self.boton_damage = ctk.CTkButton(self.panel_izquierdo, text="Seleccionar", width=50)
        self.boton_damage.grid(row=5, column=3, pady=5)

        
        ctk.CTkLabel(self.panel_izquierdo, text="Tipo de modelo:").grid(row=6, column=1, pady=5)
        self.tipo_creacion = ttk.Combobox(self.panel_izquierdo, values=["CNN1", "MLP"], state="readonly", width=45)
        self.tipo_creacion.grid(row=6, column=2, columnspan=2, pady=5)

        
        ctk.CTkLabel(self.panel_izquierdo, text="Épocas:").grid(row=8, column=1, pady=5)
        self.entry_epocas = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_epocas.grid(row=8, column=2, sticky="ew", pady=5)

        ctk.CTkLabel(self.panel_izquierdo, text="Tamaño lote:").grid(row=9, column=1, pady=5)
        self.entry_batch_size = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_batch_size.grid(row=9, column=2, sticky="ew", pady=5)

        ctk.CTkLabel(self.panel_izquierdo, text="Learning rate:").grid(row=10, column=1, pady=5)
        self.entry_learning_rate = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_learning_rate.grid(row=10, column=2, sticky="ew", pady=5)

        
        ctk.CTkLabel(self.panel_izquierdo, text="Porcentaje Validación:").grid(row=11, column=1, pady=5)
        self.entry_validation_split = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_validation_split.grid(row=11, column=2, sticky="ew", pady=5)

        # Variable para el estado del checkbox de ClassName
        self.check_filtro = ctk.IntVar()
        self.checkbutton_semilla = ctk.CTkCheckBox(self.panel_izquierdo, text="¿Quieres aplicar una semilla?", variable=self.check_filtro)
        self.checkbutton_semilla.grid(row=12, column=1, columnspan=3, pady=5)

        # Semilla de reproducibilidad
        ctk.CTkLabel(self.panel_izquierdo, text="Valor de semilla:").grid(row=13, column=1, pady=5)
        self.entry_semilla = ctk.CTkEntry(self.panel_izquierdo)
        self.entry_semilla.grid(row=13, column=2, sticky="ew", pady=5)
        self.entry_semilla.configure(state='disabled')

        # Botón para iniciar el entrenamiento
        self.button_entrenar = ctk.CTkButton(self.panel_izquierdo, text="Entrenar")
        self.button_entrenar.grid(row=14, column=2, pady=10)
        
        # Botón para detener el entrenamiento
        self.button_detener = ctk.CTkButton(self.panel_izquierdo, text="Detener")
        self.button_detener.grid(row=15, column=2, pady=10)
        
    def controles_panel_derecho(self):
        self.panel_derecho.grid_rowconfigure(2, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        self.label_panel_dch1 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
        # Segundo label justo debajo del primero en panel_derecho
        self.label_panel_dch2 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        
        self.textbox_logs_train = ctk.CTkTextbox(self.panel_derecho,wrap="word" )
        self.textbox_logs_train.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox_logs_train.configure(state="disabled")

    
    