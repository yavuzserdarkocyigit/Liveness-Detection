import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Flatten,GlobalAveragePooling1D
from keras.optimizers import SGD
from keras.layers import TimeDistributed, Conv2D, MaxPooling2D
from keras.regularizers import l2

model = Sequential([
    
    TimeDistributed(Conv2D(filters=8, kernel_size=(3, 3), activation='relu'), input_shape=(226, 64, 64, 3)),
    TimeDistributed(MaxPooling2D(pool_size=(2, 2))),
    TimeDistributed(Conv2D(filters=16, kernel_size=(3, 3), activation='relu')),
    TimeDistributed(MaxPooling2D(pool_size=(2, 2))),
    TimeDistributed(Flatten()),  

    LSTM(units=50, return_sequences=False),


    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')

])
optimizer = SGD(learning_rate=0.0001, momentum=0.9)
model.compile(optimizer= optimizer, loss='binary_crossentropy', metrics=['accuracy'])



