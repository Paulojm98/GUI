# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:37:46 2024

@author: paulo
"""
import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from utilidades.util_ticket import TicketPurpose, Ticket
import tensorflow as tf
from utilidades.util_data_generator_predict import HDF5PredictionGenerator
import pickle

class ModeloPrediccion:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        relative_path_to_image = os.path.join(self.current_dir, '../imagenes/ui/plantilla_composite_v2.png')
        self.image_structure_path = os.path.normpath(relative_path_to_image)


    def predecir(self, modelo, dataset, indices, tarea_localizacion, no_use_dataloader, panel, queue_message):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado el proceso de predicción de datos."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        self.tarea_localizacion = tarea_localizacion
        self.dataset = dataset
        
        model = tf.keras.models.load_model(modelo)
        
        indexes = []
        with open(indices, 'rb') as f:
            indexes = pickle.load(f)
        
        if no_use_dataloader:
            print("Se van a cargar todos los datos de prueba en memoria")
            X_test = self.carga_datos(indexes)
            self.predicciones = model.predict(X_test)
            
        else:
            prediction_generator = HDF5PredictionGenerator(dataset, indexes)
            self.predicciones = model.predict(prediction_generator)
  
        
        ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                        ticket_value=["Se ha terminado el proceso de predicción."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
    
    def pintar_grafica(self):
        if self.tarea_localizacion:
            promedio_x = np.mean(self.predicciones[:, 0])
            promedio_y = np.mean(self.predicciones[:, 1])
            img = mpimg.imread(self.image_structure_path)  # Reemplaza 'fondo.png' con tu imagen

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.imshow(img, extent=[-40, 259.9, -40, 259.9])  # Ajusta los límites según tu imagen

            ax.scatter(promedio_x, promedio_y, marker='x', c='red', s=500)

            ax.set_xlabel('Coordenada X')
            ax.set_ylabel('Coordenada Y')
            ax.set_title('Predicción localización del daño')

            
        else:
            predicciones = np.array(self.predicciones).flatten()
            predicciones = (predicciones > 0.5).astype(int)
    
            # Conteo de predicciones para sin daño (0) y con daño (1)
            sin_daño = np.sum(predicciones == 0)
            con_daño = np.sum(predicciones == 1)
            
            # Crear la gráfica de barras
            fig, ax = plt.subplots(figsize=(8, 6))
            labels = ['Estructura intacta', 'Estructura dañada']
            counts = [sin_daño, con_daño]
            
            ax.bar(labels, counts, color=['blue', 'red'])
            
            # Añadir etiquetas y título
            ax.set_xlabel('Tipo de Predicción')
            ax.set_ylabel('Número de Predicciones')
            ax.set_title('Número de Predicciones Sin Daño vs Con Daño')
            
        return fig
    
    def normalize_signal(self, signal):
        normalized_signal = 2 * ((signal - np.min(signal)) / (np.max(signal) - np.min(signal))) - 1
        return normalized_signal
        
    def carga_datos(self, indexes):
        X = []
        with h5py.File(self.dataset, 'r') as f:
            for classname, index, dataset_name in indexes:
                dset = f[f'test/{classname}/{index}/{dataset_name}']
                signal = dset[:]
                signal = self.normalize_signal(signal)
                X.append(signal)

        return np.array(X)
        
        