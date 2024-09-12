import gradio as gr
import os
from predict import predict_factory
import numpy as np

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
project_dir=os.path.dirname(os.path.abspath(__file__))
default_model_path = os.path.join(project_dir,"model")
default_save_path = os.path.join(project_dir,"temp")
model_types = (".pt")
model_list = []

def predict(input_img_path):
    result = predict_factory.predict(input_img_path)
    return predict_factory.get_plotted_image(result[0]),f'''
    {result[0].verbose()}\n
    {result[0].speed}\n
    {result[0].tojson()}
    '''

def get_all_model():
    global model_list
    model_list = []
    for file_name in os.listdir(default_model_path):
        if(os.path.splitext(file_name)[-1] in model_types):
            model_list.append(os.path.join(default_model_path,file_name))

get_all_model()

def refresh_model_list():
    global model_list
    get_all_model()
    return {"choices": model_list,"value":model_list[0], "__type__": "update"}

def load_model(model_path):
    print(model_path)
    predict_factory.load_model(model_path)
    return {"value":f"Loaded Model:{model_path}", "__type__": "update"}

def create_webui():
    with gr.Blocks() as demo:
        with gr.Tab("Predict"):
            with gr.Row():
                model_dorp_down = gr.Dropdown(label="Model List",choices=model_list,value=model_list[0],interactive=True)
                model_refresh_btn = gr.Button("Refresh Model")
                model_load_btn = gr.Button("Load Model",variant='primary')
            with gr.Row():
                model_info_label = gr.Label(value=f"Loaded Model:{model_list[0]}",show_label=False)
            with gr.Row():
                input_img = gr.Image(label="Input Image",interactive=True)
                output_img = gr.Image(label="Output Image",interactive=False)
            process_btn = gr.Button("Detect",variant='primary')
            with gr.Row():
                cuda_info_text = gr.TextArea(label="Predict info",interactive=False)
            model_refresh_btn.click(fn=refresh_model_list,outputs=model_dorp_down)
            model_load_btn.click(fn=load_model,inputs=model_dorp_down,outputs=model_info_label)
            process_btn.click(fn=predict,inputs=input_img,outputs=[output_img,cuda_info_text])
    return demo
    
demo = create_webui()

if __name__ == "__main__":
    demo.launch(server_port=2777,share=True)