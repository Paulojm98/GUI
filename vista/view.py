# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 23:05:27 2024

@author: paulo
"""

from .form_maestro_design import VistaMaestroDesign
from .form_bdatos_design import VistaBDatosDesign
from .form_entrenamiento_carga_memoria_design import VistaEntrenamientoCargaMemoriaDesign
from .form_entrenamiento_red import VistaEntrenamientoDesign
from .form_predecir_design import VistaPrediccionDesign
import customtkinter as ctk

class View:
    def __init__(self):
        self.root = VistaMaestroDesign()
        self.frame_classes = {
            "bdatos": VistaBDatosDesign,
            "entrenamiento_memoria": VistaEntrenamientoCargaMemoriaDesign,
            "entrenamiento": VistaEntrenamientoDesign,
            "prediccion": VistaPrediccionDesign
        }
        self.cuerpo_principal = self.root.cuerpo_principal

    def switch(self, name):
        self.limpiar_panel(self.cuerpo_principal)
        new_frame = self.frame_classes[name](self.cuerpo_principal)
        self.current_frame = new_frame
        self.current_frame.pack(side=ctk.RIGHT, fill='both', expand=True)
        
    
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def start_mainloop(self):
        self.root.mainloop()