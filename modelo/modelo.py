# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:55:47 2024

@author: paulo
"""

from .train_model_carga_memoria import ModeloEntrenamientoCargaMenmoria
from .database_manager import ModeloBDatos
from .train_model import ModeloEntrenamiento
from .prediction import ModeloPrediccion


class Modelo:
    def __init__(self):
        self.modeloBDatos = ModeloBDatos()
        self.ModeloEntrenamientoCargaMemoria = ModeloEntrenamientoCargaMenmoria()
        self.ModeloEntrenamiento = ModeloEntrenamiento()
        self.modeloPrediccion = ModeloPrediccion()