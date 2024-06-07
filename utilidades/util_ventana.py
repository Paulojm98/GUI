# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:28:35 2024

@author: paulo
"""

def centrar_ventana(ventana, app_ancho, app_largo):
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    x = int((pantall_ancho/2) - (app_ancho/2))
    y = int((pantall_largo/2)-(app_largo/2))
    
    return ventana.geometry(f"{app_ancho}x{app_largo}+{x}+{y}")