# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 20:56:56 2024

@author: paulo
"""
import tensorflow as tf
from utilidades.util_ticket import TicketPurpose, Ticket

class CustomCallback(tf.keras.callbacks.Callback):
    def __init__(self, panel, queue_message):
        super(CustomCallback, self).__init__()
        self.panel = panel
        self.queue_message = queue_message

    def on_epoch_end(self, epoch, logs=None):
        mensaje = f"Época: {epoch + 1}"
        if 'loss' in logs:
            mensaje += f", Pérdida: {logs['loss']:.4f}"
        if 'accuracy' in logs:
            mensaje += f", Precisión: {logs['accuracy']:.4f}"
        if 'val_loss' in logs:
            mensaje += f", Val Pérdida: {logs['val_loss']:.4f}"
        if 'val_accuracy' in logs:
            mensaje += f", Val Precisión: {logs['val_accuracy']:.4f}"
            
        ticket = Ticket(ticket_type=TicketPurpose.PROGRESO_TAREA,
                        ticket_value=[mensaje])
        self.queue_message.put(ticket)
        self.panel.event_generate("<<Check_queue>>")
        
        

