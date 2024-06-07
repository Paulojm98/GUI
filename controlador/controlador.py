# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 23:19:40 2024

@author: paulo
"""

from controlador.controlador_bdatos import ControladorBDatos
from controlador.controlador_entrenamiento_carga_memoria import ControladorEntrenamientoCargaMemoria
from controlador.controlador_entrenamiento import ControladorEntrenamiento
from controlador.controlador_prediccion import ControladorPrediccion
import customtkinter as ctk

class Controlador:
    def __init__(self, modelo, view):
        self.view = view
        self.model = modelo
        self._bind()

    def _bind(self):
        self.view.root.buttonMenuLateral.configure(command=self.toggle_panel)
        self.view.root.button_bdatos.configure(command=self.accion_bdatos)
        self.view.root.button_dataset.configure(command=self.accion_entrenamiento_memoria)
        self.view.root.button_entrenamiento.configure(command=self.accion_entrenamiento)
        self.view.root.button_predecir.configure(command=self.accion_prediccion)
        
    

        
    def accion_bdatos(self):
        self.view.switch("bdatos")
        self.controlador_bdatos = ControladorBDatos(self.model, self.view)
        
    def accion_entrenamiento_memoria(self):
        self.view.switch("entrenamiento_memoria")
        self.controlador_dataset = ControladorEntrenamientoCargaMemoria(self.model, self.view)
    
    def accion_entrenamiento(self):
        self.view.switch("entrenamiento")
        self.controlador_entrenamiento = ControladorEntrenamiento(self.model, self.view)
        
    def accion_prediccion(self):
        self.view.switch("prediccion")
        self.controlador_prediccion = ControladorPrediccion(self.model, self.view)
        
    def toggle_panel(self):
        if self.view.root.menu_lateral.winfo_ismapped():
            self.view.root.menu_lateral.pack_forget()
        else:
            self.view.root.menu_lateral.pack(side=ctk.LEFT, fill='both')
        

    def start(self):
        self.view.start_mainloop()