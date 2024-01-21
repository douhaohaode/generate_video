import os

def style_clips():
    directory = os.path.dirname(os.path.abspath(__file__))
    dreamtalk_folder = os.path.join(directory, "dreamtalk/data/style_clip/3DMM")
    file_paths = [os.path.join(dreamtalk_folder, file) for file in os.listdir(dreamtalk_folder)]
    print(file_paths)
# style_clip_path
    return file_paths
