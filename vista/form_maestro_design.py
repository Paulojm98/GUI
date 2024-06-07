# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 20:31:31 2024

@author: paulo
"""

import customtkinter as ctk

import utilidades.util_ventana as util_ventana


class VistaMaestroDesign(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme("blue")
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()
    
    def config_window(self):
        self.title("Interfaz gráfica")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)
        
    def paneles(self):
        # Creamos tres paneles base
        #Barra superior
        self.barra_superior = ctk.CTkFrame(self, height=50)
        self.barra_superior.pack(side=ctk.TOP, fill='both')
        
        #Menú lateral
        self.menu_lateral = ctk.CTkFrame(self, corner_radius=0, width=15)
        self.menu_lateral.pack(side=ctk.LEFT, fill='both')
        
        #Cuerpo principal
        self.cuerpo_principal = ctk.CTkFrame(self)
        self.cuerpo_principal.pack(side=ctk.RIGHT, fill='both', expand=True)
      
    def controles_barra_superior(self):
        #Etiqueta título
        self.labelTitulo = ctk.CTkLabel(self.barra_superior, text="Using machine learning to detect damage")
        self.labelTitulo.configure(font=("Roboto", 15), pady=10, padx=10, width=25)
        self.labelTitulo.pack(side=ctk.LEFT)
        
        self.buttonMenuLateral = ctk.CTkButton(self.barra_superior, text='Menu', width=5)
        self.buttonMenuLateral.pack(side=ctk.LEFT)
        
        self.labelTitulo = ctk.CTkLabel(self.barra_superior, text="paulo.juarez.moreno@alumnos.upm.es")
        self.labelTitulo.configure(font=("Roboto", 10), pady=10, padx=10, width=35)
        self.labelTitulo.pack(side=ctk.RIGHT)

        
    def controles_menu_lateral(self):
        self.menu_lateral.grid_columnconfigure(0, weight=1)  # Ajustado para que los elementos se expandan para llenar el espacio disponible
    
        # Label and dropdown menu inside the scrollable frame
        self.label_1 = ctk.CTkLabel(master=self.menu_lateral, text="Acciones")
        self.label_1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
        
        # Botones
        self.button_bdatos = ctk.CTkButton(self.menu_lateral, text="Crear Base de Datos", anchor="center", text_color="white")
        self.button_bdatos.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.button_dataset = ctk.CTkButton(self.menu_lateral, text="Entrenamiento Memoria", anchor="center", text_color="white")
        self.button_dataset.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.button_entrenamiento = ctk.CTkButton(self.menu_lateral, text="Entrenamiento Modelo", anchor="center", text_color="white")
        self.button_entrenamiento.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        self.button_predecir = ctk.CTkButton(self.menu_lateral, text="Predicción Modelo", anchor="center", text_color="white")
        self.button_predecir.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        
            
    def controles_cuerpo(self):
        label_bienvenida = ctk.CTkLabel(self.cuerpo_principal, text="Bienvenido, elige una opción",
                                text_color="black",  # Color del texto
                                font=("Roboto", 22, "bold"))  # Tamaño y estilo de fuente

        # Empaqueta el label en el centro del panel del cuerpo principal
        label_bienvenida.pack(expand=True)
        
    
        
        
    
            
            

            
    