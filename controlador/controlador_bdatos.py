# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:41:56 2024

@author: paulo
"""



from queue import Queue
import threading
from utilidades.util_ticket import TicketPurpose

class ControladorBDatos:
    def __init__(self, modelo, vista):
        self.modelo = modelo.modeloBDatos
        self.vista = vista
        self.panel = self.vista.current_frame
        self.panel_derecho = self.panel.panel_derecho
        self.queue_message = Queue()
        self._bind()

    def _bind(self):
        self.panel.checkbutton_filtro.configure(command=self.toggle_fields)
        self.panel.button_crear_indices.configure(command=lambda: threading.Thread(target=self.crear_indices).start())
        self.vista.root.bind("<<Check_queue>>", self.check_queue)
        

    def crear_indices(self):
        archivo_h5 = self.panel.entry_data_train.get()
        destino = self.panel.entry_destino_train.get()
        nombre_indexes_pristine = self.panel.entry_nombre_pristine.get()
        nombre_indexes_damage = self.panel.entry_nombre_damage.get()
        transmisor = None
        receptor = None
        ruido = True
        if self.panel.check_filtro.get() == 1:
            transmisor = float(self.panel.transmisor_entry.get())
            receptor = float(self.panel.receptor_entry.get())
            ruido = self.panel.checkbutton_ruido.get()
        self.modelo.crear_indices(archivo_h5, destino, nombre_indexes_pristine, nombre_indexes_damage, transmisor, receptor, ruido,
                                  self.panel, self.queue_message)
        
    def check_queue(self, event):
        msg = self.queue_message.get()
        
        if msg.ticket_type == TicketPurpose.INICIO_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
        if msg.ticket_type == TicketPurpose.ERROR:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
        if msg.ticket_type == TicketPurpose.FIN_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
    def toggle_fields(self):
        if self.panel.check_filtro.get() == 1:  # Si el Checkbutton está seleccionado
            self.panel.transmisor_entry.configure(state='normal')  # Activar
            self.panel.receptor_entry.configure(state='normal')  # Activar
            self.panel.checkbutton_ruido.configure(state='normal')  # Activar
        else:
            self.panel.transmisor_entry.configure(state='disabled')  # Desactivar
            self.panel.receptor_entry.configure(state='disabled')
            self.panel.checkbutton_ruido.configure(state='disabled')
            
    
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()