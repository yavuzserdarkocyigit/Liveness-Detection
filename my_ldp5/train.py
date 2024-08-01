from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.regularizers import l2
import numpy as np
import os
import matplotlib.pyplot as plt
from model import model

batch_size = 16

def load_preprocessed_data(data_folder, batch_size):
    while True:
        X, y = [], []
        for file_name in sorted(os.listdir(data_folder)):
            file_path = os.path.join(data_folder, file_name)
            data = np.load(file_path)
            X.append(data['frames'])
            y.append(data['label'])

            if len(X) == batch_size:
                yield (np.array(X), np.array(y))
                X, y = [], []


train_folder = "C:/Benim programlarim/proj/my_processed_data/processed_train"
val_folder = "C:/Benim programlarim/proj/my_processed_data/processed_val"
test_folder = "C:/Benim programlarim/proj/my_processed_data/processed_test"


train_generator = load_preprocessed_data(train_folder, batch_size)
val_generator = load_preprocessed_data(val_folder, batch_size)
test_generator = load_preprocessed_data(test_folder, batch_size)


train_steps = 280 // batch_size
val_steps = 60 // batch_size


history = model.fit(
    train_generator,
    steps_per_epoch=train_steps,
    epochs=75,
    validation_data=val_generator,
    validation_steps=val_steps,
)
model.save('model2.h5')

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.show()