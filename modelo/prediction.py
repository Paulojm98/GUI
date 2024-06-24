# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:37:46 2024

@author: paulo
"""
import numpy as np
import matplotlib.pyplot as plt
from utilidades.util_ticket import TicketPurpose, Ticket
import tensorflow as tf
from utilidades.util_data_generator_predict import HDF5PredictionGenerator

class ModeloPrediccion:
    def __init__(self):
        pass

    def predecir(self, modelo, dataset, indices, panel, queue_message):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado el proceso de predicción de datos."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        model = tf.keras.models.load_model(modelo)
        
        prediction_generator = HDF5PredictionGenerator(dataset, indices, batch_size=64)
        
        # Realizar predicciones
        predicciones = model.predict(prediction_generator)
        
        predicciones = np.array(predicciones).flatten()
        predicciones = (predicciones > 0.5).astype(int)

        # Conteo de predicciones para sin daño (0) y con daño (1)
        sin_daño = np.sum(predicciones == 0)
        con_daño = np.sum(predicciones == 1)
        
        # Crear la gráfica de barras
        self.fig, ax = plt.subplots(figsize=(8, 6))
        labels = ['Estructura intacta', 'Estructura dañada']
        counts = [sin_daño, con_daño]
        
        ax.bar(labels, counts, color=['blue', 'red'])
        
        # Añadir etiquetas y título
        ax.set_xlabel('Tipo de Predicción')
        ax.set_ylabel('Número de Predicciones')
        ax.set_title('Número de Predicciones Sin Daño vs Con Daño')

        
        ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                        ticket_value=["Se ha terminado el proceso de predicción."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        