# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:59:53 2024

@author: PMJUAREZM
"""

from tensorflow.keras.utils import Sequence
import numpy as np
import h5py

class HDF5PredictionGenerator(Sequence):
    def __init__(self, hdf5_file, indexes, batch_size=512):
        self.hdf5_file = hdf5_file
        self.indexes = indexes
        self.batch_size = batch_size

    def __len__(self):
        # Devuelve el número de lotes por época
        return int(np.ceil(len(self.indexes) / self.batch_size))

    def __getitem__(self, index):
        # Generar un lote de datos
        batch_indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        X = self.__data_generation(batch_indexes)
        return X
    
    def __data_generation(self, batch_indexes):
        X = []
        with h5py.File(self.hdf5_file, 'r') as f:
            for classname, index, dataset_name in batch_indexes:
                dset = f[f'test/{classname}/{index}/{dataset_name}']
                signal = dset[:]
                signal = self.normalize_signal(signal)
                X.append(signal)
                
        return np.array(X)
    
    def normalize_signal(self, signal):
        normalized_signal = 2 * ((signal - np.min(signal)) / (np.max(signal) - np.min(signal))) - 1
        return normalized_signal
