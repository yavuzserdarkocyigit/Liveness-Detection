import numpy as np
import os
from sklearn.metrics import confusion_matrix
from tensorflow import keras
from keras.models import load_model

model = load_model('/content/rnnmodel.h5')

def load_and_preprocess_data(test_folder):
    X, y = [], []
    for file_name in sorted(os.listdir(test_folder)):
        file_path = os.path.join(test_folder, file_name)
        if os.path.isfile(file_path):
            data = np.load(file_path)
            X.append(data['frames']) 
            y.append(data['label'])   
    return np.array(X), np.array(y)

test_folder = '/content/gdrive/MyDrive/my_processed_data/processed_test'
X_test, y_test = load_and_preprocess_data(test_folder)

y_pred = model.predict(X_test).round().astype(int)

cm = confusion_matrix(y_test, y_pred)


import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(cm, class_names):

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(cm, annot=True, fmt="d", ax=ax, cmap="Blues", cbar=False)

    
    ax.set_xlabel('Predicted Labels')
    ax.set_ylabel('True Labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(class_names)
    ax.yaxis.set_ticklabels(class_names)

    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)

cm = confusion_matrix(y_test, y_pred)

class_names = ['Class 1', 'Class 2']  


plot_confusion_matrix(cm, class_names)
plt.show()
