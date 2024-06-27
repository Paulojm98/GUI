# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 19:54:34 2024

@author: paulo
"""
from tensorflow.keras.utils import Sequence
import numpy as np
import h5py

class HDF5DataGenerator(Sequence):
    def __init__(self, hdf5_file, indexes, tarea_localizacion, batch_size=32, shuffle=True):
        self.hdf5_file = hdf5_file
        self.indexes = indexes
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.tarea_localizacion = tarea_localizacion

    def __len__(self):
        # Devuelve el número de lotes por época
        return int(np.ceil(len(self.indexes) / self.batch_size))

    def __getitem__(self, index):
        # Generar un lote de datos
        batch_indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        X, y = self.__data_generation(batch_indexes)
        return X, y
    
    def on_epoch_end(self):
        # Mezclar los índices después de cada época
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, batch_indexes):
        X = []
        y = []
        with h5py.File(self.hdf5_file, 'r') as f:
            for classname, index, dataset_name in batch_indexes:
                dset = f[f'train/{classname}/{index}/{dataset_name}']
                signal = dset[:]
                signal = self.normalize_signal(signal)
                if self.tarea_localizacion:
                    etiqueta_x = dset.attrs['label_x']
                    etiqueta_y = dset.attrs['label_y']
                    y.append([etiqueta_x, etiqueta_y])
                else:   
                    label = dset.attrs['Label']
                    y.append(label)
                    
                X.append(signal)
                
        return np.array(X), np.array(y)
    

        

    
    def normalize_signal(self, signal):
        normalized_signal = 2 * ((signal - np.min(signal)) / (np.max(signal) - np.min(signal))) - 1
        return normalized_signal
    
