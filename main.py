# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 20:42:23 2024

@author: paulo
"""

from modelo.modelo import Modelo
from vista.view import View
from controlador.controlador import Controlador

def main():
    modelo = Modelo()
    vista = View()
    controlador = Controlador(modelo, vista)
    controlador.start()

if __name__ == "__main__":
    main()
 