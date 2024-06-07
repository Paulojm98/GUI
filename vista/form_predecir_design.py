# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:28:30 2024

@author: paulo
"""

import customtkinter as ctk
from tkinter import ttk

class VistaPrediccionDesign(ctk.CTkFrame):
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
        
        self.panel_izquierdo.grid_columnconfigure(2, weight=1)
        
        # Carpeta origen
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación Modelo:").grid(row=1, column=1, pady=5)
        self.entrada_modelo = ctk.CTkEntry(self.panel_izquierdo,)
        self.entrada_modelo.grid(row=1, column=2, sticky="ew", pady=5)
        
        # Carpeta destino
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación datos test:").grid(row=2, column=1, pady=5)
        self.entrada_datos_test = ctk.CTkEntry(self.panel_izquierdo)
        self.entrada_datos_test.grid(row=2, column=2, sticky="ew", pady=5)
        
        ctk.CTkLabel(self.panel_izquierdo, text="Ubicación etiquetas:").grid(row=3, column=1, pady=5)
        self.entrada_etiquetas_test = ctk.CTkEntry(self.panel_izquierdo)
        self.entrada_etiquetas_test.grid(row=3, column=2, sticky="ew", pady=5)
        
        
        #Botón para iniciar la creación del dataset
        self.button_predecir = ctk.CTkButton(self.panel_izquierdo, text="Predecir")
        self.button_predecir.grid(row=14, column=2, pady=10)
        
    def controles_panel_derecho(self):
        self.panel_derecho.grid_rowconfigure(2, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        self.label_panel_dch1 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
        # Segundo label justo debajo del primero en panel_derecho
        self.label_panel_dch2 = ctk.CTkLabel(self.panel_derecho, text="")
        self.label_panel_dch2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        
        
    def toggle_fields(self):
        # ClassName
        if self.check_filtro.get() == 1:  # Si el Checkbutton está seleccionado
            self.entry_semilla.configure(state='normal')  # Activar
        else:
            self.entry_semilla.configure(state='disabled')  # Desactivar
        
            
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()