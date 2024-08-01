import os
import imageio

def extract_frames(video_path, output_folder, label, max_duration=None, fps=24):

    reader = imageio.get_reader(video_path)
    video_fps = reader.get_meta_data()['fps']

    if max_duration:
        max_frames = int(video_fps * max_duration)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_folder = os.path.join(output_folder, label, video_name)
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    for i, frame in enumerate(reader):
        if max_duration and i > max_frames:
            break
        if i % (video_fps // fps) == 0:
            frame_path = os.path.join(frame_folder, f"{video_name}_frame_{i}.jpg")
            imageio.imwrite(frame_path, frame)

def process_videos_from_folder(video_folder, output_folder, label, max_duration=None):

    videos = [f for f in os.listdir(video_folder) if f.endswith('.mov')]

    for video in videos:
        video_path = os.path.join(video_folder, video)
        extract_frames(video_path, output_folder, label, max_duration)


real_video_folder = "C:/Benim programlarim/proj/real" 
attack_video_folder = "C:/Benim programlarim/proj/attack" 
output_folder = "C:/Benim programlarim/proj/frames" 

process_videos_from_folder(real_video_folder, output_folder, 'real', max_duration=9)
process_videos_from_folder(attack_video_folder, output_folder, 'attack')

