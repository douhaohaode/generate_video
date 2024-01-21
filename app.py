import gradio as gr

from dreamtalk.inference_for_demo_video import generate
from tools import style_clips

css = """
#warning {background-color: #FFCCCB}
.gradio-container {background-color: black}
.feedback textarea {font-size: 24px !important}
.toolbutton {
    margin-buttom: 0em 0em 0em 0em;
    max-width: 2.5em;
    min-width: 2.5em !important;
    height: 2.5em;
}
"""


style_clip_list = style_clips()

pose_list = ["dreamtalk/data/pose/RichardShelby_front_neutral_level1_001.mat"]

device_list = ["cpu", "cuda"]

def batch_video_process(audio_path, image_path,style_clip_path,
                                   pose_path,cfg_scale,max_gen_len,device):
    pass

with gr.Blocks(css=css) as demo:

    with gr.Tab("dreamtalk"):
        with gr.Row():
            audio_path = gr.Audio(label="音频路径", type='filepath')
            image_path = gr.Image(label="头像路径", type='filepath')
        with gr.Row():
            style_clip_path = gr.Dropdown(style_clip_list, label="说话风格", value=style_clip_list[0], )
            pose_path = gr.Dropdown(pose_list, label="头部姿势", value=pose_list[0])
        with gr.Row():
            cfg_scale = gr.Slider(1.0, 10.0, value=1.0, step=1.0, label="说话风格强度")
            max_gen_len = gr.Slider(1.0, 2000.0, value=13.0, step=1.0, label="视频生成持续时间，")
            device = gr.Dropdown(device_list, label="设备", value=device_list[0])

        video_path = gr.Video(label="生成视频")
        generate_btn = gr.Button("生成")
        generate_btn.click(fn=generate,
                           inputs=[audio_path, image_path,style_clip_path,
                                   pose_path,cfg_scale,max_gen_len, device],
                        outputs=video_path)
    with gr.Tab("dreamtalk"):
        with gr.Row():
            input_audio_path = gr.Audio(label="音频路径", type='filepath')

demo.launch()