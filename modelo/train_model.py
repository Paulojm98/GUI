# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:39:17 2024

@author: paulo
"""
import tensorflow as tf
import os
import numpy as np
from matplotlib.figure import Figure
from utilidades.util_ticket import TicketPurpose, Ticket
from utilidades.util_custom_callback import CustomCallback
from utilidades.util_data_generator import HDF5DataGenerator
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
from tensorflow.keras.metrics import MeanSquaredError, MeanAbsoluteError

class ModeloEntrenamiento:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        

    def entrenar(self, dataset, carpeta_modelo, nombre_modelo, indices_pristine, indices_damage, tipo_modelo, epochs, batch_size, lr, validation_split, panel, queue_message, no_use_dataloader):
        ticket = Ticket(ticket_type=TicketPurpose.INICIO_TAREA,
                        ticket_value=["Se ha iniciado el entrenamiento del modelo."])
        queue_message.put(ticket)
        panel.event_generate("<<Check_queue>>")
        
        self.tarea_localizacion = False
        batch_size = batch_size
        
        print("Num GPUs Disponibles: ", len(tf.config.list_physical_devices('GPU')))
        
        if not os.path.exists(carpeta_modelo):
            os.makedirs(carpeta_modelo)

        if not nombre_modelo.endswith('.h5'):
            nombre_modelo += '.h5'
            
        if tipo_modelo == "MLP_damagge_detection":
            self.modelo = self.crear_modelo_mlp()
        if tipo_modelo == "CNN1_damage_detection":
            self.modelo = self.crear_modelo_cnn1()
        if tipo_modelo == "MLP_damagge_location":
            self.modelo = self.crear_modelo_mlp_location()
            self.tarea_localizacion = True
        if tipo_modelo == "CNN1_damage_location":
            self.modelo = self.crear_modelo_cnn1_location()
            self.tarea_localizacion = True
            

        self.dataset = dataset
        
        #Callbacks que se utilizan
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
        
        #Optimizador ADAM
        optimizer = Adam(learning_rate= lr)
        
        if self.tarea_localizacion:
            indexes_damage = []
            with open(indices_damage, 'rb') as f:
                indexes_damage = pickle.load(f)

            train_val_indexes, self.test_indexes = train_test_split(indexes_damage, test_size=0.2)
            train_indexes, val_indexes = train_test_split(train_val_indexes, test_size=0.2)
            self.modelo.compile(optimizer=optimizer, loss='mse', metrics=[MeanSquaredError(), MeanAbsoluteError()])
        else:
            train_indexes, val_indexes, self.test_indexes = self.indices_train_val(indices_pristine, indices_damage, validation_split)
            self.modelo.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        
        if no_use_dataloader:
            print("Se van a cargar todos los datos de entrenamietnto en memoria")
            X_train, y_train = self.carga_datos(train_indexes)
            print("Se van a cargar todos los datos de validación en memoria")
            X_val, y_val = self.carga_datos(val_indexes)
            self.history = self.modelo.fit(X_train, y_train,
                                           validation_data=(X_val, y_val),
                                           epochs=epochs,
                                           batch_size = batch_size,
                                           callbacks=callbacks,
                                           shuffle=True)
            
        else:
            train_generator = HDF5DataGenerator(dataset, train_indexes, tarea_localizacion = self.tarea_localizacion, batch_size=batch_size)
            val_generator = HDF5DataGenerator(dataset, val_indexes, tarea_localizacion = self.tarea_localizacion, batch_size=batch_size)
            self.history = self.modelo.fit(train_generator, validation_data=val_generator, epochs=epochs, callbacks=callbacks)
        
        
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
        model = Model(inputs=input_layer, outputs=output_layer, name='MLP_Model_damage_detection')
        
        return model
    
    def crear_modelo_mlp_location(self):
        input_layer = Input(shape=(2500,), name='Input_Layer')
        hidden1 = Dense(256, activation='relu', name='Hidden_Layer_1')(input_layer)
        dropout1 = Dropout(rate=0.2, name='Dropout_1')(hidden1)
        hidden2 = Dense(128, activation='relu', name='Hidden_Layer_2')(dropout1)
        dropout2 = Dropout(rate=0.2, name='Dropout_2')(hidden2)
        hidden3 = Dense(128, activation='relu', name='Hidden_Layer_3')(dropout2)
        dropout3 = Dropout(rate=0.2, name='Dropout_3')(hidden3)
        hidden4 = Dense(16, activation='relu', name='Hidden_Layer_4')(dropout3)
        dropout4 = Dropout(rate=0.2, name='Dropout_4')(hidden4)
        output_layer = Dense(2, name='Output_Layer')(dropout4)
        model = Model(inputs=input_layer, outputs=output_layer, name='MLP_Model_damage_location')
        
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
        model = Model(inputs=input_layer, outputs=output_layer, name='CNN1_Model_damage_detection')
        
        return model
        
    def pintar_graficas(self):
        accuracy_type = "accuracy"
        val_accuracy_type = "val_accuracy"
        label_y_axis = "Precisión"
        if self.tarea_localizacion:
            accuracy_type = "mean_absolute_error"
            val_accuracy_type = "val_mean_absolute_error"
            label_y_axis = "MAE"
            
        fig = Figure(figsize=(12, 6), dpi=100)
        plot1 = fig.add_subplot(121)
        plot2 = fig.add_subplot(122)
        
        plot1.plot(self.history.history[accuracy_type], label='Precisión de Entrenamiento')
        plot1.plot(self.history.history[val_accuracy_type], label='Precisión de Validación')
        plot1.set_title('Precisión a lo largo de las épocas')
        plot1.set_xlabel('Épocas')
        plot1.set_ylabel(label_y_axis)
        plot1.legend()
        
        plot2.plot(self.history.history['loss'], label='Pérdida de Entrenamiento')
        plot2.plot(self.history.history['val_loss'], label='Pérdida de Validación')
        plot2.set_title('Pérdida a lo largo de las épocas')
        plot2.set_xlabel('Épocas')
        plot2.set_ylabel('Pérdida')
        plot2.legend()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        save_path = os.path.join(parent_dir, "resultados_entrenamiento.png")
        fig.savefig(save_path)
        
        return fig
    
    def prediccion_modelo(self):
        X = []
        y = []
        with h5py.File(self.dataset, 'r') as f:
            for classname, index, dataset_name in self.test_indexes:
                dset = f[f'train/{classname}/{index}/{dataset_name}']
                signal = dset[:]
                signal = self.normalize_signal(signal)
                label = dset.attrs['Label']
                X.append(signal)
                y.append(label)
        X = np.array(X)
        y = np.array(y)

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
        train_val_indexes, test_indexes = train_test_split(indexes_combined, test_size=0.2)
        train_indexes, val_indexes = train_test_split(train_val_indexes, test_size=validation_split)
        
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
                if self.tarea_localizacion:
                    etiqueta_x = dset.attrs['label_x']
                    etiqueta_y = dset.attrs['label_y']
                    y.append([etiqueta_x, etiqueta_y])
                else:   
                    label = dset.attrs['Label']
                    y.append(label)
                X.append(signal)
        X = np.array(X)
        y = np.array(y)
        
        return X, y
    

    
         
        