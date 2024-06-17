import threading
import time

import gradio as gr
from GPUtil import GPUtil

from codeformer.inference_codeformer import code_former_generate
from dreamtalk.inference_for_demo_video import generate
from hallo_inference import hallo_inference_def
from mergevideo.merge_video import merge_video
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

device_list = ["cuda", "cpu"]

def batch_video_process(audio_path, image_path,style_clip_path,
                                   pose_path,cfg_scale,max_gen_len,device):
    pass

with gr.Blocks(css=css) as demo:

    with gr.Tab("dreamtalk"):
        with gr.Row():
            audio_path = gr.Audio(label="音频路径", type='filepath')
            image_path = gr.Image(label="头像路径", type='filepath',height=251)
        with gr.Row():
            style_clip_path = gr.Dropdown(style_clip_list, label="说话风格", value=style_clip_list[0], )
            pose_path = gr.Dropdown(pose_list, label="头部姿势", value=pose_list[0])
        with gr.Row():
            cfg_scale = gr.Slider(0.1, 1.0, value=1.0, step=0.1, label="说话风格强度")
            max_gen_len = gr.Slider(1.0, 2000.0, value=13.0, step=1.0, label="视频生成持续时间，")
            device = gr.Dropdown(device_list, label="设备", value=device_list[0])

        with gr.Row():
            video_path = gr.Video(label="生成视频",height=251,width=251)
            code_former_video_path = gr.Video(label="生成视频",height=251,width=251)

        generate_btn = gr.Button("生成")
        generate_btn.click(fn=generate,
                           inputs=[audio_path, image_path,style_clip_path,
                                   pose_path,cfg_scale,max_gen_len, device],
                        outputs=video_path)

        code_former_generate_btn = gr.Button("视频增强")
        code_former_generate_btn.click(fn=code_former_generate,
                           inputs=[video_path],
                           outputs=code_former_video_path)

        with gr.Row():
            background_video_path = gr.Video(label="视频路径",height=512,width=512)
            merge_video_path = gr.Video(label="视频路径",height=512,width=512)
        merge_btn = gr.Button("合成")
        merge_btn.click(fn=merge_video, inputs=[background_video_path,video_path,code_former_video_path],
                                       outputs=merge_video_path)


    with gr.Tab("hallo"):
        with gr.Row():
            audio_path = gr.Audio(label="音频路径", type='filepath')
            image_path = gr.Image(label="头像路径", type='filepath', height=251)

        with gr.Row():
            w = gr.Slider(256, 1024, value=512, step=256, label="每秒帧数")
            h = gr.Slider(256, 1024, value=512, step=256, label="每秒帧数")
            inference_steps = gr.Slider(1.0, 50.0, value=40, step=1, label="步数")
            cfg_scale = gr.Slider(1.0, 10.0, value=3.5, step=0.5, label="cfg_scale")

        with gr.Row():
            pose_weight = gr.Slider(1.0, 2.0, value=1.1, step=0.1, label="姿势强度")
            face_weight = gr.Slider(1.0, 2.0, value=1.1, step=0.1, label="脸部强度")
            lip_weight = gr.Slider(1.0, 2.0, value=1.1, step=0.1, label="唇部强度")

        with gr.Row():
            video_path = gr.Video(label="生成视频",height=251,width=251)

        generate_btn = gr.Button("生成")
        generate_btn.click(fn=hallo_inference_def,
                           inputs=[audio_path, image_path,pose_weight,face_weight,lip_weight,inference_steps,cfg_scale,w,h],
                           outputs=video_path)



def monitor_gpu_utilization(interval=1):
    try:
        while True:
            # 获取所有可用的GPU列表
            gpus = GPUtil.getGPUs()

            # 打印每个GPU的使用情况
            for gpu in gpus:
                print(f"GPU {gpu.id}:")
                print(f"  Name: {gpu.name}")
                print(f"  Load: {gpu.load * 100:.1f}%")
                print(f"  Free Memory: {gpu.memoryFree}MB")
                print(f"  Used Memory: {gpu.memoryUsed}MB")
                print(f"  Total Memory: {gpu.memoryTotal}MB")
                print(f"  Temperature: {gpu.temperature}C")
                print()

            # 等待指定的间隔时间
            time.sleep(interval)
    except KeyboardInterrupt:
        print("实时GPU使用情况监控已终止")


def start_monitoring_thread(interval=1):
    # 启动一个线程来监控GPU使用情况
    monitoring_thread = threading.Thread(target=monitor_gpu_utilization, args=(interval,))
    monitoring_thread.daemon = True  # 设置为守护线程，主程序退出时这个线程也会退出
    monitoring_thread.start()



if __name__ == "__main__":
    start_monitoring_thread(interval=30)

    demo.launch().launch(share=False)