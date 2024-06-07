# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:36:11 2024

@author: paulo
"""
import tensorflow as tf
import os
import numpy as np
from matplotlib.figure import Figure
from utilidades.util_ticket import TicketPurpose, Ticket
from utilidades.util_custom_callback import CustomCallback
import pickle
from sklearn.model_selection import train_test_split
import h5py
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn import metrics
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

class ModeloEntrenamientoCargaMenmoria:
    
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        

    def entrenar(self, dataset, carpeta_modelo, nombre_modelo, indices_pristine, indices_damage, tipo_modelo, epochs, batch_size, lr, validation_split, panel, queue_message, random_seed=None):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado el entrenamiento del modelo."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        
        print("Num GPUs Disponibles: ", len(tf.config.list_physical_devices('GPU')))

        self.dataset = dataset
        
        train_indexes, val_indexes, self.test_indexes = self.indices_train_val(indices_pristine, indices_damage, validation_split)
        batch_size = batch_size
        
        #Aquí está la diferencia con el otro script
        #Se cargan todas los datos en memoria
        print("Se van a cargar todos los datos de entrenamietnto en memoria")
        X_train, y_train = self.carga_datos(train_indexes)
        
        print("Se van a cargar todos los datos de validación en memoria")
        X_val, y_val = self.carga_datos(val_indexes)
        
        if tipo_modelo == "MLP":
            self.modelo = self.crear_modelo_mlp()
        if tipo_modelo == "CNN1":
            self.modelo = self.crear_modelo_cnn1()
        
        if not os.path.exists(carpeta_modelo):
            os.makedirs(carpeta_modelo)

        if not nombre_modelo.endswith('.h5'):
            nombre_modelo += '.h5'
            
        #Callbacks
        ruta_checkpoint_callback = os.path.join(self.parent_dir, nombre_modelo)
        checkpoint_callback = ModelCheckpoint(
            filepath=ruta_checkpoint_callback,
            save_weights_only=False,
            save_best_only=False,
            save_freq='epoch')
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.1,
            patience=10,
            min_lr=0.00001)
        
        callbacks = [CustomCallback(panel, queue_message), checkpoint_callback, reduce_lr]
        
        optimizer = Adam(learning_rate= lr)
        self.modelo.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

        self.history = self.modelo.fit(X_train, y_train,
                                       validation_data=(X_val, y_val),
                                       epochs=epochs,
                                       batch_size = batch_size,
                                       callbacks=callbacks,
                                       shuffle=True)
        
        ruta_modelo_guardar = os.path.join(carpeta_modelo, nombre_modelo)

        self.modelo.save(ruta_modelo_guardar)
        
        
        
        ticket = Ticket(ticket_type=TicketPurpose.FIN_TAREA,
                        ticket_value=["Se ha terminado el proceso de entrenamiento y se ha guardado el modelo"])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        
        
        
    def crear_modelo_mlp(self):
        input_layer = Input(shape=(2500,), name='Input_Layer')
        hidden1 = Dense(256, activation='relu', name='Hidden_Layer_1')(input_layer)
        dropout1 = Dropout(rate=0.2, name='Dropout_1')(hidden1)
        hidden2 = Dense(128, activation='relu', name='Hidden_Layer_2')(dropout1)
        dropout2 = Dropout(rate=0.2, name='Dropout_2')(hidden2)
        hidden3 = Dense(128, activation='relu', name='Hidden_Layer_3')(dropout2)
        dropout3 = Dropout(rate=0.2, name='Dropout_3')(hidden3)
        hidden4 = Dense(16, activation='relu', name='Hidden_Layer_4')(dropout3)
        dropout4 = Dropout(rate=0.2, name='Dropout_4')(hidden4)
        output_layer = Dense(1, activation='sigmoid', name='Output_Layer')(dropout4)
        model = Model(inputs=input_layer, outputs=output_layer, name='MLP_Model_bigdata')
        
        return model
    
    def crear_modelo_cnn1(self):
        input_layer = Input(shape=(2500, 1), name='Conv1d_1_input')
        conv1 = Conv1D(filters=16, kernel_size=3, activation='relu', name='Conv1d_1')(input_layer)
        dropout1 = Dropout(rate=0.2, name='Dropout_1')(conv1)
        max_pooling1 = MaxPooling1D(pool_size=2, name='Max_pooling1d_1')(dropout1)
        conv2 = Conv1D(filters=32, kernel_size=3, activation='relu', name='Conv1d_2')(max_pooling1)
        dropout2 = Dropout(rate=0.2, name='Dropout_2')(conv2)
        max_pooling2 = MaxPooling1D(pool_size=2, name='Max_pooling1d_2')(dropout2)
        conv3 = Conv1D(filters=64, kernel_size=3, activation='relu', name='Conv1d_3')(max_pooling2)
        dropout3 = Dropout(rate=0.2, name='Dropout_3')(conv3)
        max_pooling3 = MaxPooling1D(pool_size=2, name='Max_pooling1d_3')(dropout3)
        flatten = Flatten(name='Flatten')(max_pooling3)
        dense1 = Dense(128, activation='relu')(flatten)
        dropout4 = Dropout(rate=0.3, name='Dropout_4')(dense1)
        output_layer = Dense(1, activation='sigmoid', name='Output')(dropout4)
        model = Model(inputs=input_layer, outputs=output_layer, name='CNN1_Model_bigdata')
        
        return model
        
    def pintar_graficas(self):
        fig = Figure(figsize=(12, 6), dpi=100)
        plot1 = fig.add_subplot(121)
        plot2 = fig.add_subplot(122)
        
        plot1.plot(self.history.history['accuracy'], label='Precisión de Entrenamiento')
        plot1.plot(self.history.history['val_accuracy'], label='Precisión de Validación')
        plot1.set_title('Precisión a lo largo de las épocas')
        plot1.set_xlabel('Épocas')
        plot1.set_ylabel('Precisión')
        plot1.legend()
        
        plot2.plot(self.history.history['loss'], label='Pérdida de Entrenamiento')
        plot2.plot(self.history.history['val_loss'], label='Pérdida de Validación')
        plot2.set_title('Pérdida a lo largo de las épocas')
        plot2.set_xlabel('Épocas')
        plot2.set_ylabel('Pérdida')
        plot2.legend()

        save_path = os.path.join(self.parent_dir, "resultados_entrenamiento.png")
        fig.savefig(save_path)
        
        return fig
    
    def prediccion_modelo(self):
        
        X, y = self.carga_datos(self.test_indexes)
        predicciones = self.modelo.predict(X)
        predicciones = np.array(predicciones).flatten()
        predicciones = (predicciones > 0.5).astype(int)

        accuracy = accuracy_score(y, predicciones)
        conf_matrix = confusion_matrix(y, predicciones)
        print(conf_matrix)
        print(accuracy)
        fig, ax = plt.subplots(figsize=(8, 6))
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=['Pristine', 'Damage'])
        cm_display.plot(ax=ax)
        
        
        save_path = os.path.join(self.parent_dir, "resultados_prediccion.png")
        fig.savefig(save_path)
        
    
    def indices_train_val(self, indices_pristine, indices_damage, validation_split):
        indexes_pristine = []
        indexes_damage = []
        with open(indices_pristine, 'rb') as f:
            indexes_pristine = pickle.load(f)

        with open(indices_damage, 'rb') as f:
            indexes_damage = pickle.load(f)
        
        num_pristine = len(indexes_pristine)
        indexes_damage_selected = np.random.choice(len(indexes_damage), num_pristine, replace=False)

        indexes_damage_selected = [indexes_damage[i] for i in indexes_damage_selected]

        print(f"[INFO] Señales sin daño: {len(indexes_pristine)}")
        print(f"[INFO] Señales con daño: {len(indexes_damage)}")
        
        indexes_combined = indexes_pristine + indexes_damage_selected
        print(f"[INFO] Señales totales para el proceso: {len(indexes_combined)}")

        # Dividir los índices en entrenamiento y validación
        train_val_indexes, test_indexes = train_test_split(indexes_combined, test_size=0.2, random_state=41)
        train_indexes, val_indexes = train_test_split(train_val_indexes, test_size=validation_split, random_state=40)
        
        return train_indexes, val_indexes, test_indexes
    
    def normalize_signal(self, signal):
        normalized_signal = 2 * ((signal - np.min(signal)) / (np.max(signal) - np.min(signal))) - 1
        return normalized_signal
    
    def carga_datos(self, indexes):
        X = []
        y = []
        with h5py.File(self.dataset, 'r') as f:
            for classname, index, dataset_name in indexes:
                dset = f[f'train/{classname}/{index}/{dataset_name}']
                signal = dset[:]
                signal = self.normalize_signal(signal)
                label = dset.attrs['Label']
                X.append(signal)
                y.append(label)
        X = np.array(X)
        y = np.array(y)
        
        return X, y
        
                
                
                
        