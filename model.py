# import tensorflow as tf
import tensorflow.keras as k
import numpy as np
import PIL
import PIL.Image
import PIL.ImageOps
import os


def _create_trained_model() -> k.Model:
    model = k.models.Sequential([
        k.layers.Flatten(input_shape=(28, 28)),
        k.layers.Dense(128, activation='relu'),
        k.layers.Dropout(0.2),
        k.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    dataset = k.datasets.mnist

    (x_train, y_train), (x_test, y_test) = dataset.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model.fit(x_train, y_train, epochs=10)
    
    return model

def _open_model(model_filename: str):
    if os.path.exists(model_filename):
        return k.models.load_model(model_filename)
    model = _create_trained_model()
    model.save(model_filename)
    return model        

 

_MODEL_CACHE_FILENAME = 'model.tf'

class DigitClassifier:
    def __init__(self) -> None:
        self.model = _open_model(_MODEL_CACHE_FILENAME)
        
    def _predict(self, image: PIL.Image.Image) -> np.ndarray:
        img = PIL.ImageOps.invert(image.convert('L').resize((28, 28), PIL.Image.ANTIALIAS))
        arr = np.array(img)[None,:,:]
        return self.model.predict(arr)
        
    def classify(self, image: PIL.Image.Image) -> int:
        classification = self._predict(image)
        return classification.argmax()
    