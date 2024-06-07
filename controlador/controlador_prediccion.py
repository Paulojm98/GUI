# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:44:04 2024

@author: paulo
"""
from queue import Queue
import threading
from utilidades.util_ticket import TicketPurpose, Ticket
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ControladorPrediccion:
    def __init__(self, modelo, vista):
        self.modelo = modelo.modeloPrediccion
        self.vista= vista
        self.panel = self.vista.current_frame
        self.panel_derecho = self.panel.panel_derecho
        self.queue_message = Queue()
        self._bind()
        
    def _bind(self):
        self.panel.button_predecir.configure(command=lambda: threading.Thread(target=self.realizar_prediccion).start())
        self.vista.root.bind("<<Check_queue>>", self.check_queue)

    def realizar_prediccion(self):
        try:
            modelo = self.panel.entrada_modelo.get()
            X = self.panel.entrada_datos_test.get()
            Y = self.panel.entrada_etiquetas_test.get()
            
            self.modelo.predecir(modelo, X, Y, self.panel, self.queue_message)
            
            
        except FileNotFoundError:
            ticket = Ticket(ticket_type=TicketPurpose.ERROR,
                            ticket_value=["Ha ocurrido un error con los campos origen o destino"])
            self.queue_message.put(ticket)
            self.panel.event_generate("<<Check_queue>>")
        
    def check_queue(self, event):
        msg = self.queue_message.get()
        
        if msg.ticket_type == TicketPurpose.INICIO_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
        if msg.ticket_type == TicketPurpose.ERROR:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            
            
        if msg.ticket_type == TicketPurpose.FIN_TAREA:
            self.panel.label_panel_dch1.configure(text=msg.ticket_value[0])
            self.panel.label_panel_dch2.configure(text=msg.ticket_value[1])
            canvas = FigureCanvasTkAgg(self.modelo.fig, self.panel_derecho)  # `self.panel` es el panel de CustomTkinter donde quieres mostrar el gráfico
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
            
    def toggle_fields(self):
        # ClassName
        if self.panel.check_filtro.get() == 1:  # Si el Checkbutton está seleccionado
            self.panel.entry_semilla.configure(state='normal')  # Activar
        else:
            self.panel.entry_semilla.configure(state='disabled')  # Desactivar
            
    
        
            
    def limpiar_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
        