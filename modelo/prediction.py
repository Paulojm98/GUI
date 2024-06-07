# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:37:46 2024

@author: paulo
"""
import numpy as np
import matplotlib.pyplot as plt
from utilidades.util_ticket import TicketPurpose, Ticket
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle

class ModeloPrediccion:
    def __init__(self):
        pass

    def predecir(self, modelo, X, Y, panel, queue_message):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado el proceso de predicción de datos."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        with open(X, 'rb') as f:
            X = pickle.load(f)
        
        with open(Y, 'rb') as f:
            Y = pickle.load(f)
        
        X = np.array(X)
        Y = np.array(Y)
        
        model = load_model(modelo)

        predicciones = model.predict(X)
        predicciones = np.array(predicciones).flatten()
        predicciones = (predicciones > 0.5).astype(int)

        accuracy = accuracy_score(Y, predicciones)
        conf_matrix = confusion_matrix(Y, predicciones)
        
        self.fig, ax = plt.subplots(figsize=(8, 6))
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=['Pristine', 'Damage'])
        cm_display.plot(ax=ax)

        
        ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                        ticket_value=["Se ha terminado el proceso de predicción.",
                                      f"Precisión: {accuracy}"])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        