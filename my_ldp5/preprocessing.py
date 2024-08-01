import cv2
import numpy as np
import os

def preprocess_and_save_videos(video_folder, save_folder, frame_count=226, frame_size=(64, 64)):
    for folder_name in sorted(os.listdir(video_folder)):
        folder_path = os.path.join(video_folder, folder_name)
        frames = []

        frame_names = sorted(os.listdir(folder_path))[:frame_count]
        for frame_name in frame_names:
            frame_path = os.path.join(folder_path, frame_name)
            frame = cv2.imread(frame_path)
            frame = cv2.resize(frame, frame_size)
            frame = frame / 255.0  
            frames.append(frame)

        if len(frames) == frame_count:
            video_data = np.array(frames)
            label = 0 if 'attack' in folder_name else 1
            np.savez_compressed(os.path.join(save_folder, folder_name + '.npz'), frames=video_data, label=label)


train_folder = "C:/Benim programlarim/proj/my_data/my_train"
val_folder = "C:/Benim programlarim/proj/my_data/my_val"
test_folder = "C:/Benim programlarim/proj/my_data/my_test"

save_train_folder = "C:/Benim programlarim/proj/my_processed_data/processed_train"
save_train_folder1 = "C:/Benim programlarim/proj/my_processed_data/processed_val"
save_train_folder2 = "C:/Benim programlarim/proj/my_processed_data/processed_test"
preprocess_and_save_videos(train_folder, save_train_folder)
preprocess_and_save_videos(val_folder, save_train_folder1)
preprocess_and_save_videos(test_folder, save_train_folder2)
