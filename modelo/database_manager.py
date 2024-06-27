# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:34:01 2024

@author: paulo
"""
from utilidades.util_ticket import TicketPurpose, Ticket
import os
import h5py
import pickle

class ModeloBDatos:
    
    def __init__(self):
        pass
    

    def crear_indices(self, origen, destino, nombre_pristine, nombre_damage, transmisor, receptor, ruido, panel, queue_message):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado la creación de los indices."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        
        try:
            filters = {
                'Transmisor': transmisor,
                'Receptor': receptor,    
                'sigma': ruido     
            }

            hdf5_file = origen
            indexes_pristine = []
            indexes_damage = []        
            
            with h5py.File(hdf5_file, 'r') as f:
                for classname in f['test'].keys():
                    print(f"[INFO] ClassName: {classname}")
                    grp_class = f['test'][classname]
                    for index in grp_class.keys():
                        grp_index = grp_class[index]
                        for dataset_name in grp_index.keys():
                            
                            dset = grp_index[dataset_name]
                            
                            # Aplicar los filtros
                            if self.check_filters(dset, filters):
                                if classname == "Pristine":
                                    indexes_pristine.append((classname, index, dataset_name))
                                else:
                                    indexes_damage.append((classname, index, dataset_name))

            if not os.path.exists(destino):
                os.makedirs(destino)

            if not nombre_pristine.endswith('.pkl'):
                nombre_pristine += '.pkl'
            if not nombre_damage.endswith('.pkl'):
                nombre_damage += '.pkl'
            
            pristine_file = os.path.join(destino, nombre_pristine)
            damage_file = os.path.join(destino, nombre_damage)
            
            with open(pristine_file, 'wb') as f:
                pickle.dump(indexes_pristine, f)

            with open(damage_file, 'wb') as f:
                pickle.dump(indexes_damage, f)
            
            ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                            ticket_value=["Se ha finalizado la creación de los indices."])
            queue_message.put(ticket)
            panel.event_generate("<<Check_queue>>")
            
        except:
            ticket = Ticket(ticket_type=TicketPurpose.ERROR,
                            ticket_value=["Ha ocurrido un error al crear los indices."])
            queue_message.put(ticket)
            panel.event_generate("<<Check_queue>>")
            
    def check_filters(self, dset, filters):
        for attr, condition in filters.items():
            if attr == 'sigma':
                if condition is True:
                    continue  # Incluir tanto con 'sigma' como sin 'sigma'
                elif condition is False and 'sigma' in dset.attrs:
                    return False
            else:
                if condition is not None:
                    if attr in dset.attrs:
                        value = dset.attrs[attr]
                        if value != condition:
                            return False
                    else:
                        return False  # Si falta algún atributo requerido y el filtro no es None
        return True
            
        