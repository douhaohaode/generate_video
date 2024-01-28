from moviepy.editor import *


def merge_video(video_path_1, video_path_2,video_path_3):
    overlay_video_path = video_path_3
    if overlay_video_path == None or overlay_video_path == "":
        overlay_video_path = video_path_2

    background_video = VideoFileClip(video_path_1)

    overlay_video = VideoFileClip(overlay_video_path)

    overlay_video = overlay_video.resize(height=background_video.h // 3)

    x_pos = background_video.w - overlay_video.w - 60
    y_pos = background_video.h - overlay_video.h - 60

    final_video = CompositeVideoClip([background_video.set_pos('center'), overlay_video.set_pos((x_pos, y_pos))])

    result_path= f'results/output.mp4'

    final_video.write_videofile(result_path ,codec="libx264", audio_codec="aac")

    return result_path



