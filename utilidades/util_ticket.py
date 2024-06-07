# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 22:55:21 2024

@author: paulo
"""

from enum import Enum, auto
from typing import List

class TicketPurpose(Enum):
    INICIO_TAREA = auto()
    PROGRESO_TAREA = auto()
    FIN_TAREA =auto()
    ERROR = auto()
    
    
class Ticket:
    def __init__(self, 
                 ticket_type: TicketPurpose,
                 ticket_value: List[str]):
        
        self.ticket_type = ticket_type
        self.ticket_value = ticket_value