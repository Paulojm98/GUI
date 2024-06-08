# GUI
Interfaz gráfica para entrenar modelos de machine learning
Nuevas funciones:
  Selección de archivos o carpetas mediante FileDialog de tkinter
  Nueva opción añadida para realizar el entrenamiento con todos los datos cargados en memoria "Entrenar Memoria"
  Adición de nuevos callbacks:
    ReduceLROnPlateau, para reducir el valor del learning rate si la perdida de validación no mejora tras 10 épocas
    ModelCheckpoint, se realiza un guardado del modelo al final de cada época, por si ocurre algún imprevisto

Funciones por añadir:
  Trasladar la información completa de la consola al panel derecho de la interfaz
  Implementar un método para detener el entrenamiento mediante un botón o una combinación de teclas
